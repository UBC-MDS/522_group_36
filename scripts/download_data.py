import pandas as pd
import numpy as np

def download_and_save_data(data_set_link, output_csv, sample_size=30000, random_state=123):
    df = pd.read_parquet(data_set_link).sample(sample_size, random_state=random_state)
    df.to_csv(output_csv, index=False)
    print(f"Data saved to {output_csv}")
    print(f"Data shape: {df.shape}")
    print(df.head(2))

if __name__ == "__main__":
    data_set_link = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
    output_csv = 'data/yellow_tripdata_2024-01.csv'
    download_and_save_data(data_set_link, output_csv)