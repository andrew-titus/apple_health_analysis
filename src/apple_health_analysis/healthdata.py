import logging
import os
import xml.etree.ElementTree as ET

import pandas as pd
from pydantic import BaseModel, Field
from tqdm import tqdm

from apple_health_analysis.record import RECORD_TAG, Record


logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()


# ../../../apple_health
APPLE_HEALTH_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "apple_health"
)


class HealthData(BaseModel):
    """Container class for Apple HealthKit data."""

    class Config:
        # Allow Pandas DataFrame
        arbitrary_types_allowed = True

    # Dataframe of HKObjectType records from HealthKit
    records: pd.DataFrame = Field(default_factory=pd.DataFrame)

    # TODO: ActivitySummary

    # TODO: Workouts

    # TODO: other things like ClinicalRecord?

    @classmethod
    def from_xml_export(cls, export: os.PathLike, verbose: bool = True) -> "HealthData":
        """Parse an XML export file into a HealthData object."""
        logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        logger.debug("Creating HealthData from export XML file.")

        logger.debug("Reading export XML file...")
        export_tree = ET.parse(export)
        export_root = export_tree.getroot()
        if export_root.tag != "HealthData":
            raise ValueError(f"Unable to find HealthData tag in {export}")

        records_list: list[Record] = list()

        logger.debug("Parsing elements from export XML file...")
        elem_iter = tqdm(export_root) if verbose else export_root
        for elem in elem_iter:
            # TODO: handle other tags as well
            if elem.tag == RECORD_TAG:
                records_list.append(Record.from_xml_element(elem))

        logger.debug("Converting records to dictionaries...")
        records_dicts: list[dict] = list()
        records_iter = tqdm(records_list) if verbose else records_list
        for record in records_iter:
            records_dicts.append(dict(record))

        logger.debug("Converting record dictionaries to DataFrame...")
        records_df = pd.DataFrame(records_dicts)

        logger.debug("Creating HealthData...")
        return cls(records=records_df)

    def save_cache(self, cache: os.PathLike, verbose: bool = True) -> None:
        """Save this object to a cache for future reuse."""
        logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        logger.debug("Saving HealthData to cache at %s", cache)

        if os.path.exists(cache):
            raise FileExistsError(
                f"Cache already exists at {cache}; delete before saving"
            )
        logger.debug("Creating cache directory at %s...", cache)
        os.makedirs(cache)

        records_jsonl = os.path.join(cache, "records.jsonl")
        logger.debug("Saving records to cache at %s...", records_jsonl)
        self.records.to_json(records_jsonl, orient="records", lines=True)

        logger.debug("DONE saving HealthData to cache at %s", cache)

    @classmethod
    def from_cache(cls, cache: os.PathLike, verbose: bool = True) -> "HealthData":
        """Load a cached HealthData object."""
        logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        logger.debug("Loading HealthData from cache at %s", cache)

        if not os.path.isdir(cache):
            raise FileNotFoundError(f"Cache not found at {cache}")

        records_jsonl = os.path.join(cache, "records.jsonl")
        if not os.path.isfile(records_jsonl):
            raise FileNotFoundError(f"Records JSONL not found at {records_jsonl}")

        logger.debug("Loading records from cache at %s...", records_jsonl)
        records_df = pd.read_json(records_jsonl, orient="records", lines=True)

        logger.debug("Creating HealthData...")
        return cls(records=records_df)


def get_healthdata(verbose: bool = True, use_cache: bool = True) -> HealthData:
    """Parse the export.xml file in the Apple Health directory into a HealthData object."""
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    cache = os.path.join(APPLE_HEALTH_DIR, "export_cache")
    if os.path.isdir(cache):
        if use_cache:
            logger.info("Using cache found at %s", cache)
            return HealthData.from_cache(cache)
        else:
            logger.info("Ignoring cache found at %s, since use_cache=False", cache)
    else:
        logger.info("No cache found at %s; creating from scratch")

    export = os.path.join(APPLE_HEALTH_DIR, "export.xml")
    if not os.path.isfile(export):
        raise FileNotFoundError(f"Did not find export.xml in {APPLE_HEALTH_DIR}")

    healthdata = HealthData.from_xml_export(export, verbose=verbose)

    healthdata.save_cache(cache, verbose=verbose)

    return healthdata
