import os
import pandas as pd
import altair as alt
from sklearn.model_selection import train_test_split
import pandera as pa
from src.schema_postEDA import get_taxi_postEDA_data_schema
import click

# Enable VegaFusion for Altair
#alt.data_transformers.enable("vegafusion")

#temporarily run as python -m scripts.run_eda

class TaxiDataAnalyzer:
    def __init__(self, file_path, charts_dir="charts"):
        """
        Initialize the TaxiDataAnalyzer with the dataset file path and optional schema.

        Args:
            file_path (str): Path to the CSV dataset.
            schema (pa.DataFrameSchema, optional): Pandera schema for validation.
            charts_dir (str, optional): Directory to save all charts. Defaults to "charts".
        """
        self.file_path = file_path
        self.schema = get_taxi_postEDA_data_schema()
        self.charts_dir = charts_dir
        self.df = None
        self.train_df = None
        self.test_df = None
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

        # Ensure the charts directory exists
        os.makedirs(self.charts_dir, exist_ok=True)

    def load_data(self):
        """Load dataset from the specified file path."""
        try:
            self.df = pd.read_csv(self.file_path).drop_duplicates()
            click.echo(f"Data loaded successfully from {self.file_path}.")
        except FileNotFoundError:
            click.echo(f"File not found: {self.file_path}")
        except pd.errors.ParserError as e:
            click.echo(f"Error parsing CSV: {e}")

    def create_density_chart(self, column, title="Density Chart"):
        """
        Create and save a density chart for a given column.

        Args:
            column (str): The column name to plot.
            title (str, optional): Title of the chart. Defaults to "Density Chart".
        """
        if self.df is None:
            print("Data not loaded. Please load data before creating charts.")
            return

        chart = (
            alt.Chart(self.df)
            .transform_density(column, as_=[column, "density"])
            .mark_area()
            .encode(
                x=alt.X(column, title=column.capitalize()),
                y=alt.Y("density:Q", title="Density"),
            )
            .properties(title=title, width=600, height=400)
        )

        # Save the chart as SVG
        file_path = os.path.join(self.charts_dir, f"{title.replace(' ', '_')}.svg")
        chart.save(file_path)
        print(f"Density chart saved to {file_path}.")

    def filter_negative_fares(self):
        """Filter out rows with negative fare amounts."""
        if self.df is None:
            print("Data not loaded. Please load data before filtering.")
            return
        initial_count = len(self.df)
        self.df = self.df[self.df["fare_amount"] >= 0]
        filtered_count = len(self.df)
        print(
            f"Filtered out {initial_count - filtered_count} rows with negative fare amounts."
        )

    def split_dataset(self, test_size=0.3, random_state=123):
        if self.df is None:
            print("Data not loaded. Please load data before splitting.")
            return

        # Split the data
        self.train_df, self.test_df = train_test_split(
            self.df, test_size=test_size, random_state=random_state
        )
        
        # Store numpy arrays for modeling
        self.X_train = self.train_df["trip_distance"].values.reshape(-1, 1)
        self.y_train = self.train_df["fare_amount"].values
        self.X_test = self.test_df["trip_distance"].values.reshape(-1, 1)
        self.y_test = self.test_df["fare_amount"].values
        
        print(f"Dataset split into {len(self.train_df)} training and {len(self.test_df)} test samples.")
        
        # Save split data directly from DataFrames
        processed_dir = "data/processed"
        os.makedirs(processed_dir, exist_ok=True)
        
        # Save only the required columns from the original DataFrames
        self.train_df[["trip_distance"]].to_csv(os.path.join(processed_dir, "X_train.csv"), index=False)
        self.train_df[["fare_amount"]].to_csv(os.path.join(processed_dir, "y_train.csv"), index=False)
        self.test_df[["trip_distance"]].to_csv(os.path.join(processed_dir, "X_test.csv"), index=False)
        self.test_df[["fare_amount"]].to_csv(os.path.join(processed_dir, "y_test.csv"), index=False)
        
        print(f"CSV files saved to {processed_dir}")

    def display_summary_statistics(self, subset="train"):
        """
        Display summary statistics for the dataset.

        Args:
            subset (str, optional): Which subset to display ('train', 'test', or 'all'). Defaults to 'train'.
        """
        if subset == "train":
            df = self.train_df
        elif subset == "test":
            df = self.test_df
        elif subset == "all":
            df = self.df
        else:
            print("Invalid subset specified. Choose from 'train', 'test', or 'all'.")
            return

        if df is None:
            print(f"{subset.capitalize()} data not available.")
            return

        print(f"Summary Statistics for {subset.capitalize()} Dataset:")
        return df.describe()

    def visualize_missing_values(self, subset="train"):
        """
        Create and save a heatmap to visualize missing values.

        Args:
            subset (str, optional): Which subset to visualize ('train', 'test', or 'all'). Defaults to 'train'.
        """
        if subset == "train":
            df = self.train_df
        elif subset == "test":
            df = self.test_df
        elif subset == "all":
            df = self.df
        else:
            print("Invalid subset specified. Choose from 'train', 'test', or 'all'.")
            return

        if df is None:
            print(f"{subset.capitalize()} data not available.")
            return

        # Create heatmap
        missing_value_chart = (
            alt.Chart(df.isna().reset_index().melt(id_vars="index"))
            .mark_rect()
            .encode(
                alt.X("index:O").axis(None),
                alt.Y("variable").title(None),
                alt.Color("value").title("NaN"),
                alt.Stroke("value"),
            )
            .properties(width=df.shape[0])
        )

        # Save the chart as SVG
        file_path = os.path.join(
            self.charts_dir, f"Missing_Values_Heatmap_{subset.capitalize()}.svg"
        )
        missing_value_chart.save(file_path)
        print(f"Missing values heatmap saved to {file_path}.")

    def create_correlation_plot(self, subset="train", method="spearman"):
        """
        Create and save a correlation plot for numerical columns in the dataset.

        Args:
            subset (str, optional): Which subset to use ('train', 'test', or 'all'). Defaults to 'train'.
            method (str, optional): Correlation method ('pearson', 'spearman', 'kendall'). Defaults to 'spearman'.
        """
        if subset == "train":
            df = self.train_df
        elif subset == "test":
            df = self.test_df
        elif subset == "all":
            df = self.df
        else:
            print("Invalid subset specified. Choose from 'train', 'test', or 'all'.")
            return

        if df is None:
            print(f"{subset.capitalize()} data not available.")
            return

        numeric_df = df.select_dtypes(include="number")
        if numeric_df.empty:
            print("No numerical columns available for correlation.")
            return

        corr_matrix = numeric_df.corr(method=method).stack().reset_index(name="corr")
        # Remove self-correlation
        corr_matrix = corr_matrix[corr_matrix["level_0"] != corr_matrix["level_1"]]
        corr_matrix["abs_corr"] = corr_matrix["corr"].abs()

        correlation_chart = (
            alt.Chart(corr_matrix)
            .mark_circle()
            .encode(
                x=alt.X("level_0:O", title=None),
                y=alt.Y("level_1:O", title=None),
                size=alt.Size(
                    "abs_corr:Q",
                    title="Scale",
                    scale=alt.Scale(domain=(0,1)),
                ),
                color=alt.Color(
                    "corr:Q", title="Correlation",
                ).scale(scheme='redblue', domain=(-1, 1)),
            )
            .properties(
                title=f"Correlation Plot ({method.capitalize()}) for {subset.capitalize()} Dataset",
                width=600,
                height=600,
            )
        )

        # Save the chart as SVG
        file_path = os.path.join(
            self.charts_dir,
            f"Correlation_Plot_{subset.capitalize()}_{method.capitalize()}.svg",
        )
        correlation_chart.save(file_path)
        print(f"Correlation plot saved to {file_path}.")

    def validate_data_schema(self, subset="train"):
        """
        Validate the data schema for specific columns.

        Args:
            subset (str, optional): Which subset to validate ('train', 'test', or 'all'). Defaults to 'train'.
        """

        if subset == "train":
            df = self.train_df
        elif subset == "test":
            df = self.test_df
        elif subset == "all":
            df = self.df
        else:
            print("Invalid subset specified. Choose from 'train', 'test', or 'all'.")
            return

        if df is None:
            print(f"{subset.capitalize()} data not available.")
            return

        # subset_df = df[["trip_distance", "fare_amount"]]

        try:
            self.schema.validate(df)
            print(
                f"Successfully validated the post EDA schema for the {subset} dataset!"
            )
        except pa.errors.SchemaError as e:
            print(f"Invalid data in {subset} dataset failed validation: {e}")

    def run_all(self):
        """Run all analysis steps in sequence."""
        self.load_data()
        if self.df is not None:
            self.create_density_chart("fare_amount", title="Fare_Amount_Density_Chart")
            self.filter_negative_fares()
            self.split_dataset()
            self.display_summary_statistics(subset="train")
            self.visualize_missing_values(subset="train")
            self.create_correlation_plot(subset="train")
            self.validate_data_schema(subset="train")


