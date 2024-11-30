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
3. **Copy and paste the URL into your browser**
   
   In the terminal, look for a URL that starts with 
    `http://127.0.0.1:8888/lab?token=` 

4. **Run the analysis**

    open `yellow_taxi_analysis.ipynb` in Jupyter Lab you just launched

5. **Restart the kernel and run all cells to see the analysis**

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
