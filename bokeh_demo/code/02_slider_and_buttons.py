import pandas as pd

from bokeh.plotting import figure, curdoc

from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Slider, RadioButtonGroup

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

### -- Interactive widgets

# Length slider
length_slider = Slider(
    start=min_length, end=max_length, value=min_length, step=0.1, title="Minimum Length"
)

# Radio buttons with initia selection ("All")
type_buttons = RadioButtonGroup(
    labels=["All", "Real egg", "Chocolate egg", "Vegan chocolate egg"], active=0
)

# For easier mapping of radio button input to data
button_dict = {0: "All", 1: "Real egg", 2: "Chocolate egg", 3: "Vegan chocolate egg"}
selected_type = 0

# Functions for updating data shown in plot

def update_shown_data():
    """Update the data shown in plot based on input via minimum length slider and buttons."""

    filtered_data = egg_data

    # If not "All"
    if selected_type != 0:
        filtered_data = filtered_data[
            filtered_data["type"] == button_dict[selected_type]
        ]

    filtered_data = filtered_data[(egg_data["length"] >= min_length)]

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


def type_change(attr, old, new):
    """Change the egg type based on input of radio button.

    Args:
        attr (str): Bokeh excepts this pattern, so cannot be removed.
        old (int): Bokeh excepts this pattern, so cannot be removed.
        new (int): New value for type.
    """

    global selected_type
    selected_type = new
    update_shown_data()


# Activate when slider or button are changed
length_slider.on_change("value", change_min_length)
type_buttons.on_change("active", type_change)

# Output to server
curdoc().add_root(row(column(length_slider, type_buttons, width=400), p))


### Your Turn: Remove the type button and add instead a dropdown menu or checkbox group for the different egg types
# For more information, see https://docs.bokeh.org/en/2.4.2/docs/user_guide/interaction/widgets.html