@click.group()
def cli():
    """Taxi Data Analyzer CLI"""
    pass


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--charts_dir', default="charts", help="Directory to save charts.")
def run_all(file_path, charts_dir):
    """Run all analysis steps on the dataset."""
    analyzer = TaxiDataAnalyzer(file_path, charts_dir)
    analyzer.run_all()


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--charts_dir', default="charts", help="Directory to save charts.")
def load(file_path, charts_dir):
    """Load the dataset."""
    analyzer = TaxiDataAnalyzer(file_path, charts_dir)
    analyzer.load_data()


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--charts_dir', default="charts", help="Directory to save charts.")
@click.option('--column', required=True, help="Column to plot.")
@click.option('--title', default="Density Chart", help="Title of the density chart.")
def create_density_chart(file_path, charts_dir, column, title):
    """Create a density chart for a specified column."""
    analyzer = TaxiDataAnalyzer(file_path, charts_dir)
    analyzer.load_data()
    analyzer.create_density_chart(column, title)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--charts_dir', default="charts", help="Directory to save charts.")
def filter_negative_fares(file_path, charts_dir):
    """Filter out rows with negative fare amounts."""
    analyzer = TaxiDataAnalyzer(file_path, charts_dir)
    analyzer.load_data()
    analyzer.filter_negative_fares()


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--charts_dir', default="charts", help="Directory to save charts.")
def split_dataset(file_path, charts_dir):
    """Split the dataset into training and testing sets."""
    analyzer = TaxiDataAnalyzer(file_path, charts_dir)
    analyzer.load_data()
    analyzer.split_dataset()


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--charts_dir', default="charts", help="Directory to save charts.")
@click.option('--subset', default="train", type=click.Choice(['train', 'test', 'all']), help="Subset of the data to validate.")
def validate_schema(file_path, charts_dir, subset):
    """Validate the data schema."""
    analyzer = TaxiDataAnalyzer(file_path, charts_dir)
    analyzer.load_data()
    analyzer.validate_data_schema(subset)

if __name__ == "__main__":
    cli()
