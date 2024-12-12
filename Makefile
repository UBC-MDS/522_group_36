# Makefile
# Lixuan Lin, Dec 2024

# This script completes the analysis of taxi fare predictor
# and builds a regression model to predict the taxi fare.
# This script takes no arguments.

# example usage:
# make all

.PHONY: all clean

all : report/yellow_taxi_analysis.html report/yellow_taxi_analysis.pdf

# download data
data/raw/yellow_tripdata_2024-01.csv : scripts/download_data.py
	python -m scripts.download_data

# data validation
data/processed/yellow_tripdata_2024-01_validated.csv : data/raw/yellow_tripdata_2024-01.csv scripts/run_validation.py
	python -m scripts.run_validation

# eda
charts/Fare_Amount_Density_Chart.png: data/processed/yellow_tripdata_2024-01_validated.csv scripts/run_eda.py
	python -m scripts.run_eda run-all data/processed/yellow_tripdata_2024-01_validated.csv \
		--charts_dir charts

charts/Missing_Values_Heatmap_Train.png: data/processed/yellow_tripdata_2024-01_validated.csv scripts/run_eda.py
	python -m scripts.run_eda run-all data/processed/yellow_tripdata_2024-01_validated.csv \
		--charts_dir charts

charts/Correlation_Plot_Train_Spearman.png: data/processed/yellow_tripdata_2024-01_validated.csv scripts/run_eda.py
	python -m scripts.run_eda run-all data/processed/yellow_tripdata_2024-01_validated.csv \
		--charts_dir charts

# modeling
charts/Regression_Formula_Text.png: data/processed/X_train.csv data/processed/y_train.csv data/processed/X_test.csv data/processed/y_test.csv scripts/modeling.py
	python scripts/modeling.py \
		--x-train-path data/processed/X_train.csv \
		--y-train-path data/processed/y_train.csv \
		--x-test-path data/processed/X_test.csv \
		--y-test-path data/processed/y_test.csv

charts/Regression_Performance_Metrics.png: data/processed/X_train.csv data/processed/y_train.csv data/processed/X_test.csv data/processed/y_test.csv scripts/modeling.py
	python scripts/modeling.py \
		--x-train-path data/processed/X_train.csv \
		--y-train-path data/processed/y_train.csv \
		--x-test-path data/processed/X_test.csv \
		--y-test-path data/processed/y_test.csv

charts/Pred_Vs_Actual.png: data/processed/X_train.csv data/processed/y_train.csv data/processed/X_test.csv data/processed/y_test.csv scripts/modeling.py
	python scripts/modeling.py \
		--x-train-path data/processed/X_train.csv \
		--y-train-path data/processed/y_train.csv \
		--x-test-path data/processed/X_test.csv \
		--y-test-path data/processed/y_test.csv

charts/Final_Linear_Regression.png: data/processed/X_train.csv data/processed/y_train.csv data/processed/X_test.csv data/processed/y_test.csv scripts/modeling.py
	python scripts/modeling.py \
		--x-train-path data/processed/X_train.csv \
		--y-train-path data/processed/y_train.csv \
		--x-test-path data/processed/X_test.csv \
		--y-test-path data/processed/y_test.csv

# write the report
report/yellow_taxi_analysis.html : report/yellow_taxi_analysis.qmd \
charts/Fare_Amount_Density_Chart.png \
charts/Missing_Values_Heatmap_Train.png \
charts/Correlation_Plot_Train_Spearman.png \
charts/Regression_Formula_Text.png \
charts/Regression_Performance_Metrics.png \
charts/Pred_Vs_Actual.png \
charts/Final_Linear_Regression.png
	quarto render report/yellow_taxi_analysis.qmd --to html
	quarto render report/yellow_taxi_analysis.qmd --to pdf

# example usage:
# make clean

clean :
	rm -f data/raw/yellow_tripdata_2024-01.csv \
		data/processed/yellow_tripdata_2024-01_validated.csv
	rm -f charts/Fare_Amount_Density_Chart.png \
		charts/Missing_Values_Heatmap_Train.png \
        charts/Correlation_Plot_Train_Spearman.png \
        charts/Regression_Formula_Text.png \
		charts/Regression_Performance_Metrics.png \
		charts/Pred_Vs_Actual.png \
		charts/Final_Linear_Regression.png
	rm -rf report/yellow-taxi-analysis.html \
		report/yellow-taxi-analysis.pdf