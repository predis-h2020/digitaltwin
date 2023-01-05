import os
import sys
from pathlib import Path

import pandas as pd
import numpy as np
import csv

# from doit import create_after
# from doit.task import clean_targets

# from digitaltwin.virtual_data_generation.create_virtual_sensor_data import create_virtual_sensor_data

DOIT_CONFIG = {"verbosity": 2}
PYTHON_EXE = sys.executable

# root is the top level of the repo
root_dir = Path(__file__).parents[2]

# if package_code is changed, rerun the complete repo
package_code = list((root_dir / "digitalwin").glob("**/*.py"))

# example directory
example_dir = os.path.dirname(Path(__file__))

# extract create virtual data for temperature sensor 1
def create_virtual_sensor_data(
    metadata, raw_data, metadata_csv, raw_data_csv, combined_data_csv, raw_data_xlxs
):
    # write csv file with all the meta data
    with open(metadata_csv, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(metadata.items())

    # write sensor values to csv file
    raw_data.to_csv(raw_data_csv)

    # write csv file with all the meta data and raw data
    with open(combined_data_csv, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(metadata.items())
        writer.writerows(" ")
    raw_data.to_csv(combined_data_csv, mode='a', index=False, header=True)

    # write sensor values to excel
    raw_data.to_excel(raw_data_xlxs, sheet_name="sheet1", index=False)


def task_create_virtual_temperature_sensor():
    sensor_name = "temperature_sensor"
    sensor_testdata_dir = Path(example_dir, sensor_name)
    sensor_testdata_dir.mkdir(parents=True, exist_ok=True)

    metadata_csv = Path(sensor_testdata_dir, "metadata.csv")
    raw_data_csv = Path(sensor_testdata_dir, "raw_data.csv")
    combined_data_csv = Path(sensor_testdata_dir, "combined_data.csv")
    raw_data_xlxs = Path(sensor_testdata_dir, "raw_data.xlxs")

    return {
        "file_dep": package_code,
        "actions": [
            (
                create_virtual_sensor_data,
                [],
                {
                    "metadata": {
                        "measuring quantity": "temperature",
                        "unit": "K",
                        "package": "test_package",
                        "location": [0, 0, 0],
                    },
                    "raw_data": pd.DataFrame(
                        data={
                            "time": np.linspace(start=0, stop=10, num=50),
                            "temperature": np.linspace(start=20, stop=100, num=50),
                        }
                    ),
                    "metadata_csv": metadata_csv,
                    "raw_data_csv": raw_data_csv,
                    "combined_data_csv": combined_data_csv,
                    "raw_data_xlxs": raw_data_xlxs,
                },
            )
        ],
        "targets" : [metadata_csv, raw_data_csv, raw_data_xlxs],
        "verbosity": 2,
    }


def task_create_virtual_displacement_sensor():
    sensor_name = "displacement_sensor"
    sensor_testdata_dir = Path(example_dir, sensor_name)
    sensor_testdata_dir.mkdir(parents=True, exist_ok=True)

    metadata_csv = Path(sensor_testdata_dir, "metadata.csv")
    raw_data_csv = Path(sensor_testdata_dir, "raw_data.csv")
    combined_data_csv = Path(sensor_testdata_dir, "combined_data.csv")
    raw_data_xlxs = Path(sensor_testdata_dir, "raw_data.xlxs")

    return {
        "file_dep": package_code,
        "actions": [
            (
                create_virtual_sensor_data,
                [],
                {
                    "metadata": {
                        "measuring quantity": "displacement",
                        "unit": "m",
                        "package": "test_package2",
                        "location": [0, 0, 0],
                        "orientation": [1,0,0]
                    },
                    "raw_data": pd.DataFrame(
                        data={
                            "time": np.linspace(start=2, stop=10, num=20),
                            "displacement": np.linspace(start=11.3, stop=12.5, num=20),
                        }
                    ),
                    "metadata_csv": metadata_csv,
                    "raw_data_csv": raw_data_csv,
                    "combined_data_csv": combined_data_csv,
                    "raw_data_xlxs": raw_data_xlxs,
                },
            )
        ],
        "targets" : [metadata_csv, raw_data_csv, raw_data_xlxs],
        "verbosity": 2,
    }
