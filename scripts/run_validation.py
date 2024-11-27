import sys
import yaml
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
    # Load configuration
    config_path = "config/validation_config.yaml"
    config = load_config(config_path)
    
    data_path = config.get("data_path", "src/data/raw/yellow_cab_data.csv")
    expected_format = config.get("expected_format", "csv")
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
        log_file="logs/validation_errors.log",
        correlation_log_file="logs/correlation_errors.log"
    )
    validator.correlation_validator.feature_threshold = feature_label_threshold
    validator.correlation_validator.feature_feature_threshold = feature_feature_threshold
    
    # Run the validation
    try:
        validated_df = validator.run_validation(
            file_path=data_path,
            expected_format=expected_format,
            delimiter=delimiter,
            expected_columns=expected_columns
        )
        print("Data validation passed successfully.")
    except ValueError as ve:
        print(f"Data validation failed: {ve}")
        sys.exit(1)
    
    # Save the validated data
    validated_data_path = "src/data/processed/yellow_cab_data_validated.csv"
    validated_df.to_csv(validated_data_path, index=False)
    print(f"Validated data saved to {validated_data_path}")

if __name__ == "__main__":
    main()
