import pandas as pd

from bokeh.plotting import figure, curdoc

from bokeh.models import ColumnDataSource
from bokeh.layouts import row
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Slider

from bokeh.transform import factor_cmap, factor_mark
from bokeh.palettes import Spectral

### -----

egg_data = pd.read_csv("../data/easter_eggs.csv")

# Min and max
min_length = egg_data["length"].min()
max_length = egg_data["length"].max()

min_width = egg_data["width"].min()
max_width = egg_data["width"].max()


# Create a plot and label axes
p = figure(
    width=800,
    height=800,
    x_range=(0, max_length),
    y_range=(0, max_width),
    title="Easter egg widths and lengths",
)
p.xaxis.axis_label = "Length (cm)"
p.yaxis.axis_label = "Width (cm)"


# Cosmetics
color_map = Spectral[4]
types = ["Chocolate egg", "Vegan chocolate egg", "Real egg"]
markers = ["circle", "hex_dot", "inverted_triangle"]

# Scatter plot
fm = factor_mark("type", markers, types)
fc = factor_cmap("type", color_map, types)

scatter_plot = p.scatter(
    "length",
    "width",
    source=egg_data,
    legend_field="type",
    fill_alpha=0.4,
    size=12,
    marker=fm,
    color=fc,
)

p.legend.location = "top_left"


# Length slider
length_slider = Slider(
    start=min_length, end=max_length, value=min_length, step=0.1, title="Minimum Length"
)

# Functions for updating data shown in plot


def update_shown_data():
    """Update the data shown in plot based on input via minimum length slider."""
    filtered_data = egg_data[(egg_data["length"] >= min_length)]
    scatter_plot.data_source.data.update(ColumnDataSource(filtered_data).data)


def change_min_length(attr, old, new):
    """Change the minimum length based on slider input.

    Args:
        attr (str): Bokeh excepts this pattern, so cannot be removed.
        old (int): Bokeh excepts this pattern, so cannot be removed.
        new (int): New value for minimum.
    """

    global min_length
    min_length = new
    update_shown_data()


# Activate when slider is changed
length_slider.on_change("value", change_min_length)

# Output to server
curdoc().add_root(row(length_slider, p))


### Your Turn: Add another slider for minimum width
