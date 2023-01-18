import pytest
import jsonschema
import os
import json

def test_sensor():
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
    }
    }
    
    # path to schema file
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(ROOT_DIR, '..', '..', '..', 'digitaltwin', 'metadata', 'schemas','sensor.json' ) 
    schema = json.loads(open(schema_path).read())

    try:
    # validate data against schema
      jsonschema.validate(metadata, schema)
      assert True, f"The data is valid according to the schema."
    except jsonschema.exceptions.ValidationError as e:
      assert False, f"The data is not valid. {e}"
    except jsonschema.exceptions.SchemaError as e:
      assert False, f"The schema is not valid. {e}"

    