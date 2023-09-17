from flask import Blueprint, jsonify
import altair as alt
from vega_datasets import data
import pandas as pd

main = Blueprint('blueprint-data', __name__)

### This below endpoint shows a single chart with static data
@main.route('/chart-data')
def chart_data():
    # Sample data
    data = pd.DataFrame({
        'x': ['A', 'B', 'C', 'D', 'E'],
        'y': [5, 3, 6, 7, 2]
    })

    # Create Altair chart
    simple_chart = alt.Chart(data).mark_bar().encode(
        x='x',
        y='y'
    )   
    return jsonify(simple_chart.to_dict())


### This below endpoint should demonstrate the functionality of INTERACTIVE charts
@main.route('/chart-data-2')
def chart_data_2():
    # Sample data for two products across months
    data = pd.DataFrame({
        'month': ['A', 'B', 'C', 'D', 'E']*2,
        'sales': [5, 3, 6, 7, 2, 4, 31, 14, 23, 30],
        'product': ['Product 1']*5 + ['Product 2']*5
    })

    print(data)

    # Selection for interaction
    brush = alt.selection(type='interval', encodings=['x'])

    # First chart for 'Product 1'
    chart1 = alt.Chart(data[data['product'] == 'Product 1']).mark_bar().encode(
        x='month',
        y='sales',
        color=alt.condition(brush, 'product:N', alt.value('lightgray'))
    ).add_selection(
        brush
    )

    # Second chart for 'Product 2' with the interaction from the first chart
    chart2 = alt.Chart(data[data['product'] == 'Product 2']).mark_bar().encode(
        x='month',
        y='sales',
        color=alt.condition(brush, 'product:N', alt.value('lightgray'))
    )

    # Combine the two charts
    combined_cart = alt.hconcat(chart1, chart2).properties(title='Sales by month')

    return jsonify(combined_cart.to_dict())



@main.route('/altair/example/reusing')
def reusing_example():
    cars = data.cars.url

    chart = alt.Chart(cars).mark_circle().encode(
        x='Horsepower:Q',
        y='Miles_per_Gallon:Q',
        color='Origin:N'
    )

    return jsonify(chart.to_dict())



@main.route('/altair/example/brush')
def brush_example():
    # this example was taken directly from: https://altair-viz.github.io/user_guide/compound_charts.html
    source = data.sp500.url

    brush = alt.selection_interval(encodings=['x'])

    base = alt.Chart(source).mark_area().encode(
        x = 'date:T',
        y = 'price:Q'
    ).properties(
        width=600,
        height=200
    )

    upper = base.encode(alt.X('date:T').scale(domain=brush))

    lower = base.properties(
        height=60
    ).add_params(brush)

    chart = alt.vconcat(upper, lower)

    return jsonify(chart.to_dict())
