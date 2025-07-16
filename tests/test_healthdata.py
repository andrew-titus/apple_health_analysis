import os
import shutil
from tempfile import mkdtemp
import unittest
from unittest.mock import patch

from apple_health_analysis.healthdata import get_healthdata


class TestExport(unittest.TestCase):
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

                # TODO: more tests
        finally:
            shutil.rmtree(mock_health_dir)
