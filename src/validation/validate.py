import logging
import json
import pandas as pd
import pandera as pa
from .schema import get_taxi_data_schema
from .correlation_validator import CorrelationValidator
import os

class DataValidator:
    ALLOWED_FORMATS = ["csv", "parquet", "xlsx"]
    
    def __init__(self, target: str, log_file: str = "logs/validation_errors.log", correlation_log_file: str = "logs/correlation_errors.log"):
        
        self.schema = get_taxi_data_schema()
        self.correlation_validator = CorrelationValidator(
            target=target, 
            log_file=correlation_log_file
        )
        
        # Configure logging for validation errors
        logging.basicConfig(
            filename=log_file,
            filemode="w",
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )
    
    def check_file_format(self, file_path: str) -> str:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower().lstrip(".")
        
        if ext not in self.ALLOWED_FORMATS:
            error_msg = f"Incorrect file format: Expected one of {self.ALLOWED_FORMATS}, got '{ext}'."
            logging.error(error_msg)
            raise ValueError(error_msg)
        else:
            logging.info(f"File format '{ext}' verified successfully.")
            return ext
    
    def load_data(self, file_path: str, file_format: str) -> pd.DataFrame:
        try:
            if file_format == "csv":
                df = pd.read_csv(file_path, delimiter=",", parse_dates=["tpep_pickup_datetime", "tpep_dropoff_datetime"])
            elif file_format == "parquet":
                df = pd.read_parquet(file_path, engine='pyarrow')  # Ensure pyarrow is installed
            elif file_format == "xlsx":
                df = pd.read_excel(file_path, engine='openpyxl', parse_dates=["tpep_pickup_datetime", "tpep_dropoff_datetime"])
            else:
                error_msg = f"Unsupported file format: {file_format}."
                logging.error(error_msg)
                raise ValueError(error_msg)
            logging.info(f"Data loaded successfully from '{file_path}'.")
            return df
        except Exception as e:
            error_msg = f"Error loading data from '{file_path}': {e}"
            logging.error(error_msg)
            raise ValueError(error_msg)
    
    def validate_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            # Validate schema
            validated_df = self.schema.validate(df, lazy=True)
            logging.info("Schema validation passed.")
            
            # Perform correlation checks
            self.correlation_validator.run_all_checks(validated_df)
            
            return validated_df
        except pa.errors.SchemaErrors as e:
            # Log all schema validation errors
            error_details = e.failure_cases.to_dict(orient="records")
            error_message = json.dumps(error_details, indent=2)
            logging.error(f"Schema validation failed with errors:\n{error_message}")
            
            # Drop invalid rows based on the error cases
            invalid_indices = e.failure_cases["index"].dropna().unique()
            validated_df = (
                df.drop(index=invalid_indices)
                .reset_index(drop=True)
                .drop_duplicates()
                .dropna(how="all")
            )
            logging.info("Invalid rows have been dropped from the dataframe.")
            return validated_df
        except ValueError as ve:
            # Log correlation validation errors
            logging.error(str(ve))
            # Depending on your use case, you can choose to either drop problematic rows,
            # raise an exception, or take other actions. Here, we'll re-raise the exception.
            raise
    
    def run_validation(self, file_path: str, expected_columns: list = None) -> pd.DataFrame:
        # Check file format
        file_format = self.check_file_format(file_path)
        
        # Load data based on file format
        df = self.load_data(file_path, file_format)
        
        # Validate DataFrame structure based on expected columns
        if expected_columns:
            missing_columns = set(expected_columns) - set(df.columns)
            if missing_columns:
                error_msg = f"Missing columns in data file: {missing_columns}"
                logging.error(error_msg)
                raise ValueError(error_msg)
            else:
                logging.info("All expected columns are present in the data file.")
        
        # Validate the DataFrame
        validated_df = self.validate_dataframe(df)
        
        return validated_df
