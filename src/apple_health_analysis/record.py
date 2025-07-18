from datetime import datetime, timezone
from xml.etree.ElementTree import Element

from pydantic import BaseModel


RECORD_TAG = "Record"
RECORD_DATETIME_FMT = "%Y-%m-%d %H:%M:%S %z"


def get_xml_datetime(element: Element, key: str) -> datetime | None:
    """Get a datetime object for the given key in the XML element, if any."""
    xml_datetime: datetime | None = None
    if key in element.attrib:
        xml_datetime_pre = datetime.strptime(element.attrib[key], RECORD_DATETIME_FMT)

        # Pandas JSON serialization doesn't handle timezones correctly (dropping to UTC)
        xml_datetime = datetime.fromtimestamp(
            xml_datetime_pre.timestamp(), tz=timezone.utc
        )
    return xml_datetime


class Record(BaseModel):
    """Container for HKObjectType records from HealthKit."""

    # Type of record (e.g., heart rate)
    # TODO: change to an enum?
    record_type: str

    # Value and units for the record
    value: float | str | None = None
    unit: str | None = None

    # Source of record (e.g., a third-party app)
    source_name: str | None = None

    # Start and end date for the record (often the same/instantaneous), as well as date of creation
    start_date: datetime | None = None
    end_date: datetime | None = None
    creation_date: datetime | None = None

    @classmethod
    def from_xml_element(cls, element: Element) -> "Record":
        """Create a Record object from an XML element describing it."""
        parsed_value: float | str | None = None
        if "value" in element.attrib:
            try:
                parsed_value = float(element.attrib["value"])
            except ValueError:
                parsed_value = element.attrib["value"]

        return cls(
            record_type=element.attrib.get("type"),
            value=parsed_value,
            unit=element.attrib.get("unit"),
            source_name=element.attrib.get("sourceName"),
            start_date=get_xml_datetime(element, "startDate"),
            end_date=get_xml_datetime(element, "endDate"),
            creation_date=get_xml_datetime(element, "creationDate"),
        )
