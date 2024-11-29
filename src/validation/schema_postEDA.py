import pandera as pa
from pandera import Column, Check, DataFrameSchema
import numpy as np

def get_taxi_postEDA_data_schema() -> DataFrameSchema:
    schema = pa.DataFrameSchema(
        {
            "trip_distance": pa.Column(
                float,
                checks=Check.ge(0, element_wise=True),
                nullable=False,
                description="Elapsed trip distance in miles reported by the taximeter.",
            ),
            "fare_amount": pa.Column(
                float,
                checks=Check.ge(0, element_wise=True),
                nullable=False,
                description="Fare amount in USD.",
            )
        },
        checks=[
            Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found."),
            Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows found."),
        ]
    )
    return schema
