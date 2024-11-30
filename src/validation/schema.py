import pandera as pa
from pandera import Column, Check, DataFrameSchema
import numpy as np


def get_taxi_data_schema() -> DataFrameSchema:
    schema = DataFrameSchema(
        {
            "VendorID": Column(
                pa.Int,
                checks=Check.isin([1, 2]),
                nullable=False,
                description="Provider associated with the trip.",
            ),
            "tpep_pickup_datetime": Column(
                pa.DateTime,
                nullable=False,
                description="Date and time when the meter was engaged.",
            ),
            "tpep_dropoff_datetime": Column(
                pa.DateTime,
                nullable=False,
                description="Date and time when the meter was disengaged.",
            ),
            "passenger_count": Column(
                pa.Float,
                checks=[
                    Check.ge(
                        0, element_wise=True
                    ),  # Passenger count should be non-negative
                    Check.le(
                        6, element_wise=True
                    ),  # Assuming a reasonable max passenger count
                ],
                nullable=True,
                description="Number of passengers in the vehicle.",
            ),
            "trip_distance": Column(
                pa.Float,
                checks=Check.ge(0, element_wise=True),
                nullable=False,
                description="Elapsed trip distance in miles reported by the taximeter.",
            ),
            "RatecodeID": Column(
                pa.Float,
                checks=Check.isin([1.0, 2.0, 3.0, 4.0, 5.0]),
                nullable=True,
                description="Rate code in effect at the time of the trip.",
            ),
            "store_and_fwd_flag": Column(
                pa.String,
                checks=Check.isin(["Y", "N"]),
                nullable=True,
                description="Store and forward flag indicates whether the trip record was held in vehicle memory before sending to the vendor.",
            ),
            "PULocationID": Column(
                pa.Int,
                checks=Check.ge(
                    1, element_wise=True
                ),  # Location IDs are positive integers
                nullable=False,
                description="A unique identifier for the pickup location.",
            ),
            "DOLocationID": Column(
                pa.Int,
                checks=Check.ge(1, element_wise=True),
                nullable=False,
                description="A unique identifier for the drop-off location.",
            ),
            "payment_type": Column(
                pa.Int,
                checks=Check.isin([1, 2, 3, 4, 5, 6, 7]),
                nullable=False,
                description="Payment method: 1=Credit card, 2=Cash, etc.",
            ),
            # "fare_amount": Column(
            #     pa.Float,
            #     checks=Check.ge(0, element_wise=True),
            #     nullable=False,
            #     description="Fare amount in USD.",
            # ),
            "extra": Column(
                pa.Float,
                checks=Check.ge(0, element_wise=True),
                nullable=False,
                description="Extra fees in USD.",
            ),
            "mta_tax": Column(
                pa.Float,
                checks=Check.ge(0, element_wise=True),
                nullable=False,
                description="MTA tax in USD.",
            ),
            "tip_amount": Column(
                pa.Float,
                checks=Check.ge(0, element_wise=True),
                nullable=False,
                description="Tip amount in USD.",
            ),
            "fare_amount": Column(
                pa.Float,
                checks=[
                    Check.ge(0, element_wise=True),
                    Check(lambda s: s.isna().mean() <= 0.01, 
                         element_wise=False,
                         error="Too many null values (>1%) in fare_amount column.")
                ],
                nullable=False,
                description="Fare amount in USD.",
            ),
            "tolls_amount": Column(
                pa.Float,
                checks=Check.ge(0, element_wise=True),
                nullable=False,
                description="Tolls amount in USD.",
            ),
            "improvement_surcharge": Column(
                pa.Float,
                checks=Check.ge(0, element_wise=True),
                nullable=False,
                description="Improvement surcharge in USD.",
            ),
            "total_amount": Column(
                pa.Float,
                checks=Check.ge(0, element_wise=True),
                nullable=False,
                description="Total amount charged to the passenger in USD.",  # TODO: check for non negative values
            ),
            "congestion_surcharge": Column(
                pa.Float,
                checks=Check.ge(0, element_wise=True),
                nullable=True,
                description="Congestion surcharge in USD.",
            ),
            "Airport_fee": Column(
                pa.Float,
                checks=Check.ge(0, element_wise=True),
                nullable=True,
                description="Airport fee in USD.",
            ),
        },
        checks=[
            # Check for duplicate rows
            Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found."),
            # Check for empty rows
            Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows found."),
            # Logical checks: pickup datetime should be before dropoff datetime
            Check(
                lambda df: df["tpep_pickup_datetime"] <= df["tpep_dropoff_datetime"],
                error="Pickup datetime occurs after dropoff datetime.",
            ),
        ],
        coerce=True,  # Automatically convert data types if possible
        strict=False,  # Allow unexpected columns, adjust as needed
    )
    return schema
