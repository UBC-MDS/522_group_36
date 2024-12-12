import pytest
import pandas as pd
import os
from scripts.run_eda import TaxiDataAnalyzer, cli

@pytest.fixture
def test_data():
    """
    Fixture providing test data based on real taxi records.
    Features:
    - 20 records for better statistical analysis
    - Representative payment type distribution (80/20 split)
    - Mix of RatecodeIDs (standard and special rates)
    - Range of trip distances (short to long)
    - Strategic null values for testing missing data handling
    - Varied tip amounts and total fares
    - Mix of vendor IDs
    """
    return {
        'VendorID': [2, 1, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
        
        'tpep_pickup_datetime': [
            '2024-01-30 17:40:12', '2024-01-29 12:25:03', '2024-01-25 16:21:38',
            '2024-01-27 20:06:28', '2024-01-24 09:47:54', '2024-01-25 10:23:46',
            '2024-01-13 02:23:38', '2024-01-17 19:43:02', '2024-01-28 01:17:19',
            '2024-01-12 13:12:14', '2024-01-07 16:38:29', '2024-01-04 03:07:19',
            '2024-01-20 00:42:39', '2024-01-28 18:02:17', '2024-01-30 23:12:35',
            '2024-01-27 09:22:56', '2024-01-14 15:13:11', '2024-01-11 11:26:25',
            '2024-01-13 13:21:21', '2024-01-18 18:45:35'
        ],
        
        'tpep_dropoff_datetime': [
            '2024-01-30 17:47:05', '2024-01-29 12:53:32', '2024-01-25 16:36:41',
            '2024-01-27 20:41:05', '2024-01-24 10:03:31', '2024-01-25 10:33:32',
            '2024-01-13 02:33:36', '2024-01-17 20:01:45', '2024-01-28 01:32:01',
            '2024-01-12 13:19:04', '2024-01-07 16:43:49', '2024-01-04 03:50:42',
            '2024-01-20 00:50:56', '2024-01-28 18:12:33', '2024-01-30 23:31:49',
            '2024-01-27 09:34:55', '2024-01-14 15:32:24', '2024-01-11 11:33:47',
            '2024-01-13 14:04:33', '2024-01-18 19:00:10'
        ],
        
        'passenger_count': [2.0, 1.0, 1.0, 1.0, 1.0, None, 1.0, 1.0, 1.0, 1.0,
                          1.0, 4.0, 2.0, 2.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0],
        
        'trip_distance': [0.78, 7.21, 2.21, 4.85, 1.4, 1.02, 1.37, 2.42, 1.6, 0.9,
                         1.2, 16.59, 1.48, 1.28, 8.94, 2.83, 2.36, 0.74, 18.93, 2.2],
        
        'RatecodeID': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                       1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, None, 2.0, 2.0],
        
        'store_and_fwd_flag': ['N', 'N', 'N', 'N', 'N', None, 'N', 'N', 'N', 'N',
                              'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],
        
        'PULocationID': [230, 236, 211, 68, 161, 142, 107, 161, 4, 141,
                        114, 132, 79, 186, 70, 164, 43, 162, 132, 163],
        
        'DOLocationID': [186, 211, 68, 236, 186, 163, 211, 141, 231, 263,
                        186, 17, 186, 107, 163, 231, 164, 163, 114, 263],
        
        'payment_type': [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2],
        
        'fare_amount': [7.9, 34.73, 15.6, 32.4, 14.2, 10.0, 10.7, 17.7, 12.8, 7.9,
                       7.9, 74.4, 10.0, 10.7, 35.9, 14.9, 18.4, 8.6, 70.0, 15.6],
        
        'extra': [2.5, 0.0, 2.5, 1.0, 0.0, 0.0, 1.0, 2.5, 3.5, 2.5,
                 5.0, 1.0, 1.0, 0.0, 6.0, 0.0, 0.0, 0.0, 0.0, 5.0],
        
        'mta_tax': [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                    0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        
        'tip_amount': [0.0, 0.0, 4.42, 3.74, 3.64, 2.8, 8.0, 4.84, 3.55, 2.4,
                      1.0, 0.0, 1.95, 2.94, 10.92, 0.0, 4.48, 1.89, 15.15, 4.4],
        
        'tolls_amount': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0, 6.94, 0.0, 0.0, 0.0, 0.0, 0.0],
        
        'improvement_surcharge': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                                1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        
        'total_amount': [14.4, 38.73, 26.52, 41.14, 21.84, 16.8, 23.7, 29.04, 21.35, 14.3,
                        15.4, 78.65, 16.95, 17.64, 65.51, 18.9, 26.88, 14.49, 90.9, 26.5],
        
        'congestion_surcharge': [2.5, None, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5,
                                2.5, 0.0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
        
        'Airport_fee': [0.0, None, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1.75, 0.0, 0.0, 1.75, 0.0, 0.0, 0.0, 1.75, 0.0]
    }


@pytest.fixture
def test_csv(tmp_path, test_data):
    """Fixture creating a temporary CSV file with test data"""
    test_csv_path = os.path.join(tmp_path, "test_taxi_data.csv")
    pd.DataFrame(test_data).to_csv(test_csv_path, index=False)
    return test_csv_path

@pytest.fixture
def analyzer(test_csv, tmp_path):
    """Fixture providing initialized TaxiDataAnalyzer"""
    test_charts_dir = os.path.join(tmp_path, "test_charts")
    analyzer = TaxiDataAnalyzer(test_csv, charts_dir=test_charts_dir)
    analyzer.load_data()
    return analyzer

chart_output_format = 'png'

def test_data_loading_success(analyzer, test_data):
    """Test that data is loaded correctly"""
    assert analyzer.df is not None
    expected_columns = list(test_data.keys())
    assert all(col in analyzer.df.columns for col in expected_columns)

def test_data_loading_missing_file(tmp_path):
    """Test handling of non-existent file"""
    nonexistent_file = os.path.join(tmp_path, "nonexistent.csv")
    analyzer = TaxiDataAnalyzer(nonexistent_file)
    analyzer.load_data()
    assert analyzer.df is None

def test_negative_fare_filtering(analyzer):
    """Test filtering of negative fares"""
    initial_count = len(analyzer.df)
    analyzer.filter_negative_fares()
    assert len(analyzer.df) == initial_count  # No negative fares in test data
    assert analyzer.df['fare_amount'].min() >= 0

def test_train_test_split(analyzer):
    """Test dataset splitting"""
    analyzer.split_dataset(test_size=0.5, random_state=42)
    assert len(analyzer.train_df) == 10
    assert len(analyzer.test_df) == 10

def test_split_file_creation(analyzer):
    """Test creation of split data files"""
    analyzer.split_dataset(test_size=0.5, random_state=42)
    split_files = ['X_train.csv', 'y_train.csv', 'X_test.csv', 'y_test.csv']
    for file in split_files:
        assert os.path.exists(os.path.join('data/processed', file))

def test_density_chart_creation(analyzer):
    """Test density chart creation"""
    analyzer.create_density_chart('fare_amount', 'Test_Density_Chart')
    assert os.path.exists(os.path.join(analyzer.charts_dir, f'Test_Density_Chart.{chart_output_format}'))

def test_correlation_plot_creation(analyzer):
    """Test correlation plot creation"""
    analyzer.split_dataset(test_size=0.5, random_state=42)
    analyzer.create_correlation_plot(subset='train')
    assert os.path.exists(os.path.join(analyzer.charts_dir, 
                                     f'Correlation_Plot_Train_Spearman.{chart_output_format}'))

def test_missing_values_visualization(analyzer):
    """Test missing values visualization"""
    analyzer.split_dataset(test_size=0.5, random_state=42)
    analyzer.visualize_missing_values(subset='train')
    assert os.path.exists(os.path.join(analyzer.charts_dir, 
                                     f'Missing_Values_Heatmap_Train.{chart_output_format}'))

def test_schema_validation(analyzer):
    """Test data schema validation"""
    analyzer.split_dataset(test_size=0.5, random_state=42)
    analyzer.validate_data_schema(subset='train')  # Should not raise exceptions

def test_display_summary_statistics(analyzer):
    """
    Test the display_summary_statistics function for:
    1. Correct subset selection
    2. Return value type
    3. Invalid inputs
    4. Missing data handling
    """
    # Setup
    analyzer.split_dataset(test_size=0.5, random_state=42)
    
    # Test train subset
    train_stats = analyzer.display_summary_statistics(subset="train")
    assert isinstance(train_stats, pd.DataFrame), "Should return a DataFrame"
    assert train_stats.shape[1] == 16, "Number of rows should match number of numeric columns in original data"
    
    # Test test subset
    test_stats = analyzer.display_summary_statistics(subset="test")
    assert isinstance(test_stats, pd.DataFrame)
    assert test_stats.shape[1] == 16, "Number of rows should match number of numeric columns in original data"
    
    # Test all data
    all_stats = analyzer.display_summary_statistics(subset="all")
    assert isinstance(all_stats, pd.DataFrame)
    assert all_stats.shape[1] == 16, "Number of rows should match number of numeric columns in original data"
    
    # Test invalid subset
    invalid_stats = analyzer.display_summary_statistics(subset="invalid")
    assert invalid_stats is None  # Should return None for invalid subset
    

