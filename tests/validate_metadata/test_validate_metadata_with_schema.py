import pytest
import jsonschema
import json

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

    schema = json.loads(open('metadata/schemas/sensor.json').read())

    jsonschema.validate(metadata, schema)