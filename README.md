# NYC Yellow Taxi Fare Predictor 🚕

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/docker-publish.yml)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC_BY--NC--ND_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)




## About

This project predicts NYC yellow taxi fare prices based on trip distance. Analyzing 30,000 NYC yellow taxi trips in January 2024, we used a simple linear regression model where trip distance predicts fare price. The resulting model predicts that each additional mile travelled is associated with a $3.62 increase in the fare price. The model performed decently well - the $R^2$ value was 0.848. This means that 84.8% of the variance in the fare prices was explained by trip distance. This model could be useful for NYC taxi customers who know how long their taxi trip is going to be - they can use our model to predict their taxi fare price.

## Report

The final report can be found [here](https://UBC-MDS.github.io/DSCI_522_Group36_taxi_fare_predictor/).

## Usage

## Option 1: Using Docker With Manual Build

### Setup

> If you are using Windows or Mac, make sure Docker Desktop is running.

### Running the Analysis

1. **Clone the repository and navigate to the root of this project**:
    ```
    git clone https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor.git
    
    cd DSCI_522_Group36_taxi_fare_predictor
    ```
    
2. **Run the container using the command line**
    ``` 
    docker compose up
    ```
    \* We are doing a port mapping here. To run the docker-compose, make sure your 8888 port is free. 

    If you are testing this out locally, you can also build the Docker image locally by running the following commands: 
    ```
    docker build -t taxi-fare-predictor .

    docker run --rm -it -p 8888:8888 -v "$(pwd):/home/jovyan/work" taxi-fare-predictor
    ```
    Make sure current working directory is the root of this project.

3. **Copy and paste the URL into your browser**
   
   In the terminal, look for a URL that starts with 
    `http://127.0.0.1:8888/lab?token=` 

4. **Prepare the data**

   To run this analysis pipeline, open a terminal and run the following commands:
   
   ```
   python -m scripts.download_data
   ```
    
5. **Run data validation**

    ```
    python -m scripts.run_validation
    ```
    
    This script will check if the data is valid and print out the result. If the data is valid, it will print out "Data validation passed successfully". If the data is invalid, it will log the error messages in logs and remove those rows. The validated data will be saved in data/processed. In this testing, we only removed 2000 rows after validation which are data that is outside of the NYC taxi data [documentation](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf) range.

6. **Run the eda analysis**
   
    ```
    python -m scripts.run_eda run-all data/processed/yellow_tripdata_2024-01_validated.csv --charts_dir charts
    ```

7. **Run the model**

   ```
   python -m scripts.modeling --x-train-path data/processed/X_train.csv --y-train-path data/processed/y_train.csv --x-test-path data/processed/X_test.csv --y-test-path data/processed/y_test.csv
   ```

8. **Render Quarto**

   To render the Quarto document to HTML and PDF:

   ```
   quarto render report/yellow_taxi_analysis.qmd --to html
   quarto render report/yellow_taxi_analysis.qmd --to pdf
   ``` 
### Clean up

To shut down the container and clean up the resources, type `Cntrl` + `C` in the 
terminal where you launched the container, and then type `docker compose rm`


## Option 2: Docker Build With Make

1. To replicate the analysis, clone this GitHub repository, then run the following command at the command line/terminal 
from the root directory of this project:

    ```
    docker compose up 
    ```

In the terminal, look for a URL that starts with 
    `http://127.0.0.1:8888/lab?token=`

2. After Docker builds and launches the container with Jupyter Lab. Run this command in the Jupyter Terminal. 

    ```
    make all
    ```

3. To reset the repo to a clean state, with no intermediate or results
files, run the following command at the command line/terminal from the
root directory of this project:

    ```
    make clean
    ```

## Developer notes

### Developer dependencies
- `conda` (version 23.9.0 or higher)
- `conda-lock` (version 2.5.7 or higher)

Additional dependencies are specified in the [`Dockerfile`](Dockerfile) and [`environment.yml`](environment.yml).

### Adding a new dependency

1. Add the dependency to the `environment.yml` file on a new branch.

2. Run `conda-lock -k explicit --file environment.yml -p linux-64` to update the `conda-linux-64.lock` file.

2. Re-build the Docker image locally to ensure it builds and runs properly.

3. Push the changes to GitHub. A new Docker
   image will be built and pushed to Docker Hub automatically.
   It will be tagged with the SHA for the commit that changed the file.

4. Send a pull request to merge the changes into the `main` branch. 

## Contributors

- **Jam Lin**
- **Jiayi Li**
- **Han Wang**
- **Yibin Long**

## License

This project is licensed under the MIT license for the project code and the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0) license for the project report - see the LICENSE file for more details.

## References

Charles R Harris, K Jarrod Millman, Stéfan J van der Walt, Ralf Gommers, Pauli Virtanen, David Cournapeau, Eric Wieser, Julian Taylor, Sebastian Berg, Nathaniel J Smith, Robert Kern, Matti Picus, Stephan Hoyer, Marten H van Kerkwijk, Matthew Brett, Allan Haldane, Jaime Fernández del Río, Mark Wiebe, Pearu Peterson, Pierre Gérard-Marchant, Kevin Sheppard, Tyler Reddy, Warren Weckesser, Hameer Abbasi, Christoph Gohlke, and Travis E Oliphant. Array programming with NumPy. Nature, 585(7825):357–362, 2020. URL: https://doi.org/10.1038/s41586-020-2649-2, doi:10.1038/s41586-020-2649-2.

F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot, and E. Duchesnay. Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12:2825–2830, 2011.

Jake VanderPlas. Altair: interactive statistical visualizations for python. Journal of open source software, 3(7825):1057, 2018. URL: https://doi.org/10.21105/joss.01057, doi:10.21105/joss.01057.

Guido Van Rossum and Fred L. Drake. Python 3 Reference Manual. CreateSpace, Scotts Valley, CA, 2009. ISBN 1441412697.

New York City Taxi and Limousine Commission. TLC Trip Record Data. Retrieved from https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page, 2024. Wes McKinney. Data structures for statistical computing in python. In Stéfan van der Walt and Jarrod Millman, editors, Proceedings of the 9th Python in Science Conference, =51 – 56. 2010.

Wes McKinney. Data structures for statistical computing in python. In Stéfan van der Walt and Jarrod Millman, editors, Proceedings of the 9th Python in Science Conference, =51 – 56. 2010.
