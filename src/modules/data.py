from flask import Blueprint, jsonify
import altair as alt
from vega_datasets import data

main = Blueprint("blueprint-data", __name__)


@main.route("/altair/example/pointmap")
def example_pointmap():
    # example taken from: https://altair-viz.github.io/gallery/point_map.html

    # Read in points
    airports = data.airports()

    # Read in polygons from topojson
    states = alt.topo_feature(data.us_10m.url, feature="states")

    # US states background
    background = (
        alt.Chart(states)
        .mark_geoshape(fill="lightgray", stroke="white")
        .properties(width=500, height=300)
        .project("albersUsa")
    )

    # airport positions on background
    points = (
        alt.Chart(airports)
        .mark_circle(size=10, color="steelblue")
        .encode(
            longitude="longitude:Q",
            latitude="latitude:Q",
            tooltip=["name", "city", "state"],
        )
    )

    chart = background + points

    return jsonify(chart.to_dict())


@main.route("/altair/example/barchart")
def barchart():
    # example taken from: https://altair-viz.github.io/gallery/bar_chart_with_highlighted_bar.html

    source = data.wheat()

    barchart = (
        alt.Chart(source)
        .mark_bar()
        .encode(
            x="year:O",
            y="wheat:Q",
            # The highlight will be set on the result of a conditional statement
            color=alt.condition(
                alt.datum.year == 1810,  # If the year is 1810 this test returns True,
                alt.value("orange"),  # which sets the bar orange.
                alt.value(
                    "steelblue"
                ),  # And if it's not true it sets the bar steelblue.
            ),
        )
        .properties(width=600)
    )

    return jsonify(barchart.to_dict())


@main.route("/altair/example/interactive/brushscatter")
def brush_scatter():
    # original example: https://altair-viz.github.io/gallery/scatter_linked_table.html
    source = data.cars()

    # Brush for selection
    brush = alt.selection_interval()

    # Scatter Plot
    points = (
        alt.Chart(source)
        .mark_point()
        .encode(
            x="Horsepower:Q",
            y="Miles_per_Gallon:Q",
            color=alt.condition(brush, alt.value("steelblue"), alt.value("grey")),
        )
        .add_params(brush)
    )

    # Base chart for data tables
    ranked_text = (
        alt.Chart(source)
        .mark_text(align="right")
        .encode(y=alt.Y("row_number:O").axis(None))
        .transform_filter(brush)
        .transform_window(row_number="row_number()")
        .transform_filter(alt.datum.row_number < 15)
    )

    # Data Tables
    horsepower = ranked_text.encode(text="Horsepower:N").properties(
        title=alt.Title(text="Horsepower", align="right")
    )
    mpg = ranked_text.encode(text="Miles_per_Gallon:N").properties(
        title=alt.Title(text="MPG", align="right")
    )
    origin = ranked_text.encode(text="Origin:N").properties(
        title=alt.Title(text="Origin", align="right")
    )
    text = alt.hconcat(horsepower, mpg, origin)  # Combine data tables

    # Build chart
    brush_scatter_plot = (
        alt.hconcat(points, text)
        .resolve_legend(color="independent")
        .configure_view(stroke=None)
    )

    return jsonify(brush_scatter_plot.to_dict())


@main.route("/altair/example/scatter")
def reusing_example():
    cars = data.cars.url

    chart = (
        alt.Chart(cars)
        .mark_circle()
        .encode(x="Horsepower:Q", y="Miles_per_Gallon:Q", color="Origin:N")
    )

    return jsonify(chart.to_dict())


@main.route("/altair/example/interactivelegend")
def interactive_legend():
    # example taken from: https://altair-viz.github.io/gallery/interactive_legend.html
    source = data.unemployment_across_industries.url

    selection = alt.selection_point(fields=["series"], bind="legend")

    chart = (
        alt.Chart(source)
        .mark_area()
        .encode(
            alt.X("yearmonth(date):T").axis(domain=False, format="%Y", tickSize=0),
            alt.Y("sum(count):Q").stack("center").axis(None),
            alt.Color("series:N").scale(scheme="category20b"),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        )
        .add_params(selection)
    )

    return jsonify(chart.to_dict())


@main.route("/altair/example/interactive-crossheight")
def interactive_crossheight():
    ## example from: https://altair-viz.github.io/gallery/interactive_cross_highlight.html
    source = data.movies.url

    pts = alt.selection_point(encodings=["x"])

    rect = (
        alt.Chart(data.movies.url)
        .mark_rect()
        .encode(
            alt.X("IMDB_Rating:Q").bin(),
            alt.Y("Rotten_Tomatoes_Rating:Q").bin(),
            alt.Color("count()").scale(scheme="greenblue").title("Total Records"),
        )
    )

    circ = (
        rect.mark_point()
        .encode(
            alt.ColorValue("grey"), alt.Size("count()").title("Records in Selection")
        )
        .transform_filter(pts)
    )

    bar = (
        alt.Chart(source, width=550, height=200)
        .mark_bar()
        .encode(
            x="Major_Genre:N",
            y="count()",
            color=alt.condition(
                pts, alt.ColorValue("steelblue"), alt.ColorValue("grey")
            ),
        )
        .add_params(pts)
    )

    chart = alt.vconcat(rect + circ, bar).resolve_legend(
        color="independent", size="independent"
    )

    return jsonify(chart.to_dict())


