# scripts/run_validation.py

import sys
import os
import yaml
import logging
from src.validation.validate import DataValidator

def load_config(config_path: str) -> dict:
    """
    Loads the YAML configuration file.

    :param config_path: Path to the YAML config file.
    :return: Configuration as a dictionary.
    """
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"Error loading config file: {e}")
        sys.exit(1)

def main():
    # Add the project root to sys.path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(project_root, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create .gitkeep file in logs directory
    gitkeep_path = os.path.join(logs_dir, ".gitkeep")
    if not os.path.exists(gitkeep_path):
        with open(gitkeep_path, 'w') as f:
            pass  # Create empty file

    # Configure logging
    logging.basicConfig(
        filename=os.path.join(logs_dir, "correlation_errors.log"),
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Load configuration
    config_path = os.path.join(project_root, "config", "validation_config.yaml")
    config = load_config(config_path)
    
    data_path = config.get("data_path", "data/raw/yellow_tripdata_2024-01.csv")
    delimiter = config.get("delimiter", ",")
    expected_columns = config.get("expected_columns", [
        "VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime",
        "passenger_count", "trip_distance", "RatecodeID",
        "store_and_fwd_flag", "PULocationID", "DOLocationID",
        "payment_type", "fare_amount", "extra", "mta_tax",
        "tip_amount", "tolls_amount", "improvement_surcharge",
        "total_amount", "congestion_surcharge", "Airport_fee"
    ])
    correlation_thresholds = config.get("correlation_thresholds", {})
    feature_label_threshold = correlation_thresholds.get("feature_label", 0.9)
    feature_feature_threshold = correlation_thresholds.get("feature_feature", 0.8)
    
    # Initialize the DataValidator with dynamic thresholds
    validator = DataValidator(
        target="VendorID",  # Adjust target as needed
        log_file=os.path.join(project_root, "logs", "validation_errors.log"),
        correlation_log_file=os.path.join(project_root, "logs", "correlation_errors.log")
    )
    validator.correlation_validator.feature_threshold = feature_label_threshold
    validator.correlation_validator.feature_feature_threshold = feature_feature_threshold
    
    # Run the validation
    try:
        validated_df = validator.run_validation(
            file_path=data_path,
            expected_columns=expected_columns
        )
        print("Data validation passed successfully.")
    except ValueError as ve:
        print(f"Data validation failed: {ve}")
        sys.exit(1)
    
    # Save the validated data based on the file format
    file_extension = data_path.split(".")[-1].lower()
    if file_extension == "csv":
        validated_data_path = os.path.join(project_root, "data", "processed", "yellow_tripdata_2024-01_validated.csv")
        validated_df.to_csv(validated_data_path, index=False)
    elif file_extension == "parquet":
        validated_data_path = os.path.join(project_root, "data", "processed", "yellow_tripdata_2024-01_validated.parquet")
        validated_df.to_parquet(validated_data_path, engine='pyarrow', index=False)
    elif file_extension == "xlsx":
        validated_data_path = os.path.join(project_root, "data", "processed", "yellow_tripdata_2024-01_validated.xlsx")
        validated_df.to_excel(validated_data_path, engine='openpyxl', index=False)
    else:
        # This case should not occur due to prior checks
        validated_data_path = os.path.join(project_root, "data", "processed", "yellow_tripdata_2024-01_validated.csv")
        validated_df.to_csv(validated_data_path, index=False)
    
    print(f"Validated data saved to {validated_data_path}")

if __name__ == "__main__":
    main()
