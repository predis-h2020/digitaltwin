import numpy as np


def create_virtual_sensor_data(output_dir=None):
    """
    Creates virtual sensor data
    param:
        output_dir: string
             The path where the files are to be stored, if empty, not files are stored
             This is not yet implemented
    :returns
        python_dictionary with the virtual time series data and metadata for each sensor
    """
    output_data = {}

    # add first sensor
    num_samples = 50  # number of time instances
    metadata_sensor_1 = {
        "measuring quantity": "temperature",
        "unit": "K",
        "package": "test_package",
        "location": [0, 0, 0],
    }

    raw_data_sensor_1 = {
        "time": np.linspace(start=0, stop=10, num=num_samples),
        "temperature": np.linspace(start=20, stop=100, num=num_samples),
    }

    output_data["sensor_1"] = {
        "raw_data": raw_data_sensor_1,
        "meta_data": metadata_sensor_1,
    }

    # add second sensor
    num_samples = 200  # number of time instances
    metadata_sensor_2 = {
        "measuring quantity": "displacement",
        "unit": "m",
        "package": "test_package",
        "orientation": [1, 0, 0],
        "location": [5, 5, 5],
    }

    raw_data_sensor_2 = {
        "time": np.linspace(start=1, stop=5, num=num_samples),
        "temperature": np.linspace(start=1e-3, stop=5e-3, num=num_samples),
    }

    output_data["sensor_2"] = {
        "raw_data": raw_data_sensor_1,
        "meta_data": metadata_sensor_1,
    }

    return output_data
