import pytest
from pytest_json_schema import assert_valid_schema

def test_validate_metadata():
    # Define the data to validate
    metadata = {
    "sensor_id": "sensor-001",
    "package_id": "package-001",
    "position": {
        "location": [0, 1, 0]
    },
    "measuring_quantity" :       {
        "type": "temperature",
        "unit": "K"
      },
    "independent_variable":       {
        "type": "time",
        "unit": "s"
      }
    }

    with assert_valid_schema({'response': '/../../metadata/schemas/sensor.json'}):
        response = metadata