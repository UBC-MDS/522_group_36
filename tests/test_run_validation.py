import os
import sys
import pytest
import yaml
from unittest.mock import patch
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts.run_validation import load_config, main
from click.testing import CliRunner

@pytest.fixture
def config_data():
    """
    Mock config data
    """
    return {
        "data_path": "data/raw/yellow_tripdata_2024-01.csv",
        "delimiter": ",",
        "expected_columns": [
            "VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime",
            "passenger_count", "trip_distance", "RatecodeID",
            "store_and_fwd_flag", "PULocationID", "DOLocationID",
            "payment_type", "fare_amount", "extra", "mta_tax",
            "tip_amount", "tolls_amount", "improvement_surcharge",
            "total_amount", "congestion_surcharge", "Airport_fee"
        ],
        "correlation_thresholds": {
            "feature_label": 0.9,
            "feature_feature": 0.8
        }
    }

@pytest.fixture
def temp_config_file(tmp_path, config_data):
    """
    Create a temporary config file.
    """
    config_file = tmp_path / "validation_config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(config_data, f)
    return config_file

def test_load_config_success(temp_config_file):
    """
    Test loading a YAML config file.
    """
    config = load_config(temp_config_file)
    assert isinstance(config, dict), "Config should be a dictionary."
    assert "data_path" in config, "'data_path' should be present in the config."
    assert config["data_path"] == "data/raw/yellow_tripdata_2024-01.csv", "The data path should match."

def test_load_config_failure():
    """
    Test loading an invalid YAML config file.
    """
    with pytest.raises(SystemExit):
        load_config("non_existent_config.yaml")