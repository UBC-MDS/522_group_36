import pandas as pd
import numpy as np

#temporarily run as python -m scripts.download_data

def download_and_save_data(data_set_link, output_csv, sample_size=30000, random_state=123):
    """Downloads and saves a sample from a parquet dataset to a CSV file.
    This function reads a parquet file from a provided URL, takes a random sample,
    and saves it as a CSV file. It also prints information about the saved data.
    Args:
        data_set_link (str): URL or file path to the parquet dataset.
        output_csv (str): File path where the CSV will be saved.
        sample_size (int, optional): Number of rows to sample. Defaults to 30000.
        random_state (int, optional): Seed for random sampling. Defaults to 123.
    Returns:
        None
    Prints:
        - Confirmation message with save location
        - Shape of the sampled dataset
        - First two rows of the dataset
    """
    
    df = pd.read_parquet(data_set_link).sample(sample_size, random_state=random_state)
    df.to_csv(output_csv, index=False)
    print(f"Data saved to {output_csv}")
    print(f"Data shape: {df.shape}")
    print(df.head(2))

if __name__ == "__main__":
    data_set_link = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
    output_csv = 'data/yellow_tripdata_2024-01.csv'
    download_and_save_data(data_set_link, output_csv)