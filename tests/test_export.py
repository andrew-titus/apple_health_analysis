import os
import shutil
from tempfile import mkdtemp
import unittest
from unittest.mock import patch

from apple_health_analysis.export import parse_export


class TestExport(unittest.TestCase):
    def test_parse_export(self) -> None:
        """Test that Apple Health export parsing works as expected."""
        mock_health_dir = mkdtemp()
        try:
            with patch(
                "apple_health_analysis.export.APPLE_HEALTH_DIR", mock_health_dir
            ):
                with (
                    self.subTest(name="Missing export file"),
                    self.assertRaises(FileNotFoundError),
                ):
                    parse_export()

                with self.subTest(name="No HealthData"):
                    with open(os.path.join(mock_health_dir, "export.xml"), "w") as fd:
                        fd.write(
                            "<SomeOtherTag><HealthData></HealthData></SomeOtherTag>\n"
                        )
                    with self.assertRaises(ValueError):
                        parse_export()

                with self.subTest(name="No HealthData"):
                    with open(os.path.join(mock_health_dir, "export.xml"), "w") as fd:
                        fd.write("<HealthData></HealthData>\n")
                    export_root = parse_export()
                    self.assertEqual(export_root.tag, "HealthData")
        finally:
            shutil.rmtree(mock_health_dir)
