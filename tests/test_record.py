from datetime import datetime, timedelta, timezone
import unittest
import xml.etree.ElementTree as ET

from pydantic import ValidationError

from apple_health_analysis.record import Record, get_xml_datetime


INVALID_RECORD_NO_TYPE = '<Record value="123.456"></Record>'
VALID_RECORD_FLOAT = """<Record type="HKQuantityTypeIdentifierHeartRate" sourceName="Test Source" sourceVersion="1.234" device="Test Device" unit="count/min" creationDate="2025-01-03 01:23:45 -0400" startDate="2025-01-01 01:23:45 -0400" endDate="2025-01-02 01:23:45 -0400" value="123.456">
  <MetadataEntry key="HKMetadataKeyHeartRateMotionContext" value="0"/>
</Record>"""
VALID_RECORD_STR = """<Record type="HKCategoryTypeIdentifierSleepAnalysis" sourceName="Test Source 2" sourceVersion="123" creationDate="2024-12-31 23:59:59 +0400" startDate="2024-12-31 23:59:58 +0400" endDate="2024-12-31 23:59:58 +0400" value="HKCategoryValueSleepAnalysisAsleepUnspecified">
</Record>"""


class TestRecord(unittest.TestCase):
    def test_get_xml_datetime(self) -> None:
        """Test the XML datetime utility works as expected."""
        element = ET.fromstring(
            '<Record startDate="2025-01-01 01:23:45 +0500" endDate="2025/01/01"></Record>'
        )

        with self.subTest(name="no key"):
            self.assertIsNone(get_xml_datetime(element, "creationDate"))

        with self.subTest(name="valid float"):
            self.assertEqual(
                get_xml_datetime(element, "startDate"),
                datetime(
                    2025,
                    1,
                    1,
                    hour=1,
                    minute=23,
                    second=45,
                    tzinfo=timezone(timedelta(hours=5)),
                ),
            )

        with self.subTest(name="invalid format"), self.assertRaises(ValueError):
            get_xml_datetime(element, "endDate")

    def test_Record(self) -> None:
        """Test that the Record container works as expected."""
        with self.subTest(valid=False, name="no type"):
            with self.assertRaises(ValidationError):
                Record.from_xml_element(ET.fromstring(INVALID_RECORD_NO_TYPE))

        with self.subTest(valid=True, val="float"):
            record = Record.from_xml_element(ET.fromstring(VALID_RECORD_FLOAT))
            self.assertEqual(record.record_type, "HKQuantityTypeIdentifierHeartRate")
            self.assertEqual(record.source_name, "Test Source")
            self.assertAlmostEqual(record.value, 123.456)
            self.assertEqual(record.unit, "count/min")
            self.assertEqual(
                record.creation_date,
                datetime(
                    2025,
                    1,
                    3,
                    hour=1,
                    minute=23,
                    second=45,
                    tzinfo=timezone(timedelta(hours=-4)),
                ),
            )
            self.assertEqual(
                record.start_date,
                datetime(
                    2025,
                    1,
                    1,
                    hour=1,
                    minute=23,
                    second=45,
                    tzinfo=timezone(timedelta(hours=-4)),
                ),
            )
            self.assertEqual(
                record.end_date,
                datetime(
                    2025,
                    1,
                    2,
                    hour=1,
                    minute=23,
                    second=45,
                    tzinfo=timezone(timedelta(hours=-4)),
                ),
            )

        with self.subTest(valid=True, val="str"):
            record = Record.from_xml_element(ET.fromstring(VALID_RECORD_STR))
            self.assertEqual(
                record.record_type, "HKCategoryTypeIdentifierSleepAnalysis"
            )
            self.assertEqual(record.source_name, "Test Source 2")
            self.assertIsNone(record.unit)
            self.assertEqual(
                record.creation_date,
                datetime(
                    2024,
                    12,
                    31,
                    hour=23,
                    minute=59,
                    second=59,
                    tzinfo=timezone(timedelta(hours=4)),
                ),
            )
            self.assertEqual(
                record.start_date,
                datetime(
                    2024,
                    12,
                    31,
                    hour=23,
                    minute=59,
                    second=58,
                    tzinfo=timezone(timedelta(hours=4)),
                ),
            )
            self.assertEqual(
                record.end_date,
                datetime(
                    2024,
                    12,
                    31,
                    hour=23,
                    minute=59,
                    second=58,
                    tzinfo=timezone(timedelta(hours=4)),
                ),
            )

            # Regression test for Pandas not serializing timezone info
            self.assertEqual(record.start_date.tzinfo, timezone.utc)
            self.assertEqual(record.end_date.tzinfo, timezone.utc)
            self.assertEqual(record.creation_date.tzinfo, timezone.utc)
