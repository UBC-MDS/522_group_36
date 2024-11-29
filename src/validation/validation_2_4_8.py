import pandera as pa
from pandera import Column, Check, DataFrameSchema
import numpy as np

def column_name_validation() -> DataFrameSchema:
    schema = pa.DataFrameSchema(
        {
            "trip_distance": pa.Column(
                                float,
                                pa.Check(
                                    lambda s: s > 0,
                                    error="Invalid value for 'trip_distance': must be greater than 0."
                                    ),
                                nullable=False
                            ),
            "fare_amount": pa.Column(
                                float,
                                pa.Check(
                                    lambda s: s > 0,
                                    error="Invalid value for 'fare_amount': must be greater than 0."
                                    ), 
                                nullable=False
                            )
        },
         checks=[
            Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found."),
            Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows found."),
        ]
    )
    return schema  

def threhold_validation() -> DataFrameSchema:  
    schema = pa.DataFrameSchema(
        {
            "fare_amount": pa.Column(float, 
                                pa.Check(lambda s: s.isna().mean() <=0.01, 
                                    element_wise=False, 
                                    error="Too many null values in 'fare_amount' column."), 
                                nullable=True)
        },
        checks=[
            Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found."),
            Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows found."),
        ]
    )
    return schema

def category_level_validation() -> DataFrameSchema:
    schema = pa.DataFrameSchema(
        {
            "VendorID":
                pa.Column(
                    int,
                    pa.Check.isin([1,2],
                                  error="Invalid value for 'VendorID': must be 1 or 2."),
                    nullable=False,
                ),
            "RatecodeID":
                pa.Column(
                    float,
                    pa.Check.isin([1.0,2.0,3.0,4.0,5.0],
                                  error="Invalid value for 'RatecodeID': must be one of [1.0, 2.0, 3.0, 4.0, 5.0]."),
                    nullable=False,
                ),
            "Store_and_fwd_flag":
                pa.Column(
                    object,
                    pa.Check.isin(['N','Y'],
                                  error="Invalid value for 'Store_and_fwd_flag': must be 'N' or 'Y'."),
                    nullable=True,
                ),
            "Payment_type":
                pa.Column(
                    int,
                    pa.Check.isin([2, 0, 1, 4, 3],
                                  error="Invalid value for 'Payment_type': must be one of [0, 1, 2, 3, 4]."),
                    nullable=False
                )
        },
         checks=[
            Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found."),
            Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows found."),
        ]
    )
    return schema