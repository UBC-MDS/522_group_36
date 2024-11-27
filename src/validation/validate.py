import json
import logging
import pandas as pd
import pandera as pa
from pandera import Check
from .correlation_validator import CorrelationValidator
import os

logging.basicConfig(
    filename="validation_errors.log",
    filemode="w",
    format="%(asctime)s - %(message)s",
    level=logging.INFO,
)

class DataValidator:
    def __init__(self, data):
        self.data = data


    
