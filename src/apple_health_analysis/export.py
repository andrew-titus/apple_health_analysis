import os
import xml.etree.ElementTree as ET


# ../../../apple_health
APPLE_HEALTH_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "apple_health"
)


def parse_export() -> ET.Element:
    """Parse the export.xml file into a xml.etree.ElementTree.Element file."""
    EXPORT = os.path.join(APPLE_HEALTH_DIR, "export.xml")
    if not os.path.isfile(EXPORT):
        raise FileNotFoundError(f"Did not find export.xml in {APPLE_HEALTH_DIR}")

    export_tree = ET.parse(EXPORT)
    export_root = export_tree.getroot()
    if export_root.tag != "HealthData":
        raise ValueError(f"Unable to find HealthData tag in {EXPORT}")
    return export_root
