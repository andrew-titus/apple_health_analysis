import os
import xml.etree.ElementTree as ET

import pandas as pd
from pydantic import BaseModel, Field


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
    def from_xml_export(cls, export: os.PathLike) -> "HealthData":
        """Parse an XML export file into a HealthData object."""
        export_tree = ET.parse(export)
        export_root = export_tree.getroot()
        if export_root.tag != "HealthData":
            raise ValueError(f"Unable to find HealthData tag in {export}")

        # TODO
        return None


def get_healthdata() -> HealthData:
    """Parse the export.xml file in the Apple Health directory into a HealthData object."""
    EXPORT = os.path.join(APPLE_HEALTH_DIR, "export.xml")
    if not os.path.isfile(EXPORT):
        raise FileNotFoundError(f"Did not find export.xml in {APPLE_HEALTH_DIR}")
    return HealthData.from_xml_export(EXPORT)
