import numpy as np
import pytest
from digitaltwin.virtual_data_generation.create_virtual_sensor_data import create_virtual_sensor_data

def test_metadata():
    """Testing the correct extraction of metadata
    """

    result = create_virtual_sensor_data()

    assert result["sensor_1"]["meta_data"]["unit"] == "K"