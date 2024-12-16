import logging
import pandas as pd
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import FeatureLabelCorrelation, FeatureFeatureCorrelation

class CorrelationValidator:
    def __init__(self, target: str, feature_threshold: float = 0.9, feature_feature_threshold: float = 0.8,
                 log_file: str = None):
        self.target = target
        self.feature_threshold = feature_threshold
        self.feature_feature_threshold = feature_feature_threshold
       
    
    def check_feature_label_correlation(self, df: pd.DataFrame):
        dataset = Dataset(df, label=self.target)
        check = FeatureLabelCorrelation().add_condition_feature_pps_less_than(self.feature_threshold)
        result = check.run(dataset)
        if not result.passed_conditions():
            logging.error("Feature-Label correlation exceeds the threshold.")
            raise ValueError("Feature-Label correlation exceeds the maximum acceptable threshold.")
        else:
            logging.info("Feature-Label correlation is within the acceptable threshold.")
    
    def check_feature_feature_correlation(self, df: pd.DataFrame):
        dataset = Dataset(df, label=self.target)
        check = FeatureFeatureCorrelation().add_condition_pps_less_than(self.feature_feature_threshold)
        result = check.run(dataset)
        
        if not result.passed_conditions():
            logging.error("Feature-Feature correlation exceeds the threshold.")
            raise ValueError("Feature-Feature correlation exceeds the maximum acceptable threshold.")
        else:
            logging.info("Feature-Feature correlation is within the acceptable threshold.")
    
    def run_all_checks(self, df: pd.DataFrame):
        self.check_feature_label_correlation(df)
        self.check_feature_feature_correlation(df)
