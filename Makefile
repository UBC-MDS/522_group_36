# Makefile
# Lixuan Lin, Dec 2024

# This driver script completes the textual analysis of
# 3 novels and creates figures on the 10 most frequently
# occuring words from each of the 3 novels. This script
# takes no arguments.

# example usage:
# make all

.PHONY: all clean fig

all : report/count_report.html

# download data
data/raw/yellow_tripdata_2024-01.csv : 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet' scripts/download_data.py
	python scripts/download_data.py \
		--input_file='https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet' \
		--output_file=data/raw/yellow_tripdata_2024-01.csv

# data validation
data/processed/yellow_tripdata_2024-01_validated.csv : data/raw/yellow_tripdata_2024-01.csv scripts/run_validation.py
	python scripts/run_validation.py \
		--input_file=data/raw/yellow_tripdata_2024-01.csv \
		--output_file=data/processed/yellow_tripdata_2024-01_validated.csv

# eda
charts/Fare_Amount_Density_Chart.png: data/processed/yellow_tripdata_2024-01_validated.csv scripts/run_eda.py
	python scripts/run_eda.py \
		--input_file=data/processed/yellow_tripdata_2024-01_validated.csv \
		--output_file=charts/Fare_Amount_Density_Chart.png

charts/Missing_Values_Heatmap_Train.png: data/processed/yellow_tripdata_2024-01_validated.csv scripts/run_eda.py
	python scripts/run_eda.py \
		--input_file=data/processed/yellow_tripdata_2024-01_validated.csv \
		--output_file=charts/Missing_Values_Heatmap_Train.png

charts/Correlation_Plot_Train_Spearman.png: data/processed/yellow_tripdata_2024-01_validated.csv scripts/run_eda.py
	python scripts/run_eda.py \
		--input_file=data/processed/yellow_tripdata_2024-01_validated.csv \
		--output_file=charts/Correlation_Plot_Train_Spearman.png

# modeling
charts/Regression_Formula_Text.png: data/processed/X_train.csv scripts/modeling.py
	python scripts/modeling.py \
		--input_file=data/processed/X_train.csv \
		--output_file=charts/Regression_Formula_Text.png

charts/Regression_Performance_Metrics.png: data/processed/X_train.csv scripts/modeling.py
	python scripts/modeling.py \
		--input_file=data/processed/X_train.csv \
		--output_file=charts/Regression_Performance_Metrics.png

charts/Pred_Vs_Actual.png: data/processed/X_train.csv scripts/modeling.py
	python scripts/modeling.py \
		--input_file=data/processed/X_train.csv \
		--output_file=charts/Pred_Vs_Actual.png

charts/Final_Linear_Regression.png: data/processed/X_train.csv scripts/modeling.py
	python scripts/modeling.py \
		--input_file=data/processed/X_train.csv \
		--output_file=charts/Final_Linear_Regression.png

# write the report
report/count_report.html : report/count_report.qmd \
results/figure/isles.png \
results/figure/abyss.png \
results/figure/last.png \
results/figure/sierra.png
    quarto render report/count_report.qmd

clean :
    rm -f results/isles.dat \
        results/abyss.dat \
        results/last.dat \
        results/sierra.dat
    rm -f results/figure/isles.png \
        results/figure/abyss.png \
        results/figure/last.png \
        results/figure/sierra.png
    rm -rf report/count_report.html