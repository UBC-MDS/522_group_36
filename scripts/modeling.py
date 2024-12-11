import click
import os
import altair as alt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

@click.command()
@click.option('--x-train-path', type=str, help="Path to X training data")
@click.option('--y-train-path', type=str, help="Path to y training data")
@click.option('--x-test-path', type=str, help="Path to X testing data")
@click.option('--y-test-path', type=str, help="Path to y testing data")
@click.option('--charts-dir', type=str, default="charts", help="Directory to save charts")
def main(x_train_path, y_train_path, x_test_path, y_test_path, charts_dir='charts'):
    # Fits a simple linear regression model onto the training data
    
    X_train = pd.read_csv(x_train_path)['trip_distance'].values.reshape(-1,1)
    y_train = pd.read_csv(y_train_path)['fare_amount'].values
    X_test = pd.read_csv(x_test_path)['trip_distance'].values.reshape(-1,1)
    y_test = pd.read_csv(y_test_path)['fare_amount'].values
    
    np.random.seed(552)

    # Fit our Linear Regression Model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    intercept = model.intercept_
    slope = model.coef_[0]
    
    test_predictions = pd.DataFrame({
        'trip_distance': X_test.flatten(),
        'fare_amount': y_test,
        'y_pred': model.predict(X_test)
    })

    formula_text = f"The regression line formula is: y_hat = {slope:.4f} * trip_distance + {intercept:.4f}"
    
    formula_chart = alt.Chart(pd.DataFrame({'text': [formula_text]})).mark_text(
        align='center',
        baseline='middle',
        fontSize=14
    ).encode(
        text='text:N'
    ).properties(
        width=600,
        height=100
    )

    formula_svg_path = os.path.join(charts_dir, "Regression_Formula_Text.png")
    formula_chart.save(formula_svg_path)
    print(f"Regression formula saved to {formula_svg_path}.")
    
    print(test_predictions)

    # Calculate error metrics
    y_true = test_predictions['fare_amount']
    y_pred = test_predictions['y_pred']
    test_predictions['residuals'] = y_true - y_pred
    test_predictions['abs_residuals'] = np.abs(test_predictions['residuals'])
    
    metrics = {
        'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
        'R²': r2_score(y_true, y_pred),
        'MAE': mean_absolute_error(y_true, y_pred)
    }

    metrics_text = (
        "Regression Performance Metrics:\n"
        f"RMSE: ${metrics['RMSE']:.2f}\n"
        f"R²: {metrics['R²']:.3f}\n"
        f"MAE: ${metrics['MAE']:.2f}"
    )

    metrics_chart = alt.Chart(pd.DataFrame({'text': [metrics_text]})).mark_text(
        align='center',
        baseline='middle',
        fontSize=14
    ).encode(
        text='text:N'
    ).properties(
        width=600,
        height=200
    )

    metrics_svg_path = os.path.join(charts_dir, "Regression_Performance_Metrics.png")
    metrics_chart.save(metrics_svg_path)
    print(f"Regression performance metrics saved to {metrics_svg_path}.")

    error_scatter = alt.Chart(test_predictions).mark_circle(size=60, opacity=0.3).encode(
        x=alt.X('fare_amount', title='Actual Fare Amount ($)'),
        y=alt.Y('y_pred', title='Predicted Fare Amount ($)'),
        tooltip=['trip_distance', 'fare_amount', 'y_pred', 'residuals']
    ).properties(
        width=400,
        height=400,
        title='Predicted vs Actual Taxi Fare Amounts With Error Line'
    )
    error_diagonal = alt.Chart(pd.DataFrame({
        'x': [test_predictions['fare_amount'].min(), test_predictions['fare_amount'].max()]
    })).mark_line(color='red', strokeDash=[4, 4]).encode(
        x='x',
        y='x'
    )
    
    combined_chart = error_scatter + error_diagonal

    combined_chart_path = os.path.join(charts_dir, "Pred_Vs_Actual.png")

    combined_chart.save(combined_chart_path)
    print(f"Error scatter and diagonal chart saved to {combined_chart_path}.")

    scatter_plot = alt.Chart(test_predictions).mark_circle().encode(
        x=alt.X('trip_distance', title='Trip Distance (miles)'),
        y=alt.Y('fare_amount', title="Fare Amount (USD)"),
        color=alt.value('purple'),
        tooltip=['trip_distance', 'fare_amount']
    ).properties(
        title="Regression of Trip Distance vs Fare Amount for NYC Yellow Taxis in January 2024"
    )
    
    line_plot = alt.Chart(test_predictions).mark_line(color='orange').encode(
        x='trip_distance',
        y='y_pred'
    )
    
    final_chart = scatter_plot + line_plot
    
    final_chart_path = os.path.join(charts_dir, "Final_Linear_Regression.png")

    final_chart.save(final_chart_path)
    print(f"Final Linear Regression Chart saved to {final_chart_path}.")

if __name__ == "__main__":
    main()