@main.route("/altair/example/brush")
def brush_example():
    # this example was taken directly from: https://altair-viz.github.io/user_guide/compound_charts.html
    source = data.sp500.url

    brush = alt.selection_interval(encodings=["x"])

    base = (
        alt.Chart(source)
        .mark_area()
        .encode(x="date:T", y="price:Q")
        .properties(width=600, height=200)
    )

    upper = base.encode(alt.X("date:T").scale(domain=brush))

    lower = base.properties(height=60).add_params(brush)

    chart = alt.vconcat(upper, lower)

    return jsonify(chart.to_dict())


@main.route("/altair/example/interactive-one-dropdown")
def interactive_dropdown_one():
    # Dropdown for both X-axis of scatter plot and Y-axis of bar chart
    dropdown = alt.binding_select(
        options=['Horsepower', 'Displacement', 'Weight_in_lbs', 'Acceleration'],
        name='Column Selector '
    )
    col_param = alt.param(
        value='Horsepower',
        bind=dropdown
    )

    # Scatter chart
    scatter_chart = alt.Chart(data.cars.url).mark_circle().encode(
        x=alt.X('x:Q', title=''),
        y='Miles_per_Gallon:Q',
        color='Origin:N'
    ).transform_calculate(
        x=f'datum[{col_param.name}]'
    ).add_params(
        col_param
    )

    # Bar chart
    bar_chart = alt.Chart(data.cars.url).mark_bar().encode(
        x=alt.X('Origin:N', title='Origin'),
        y=alt.Y('y:Q', title=''),
        color='Origin:N'
    ).transform_calculate(
        y=f'datum[{col_param.name}]'
    ).transform_aggregate(
        average_y='mean(y)',
        groupby=['Origin']
    ).encode(
        y='average_y:Q'
    )

    chart = alt.hconcat(scatter_chart, bar_chart)

    return jsonify(chart.to_dict())


@main.route("/altair/example/interactive-two-dropdown")
def interactive_dropdown_two():
    # # example idea built from: https://altair-viz.github.io/user_guide/interactions.html
    # Dropdown for X-axis
    dropdown_x = alt.binding_select(
        options=['Horsepower', 'Displacement', 'Weight_in_lbs', 'Acceleration'],
        name='Scatter: '
    )
    xcol_param = alt.param(
        value='Horsepower',
        bind=dropdown_x
    )

    # Dropdown for Y-axis
    dropdown_y = alt.binding_select(
        options=['Horsepower', 'Displacement', 'Weight_in_lbs', 'Acceleration'],
        name='Bar: '
    )
    ycol_param = alt.param(
        value='Horsepower',
        bind=dropdown_y
    )

    # Scatter chart
    scatter_chart = alt.Chart(data.cars.url).mark_circle().encode(
        x=alt.X('x:Q', title=''),
        y='Miles_per_Gallon:Q',
        color='Origin:N'
    ).transform_calculate(
        x=f'datum[{xcol_param.name}]'
    ).add_params(
        xcol_param
    )

    # Bar chart
    bar_chart = alt.Chart(data.cars.url).mark_bar().encode(
        x=alt.X('Origin:N', title='Origin'),
        y=alt.Y('y:Q', title=''),
        color='Origin:N'
    ).transform_calculate(
        y=f'datum[{ycol_param.name}]'
    ).transform_aggregate(
        average_y='mean(y)',
        groupby=['Origin']
    ).encode(
        y='average_y:Q'
    ).add_params(
        ycol_param
    )

    chart = alt.hconcat(scatter_chart, bar_chart)

    return jsonify(chart.to_dict())



@main.route("/altair/example/interactive-one-dropdown-three-visuals")
def interactive_dropdown_one_three_visuals():

    # Dropdown for X-axis of scatter plot, Y-axis of bar chart, and other charts
    dropdown = alt.binding_select(
        options=['Horsepower', 'Displacement', 'Weight_in_lbs', 'Acceleration'],
        name='Column Selector '
    )
    col_param = alt.param(
        value='Horsepower',
        bind=dropdown
    )

    # Scatter chart
    scatter_chart = alt.Chart(data.cars.url).mark_circle().encode(
        x=alt.X('x:Q', title=''),
        y='Miles_per_Gallon:Q',
        color='Origin:N'
    ).transform_calculate(
        x=f'datum[{col_param.name}]'
    ).add_params(
        col_param
    )

    # Bar chart
    bar_chart = alt.Chart(data.cars.url, width=300).mark_bar().encode(
        x=alt.X('Origin:N', title='Origin'),
        y=alt.Y('y:Q', title=''),
        color='Origin:N'
    ).transform_calculate(
        y=f'datum[{col_param.name}]'
    ).transform_aggregate(
        average_y='mean(y)',
        groupby=['Origin']
    ).encode(
        y='average_y:Q'
    )

    # Line chart showing trend over the years
    line_chart = alt.Chart(data.cars.url).mark_line().encode(
        x='Year:T',
        y=alt.Y('y:Q', title=''),
        color='Origin:N'
    ).transform_calculate(
        y=f'datum[{col_param.name}]'
    ).transform_aggregate(
        average_y='mean(y)',
        groupby=['Year', 'Origin']
    ).encode(
        y='average_y:Q'
    )

    # Combining all the charts
    row_1 = alt.hconcat(scatter_chart, bar_chart)
    row_2 = alt.hconcat(line_chart)
    chart = alt.vconcat(row_1, row_2)

    return jsonify(chart.to_dict())
