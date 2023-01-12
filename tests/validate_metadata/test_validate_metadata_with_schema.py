import pytest
import jsonschema
import os
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
        "unit": "K",
      },
    "independent_variable":       {
        "type": "time",
        "unit": "s"
      }
    }
    

    
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    schema_path = os.path.join(ROOT_DIR, '..', '..', 'metadata', 'schemas','sensor.json' ) 

    schema = json.loads(open(schema_path).read())

    jsonschema.validate(metadata, schema)