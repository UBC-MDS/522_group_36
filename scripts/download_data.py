import pandas as pd
import numpy as np
import click

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

@click.command()
@click.option('--data-set-link', '-d', 
              default="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet",
              help='URL or file path to the parquet dataset')
@click.option('--output-csv', '-o', 
              default='data/yellow_tripdata_2024-01.csv',
              help='File path where the CSV will be saved')
@click.option('--sample-size', '-n', 
              default=30000, 
              help='Number of rows to sample')
@click.option('--random-state', '-r', 
              default=123, 
              help='Seed for random sampling')
def main(data_set_link, output_csv, sample_size, random_state):
    """Download and sample data from a parquet file and save to CSV."""
    download_and_save_data(data_set_link, output_csv, sample_size, random_state)

if __name__ == "__main__":
    main()