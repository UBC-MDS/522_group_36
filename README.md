# NYC Yellow Taxi Fare Predictor 🚕

In this project we attempt to predict the fare price of yellow taxi trips in NYC using a simple linear regression model that uses trip distance as the independent variable and fare price as the dependent variable.

## Usage

### Setup

> If you are using Windows or Mac, make sure Docker Desktop is running.

### Running the analysis

1. **Clone the repository and navigate to the root of this project**:
    ```bash
    git clone https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor.git
    cd DSCI_522_Group36_taxi_fare_predictor
    ```
    
2. **Run the container using the command line**
    ``` 
    docker run --rm -it -p 9999:8888 lixuanlin/taxi-fare-predictor
    ```
    \* We are doing a port mapping here. Try docker run --rm -it -p 8888:8888 lixuanlin/taxi-fare-predictor if your port 8888 port is free. 

    If you are testing this out locally, you can also build the Docker image locally by running the following commands: 
    ```
    docker build -t taxi-fare-predictor .

    docker run --rm -it -p 8888:8888 -v "$(pwd):/home/jovyan/work" taxi-fare-predictor
    ```
    Make sure current working directory is the root of this project.

3. **Copy and paste the URL into your browser**
   
   In the terminal, look for a URL that starts with 
    `http://127.0.0.1:8888/lab?token=` 

    
4. **Run data validation**
    
    ```
    python scripts/run_validation.py
    ```
    This script will check if the data is valid and print out the result. If the data is valid, it will print out "Data is valid". If the data is invalid, it will log the error messages in logs.
5. **Run the analysis**

    open `yellow_taxi_analysis.ipynb` in Jupyter Lab you just launched

6. **Restart the kernel and run all cells to see the analysis**

   under the "Kernel" menu click "Restart Kernel and Run All Cells..."

### Clean up

1. To shut down the container and clean up the resources, type `Cntrl` + `C` in the terminal

## Developer notes

### Developer dependencies
- `conda` (version 23.9.0 or higher)
- `conda-lock` (version 2.5.7 or higher)

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

New York City Taxi and Limousine Commission. TLC Trip Record Data. Retrieved from https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page, 2024. Wes McKinney. Data structures for statistical computing in python. In Stéfan van der Walt and Jarrod Millman, editors, Proceedings of the 9th Python in Science Conference, =51 – 56. 2010.

Wes McKinney. Data structures for statistical computing in python. In Stéfan van der Walt and Jarrod Millman, editors, Proceedings of the 9th Python in Science Conference, =51 – 56. 2010.
