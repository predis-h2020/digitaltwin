import jsonschema

# Define the schema, this can also be read from file, here is just a text example
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Waste Package Monitoring Sensor Metadata",
    "description": "Metadata for a waste package monitoring sensor, including its unique identifier, position, and measurement capabilities.",
    "type": "object",
    "required": [
        "sensor_id",
        "position",
        "measuring_quantity"
    ],
    "properties": {
        "sensor_id": {
            "description": "A unique identifier for the sensor.",
            "type": "string"
        },
        "package_id": {
            "description": "A unique identifier for the Waste Package where the sensor is placed.",
            "type": "string"
        },
        "position": {
            "description": "The position of the sensor defined by location and optional orientation.",
            "type": "object",
            "required": [
                "location"
            ],
            "properties": {
                "location": {
                    "description": "The XYZ coordinates of the sensor.",
                    "type": "array",
                    "items": {
                        "type": "number"
                    }
                },
                "orientation": {
                    "description": "The XYZ coordinates of the orientation.",
                    "type": "array",
                    "items": {
                        "type": "number"
                    }
                }
            }
        },
        "measuring_quantity": {
            "description": "The type of measurement that the sensor is capable of taking.",
            "type": "object",
            "required": [
                "type",
                "unit"
            ],
            "properties": {
                "type": {
                    "type": "string",
                    "enum": [
                        "temperature"
                    ]
                },
                "unit": {
                    "description": "SI unit.",
                    "type": "string"
                }
            }
        },
        "independent_variable": {
            "description": "The chosen variable to make the measurements as a function of.",
            "type": "object",
            "required": [
                "type",
                "unit"
            ],
            "properties": {
                "type": {
                    "type": "string",
                    "enum": [
                        "time"
                    ]
                },
                "unit": {
                    "description": "SI unit.",
                    "type": "string"
                }
            }
        }
    }
}

# Define the data to validate
data = {
    "sensor_id": "sensor-001",
    "package_id": "package-001",
    "position": {
        "location": [0, 1, 0]
    },
    "measuring_quantity" :       {
        "type": "temperature"
#        "unit": "K"
      },
    "independent_variable":       {
        "type": "time",
        "unit": "s"
      }
  }

# Validate the data, should throw error about missing unit, if no error it means data follows the schema
jsonschema.validate(instance=data, schema=schema)