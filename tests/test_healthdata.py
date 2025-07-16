from datetime import datetime, timedelta, timezone
import os
import shutil
from tempfile import mkdtemp
import unittest
from unittest.mock import patch

import pandas as pd

from apple_health_analysis.healthdata import get_healthdata


VALID_EXPORT_XML = """<HealthData>
  <SomeOtherTag>Hello world!</SomeOtherTag>
  <Record type="HKQuantityTypeIdentifierHeartRate" sourceName="Test Source" sourceVersion="1.234" device="Test Device" unit="count/min" creationDate="2025-01-03 01:23:45 -0400" startDate="2025-01-01 01:23:45 -0400" endDate="2025-01-02 01:23:45 -0400" value="123.456">
    <MetadataEntry key="HKMetadataKeyHeartRateMotionContext" value="0"/>
  </Record>
  <Record type="HKQuantityTypeIdentifierHeartRate" sourceName="Test Source" sourceVersion="1.234" device="Test Device" unit="count/min" creationDate="2025-01-03 02:34:56 -0400" startDate="2025-01-01 02:34:56 -0400" endDate="2025-01-02 02:34:56 -0400" value="100">
    <MetadataEntry key="HKMetadataKeyHeartRateMotionContext" value="0"/>
  </Record>
</HealthData>"""


class TestHealthData(unittest.TestCase):
    def test_get_healthdata(self) -> None:
        """Test that Apple Health export parsing works as expected."""
        mock_health_dir = mkdtemp()
        try:
            with patch(
                "apple_health_analysis.healthdata.APPLE_HEALTH_DIR", mock_health_dir
            ):
                with (
                    self.subTest(name="Missing export file"),
                    self.assertRaises(FileNotFoundError),
                ):
                    get_healthdata()

                with self.subTest(name="No HealthData"):
                    with open(os.path.join(mock_health_dir, "export.xml"), "w") as fd:
                        fd.write(
                            "<SomeOtherTag><HealthData></HealthData></SomeOtherTag>\n"
                        )
                    with self.assertRaises(ValueError):
                        get_healthdata()

                with self.subTest(name="Valid HealthData"):
                    with open(os.path.join(mock_health_dir, "export.xml"), "w") as fd:
                        fd.write(VALID_EXPORT_XML)
                    healthdata = get_healthdata()

                    expected_records_df = pd.DataFrame(
                        {
                            "record_type": [
                                "HKQuantityTypeIdentifierHeartRate",
                                "HKQuantityTypeIdentifierHeartRate",
                            ],
                            "value": [123.456, 100],
                            "unit": ["count/min", "count/min"],
                            "source_name": ["Test Source", "Test Source"],
                            "start_date": [
                                datetime(
                                    2025,
                                    1,
                                    1,
                                    hour=1,
                                    minute=23,
                                    second=45,
                                    tzinfo=timezone(timedelta(hours=-4)),
                                ),
                                datetime(
                                    2025,
                                    1,
                                    1,
                                    hour=2,
                                    minute=34,
                                    second=56,
                                    tzinfo=timezone(timedelta(hours=-4)),
                                ),
                            ],
                            "end_date": [
                                datetime(
                                    2025,
                                    1,
                                    2,
                                    hour=1,
                                    minute=23,
                                    second=45,
                                    tzinfo=timezone(timedelta(hours=-4)),
                                ),
                                datetime(
                                    2025,
                                    1,
                                    2,
                                    hour=2,
                                    minute=34,
                                    second=56,
                                    tzinfo=timezone(timedelta(hours=-4)),
                                ),
                            ],
                            "creation_date": [
                                datetime(
                                    2025,
                                    1,
                                    3,
                                    hour=1,
                                    minute=23,
                                    second=45,
                                    tzinfo=timezone(timedelta(hours=-4)),
                                ),
                                datetime(
                                    2025,
                                    1,
                                    3,
                                    hour=2,
                                    minute=34,
                                    second=56,
                                    tzinfo=timezone(timedelta(hours=-4)),
                                ),
                            ],
                        }
                    )
                    self.assertTrue(healthdata.records.equals(expected_records_df))
        finally:
            shutil.rmtree(mock_health_dir)
