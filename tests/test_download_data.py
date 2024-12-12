import pytest
import pandas as pd
import os
from scripts.download_data import download_and_save_data

def test_download_and_save_data(tmp_path):
    """
    Test that verifies:
    1. File is created and not empty
    2. DataFrame has exactly 5 rows
    3. Contains all expected columns from NYC taxi dataset
    """
    # Test parameters
    test_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
    test_output = os.path.join(tmp_path, "test_output.csv")
    test_sample_size = 5
    
    # Expected columns for NYC taxi dataset
    expected_columns =[
        'VendorID',
        'tpep_pickup_datetime',
        'tpep_dropoff_datetime',
        'passenger_count',
        'trip_distance',
        'RatecodeID',
        'store_and_fwd_flag',
        'PULocationID',
        'DOLocationID', 
        'payment_type',
        'fare_amount',
        'extra',
        'mta_tax',
        'tip_amount',
        'tolls_amount',
        'improvement_surcharge',
        'total_amount',
        'congestion_surcharge',
        'Airport_fee'    
    ]
    
    
    # Run the function
    download_and_save_data(test_url, test_output, sample_size=test_sample_size)
    
    # Basic file checks
    assert os.path.exists(test_output), "CSV file was not created"
    assert os.path.getsize(test_output) > 0, "CSV file is empty"
    
    # Read the CSV to check contents
    df = pd.read_csv(test_output)
    
    # Check number of rows
    assert len(df) == test_sample_size, f"Expected {test_sample_size} rows, but got {len(df)} rows"
    
    # Check all expected columns are present
    for column in expected_columns:
        assert column in df.columns, f"Expected column {column} not found in DataFrame"
            
   