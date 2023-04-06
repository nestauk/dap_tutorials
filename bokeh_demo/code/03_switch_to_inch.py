import pandas as pd

from bokeh.layouts import row, column
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Slider, RadioButtonGroup
from bokeh.models.widgets.buttons import Button

from bokeh.transform import factor_cmap, factor_mark
from bokeh.palettes import Spectral

### -----

egg_data = pd.read_csv("../data/easter_eggs.csv")

egg_data_inch = egg_data.copy()
egg_data_inch["length"] = egg_data["length"] / 2.54
egg_data_inch["width"] = egg_data["width"] / 2.54

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

# Inch button
inch_button = Button(label="Switch to inch", button_type="primary", width=50)

# Default settings
selected_type = 0
switched_to_inch = False

# Functions for updating data shown in plot
def update_shown_data():
    """Update the data shown in plot based on input via sliders and buttons."""

    # Switch to inches
    if switched_to_inch:
        filtered_data = egg_data_inch
    else:
        filtered_data = egg_data

    # Select by type, If not "All"
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


def change_data_source():
    """Swich from cm to inch or back."""

    global switched_to_inch

    if switched_to_inch:
        p.xaxis.axis_label = "Length (cm)"
        p.yaxis.axis_label = "Width (cm)"
        switched_to_inch = False

    else:
        p.xaxis.axis_label = "Length (inches)"
        p.yaxis.axis_label = "Width (inches)"
        switched_to_inch = True

    update_shown_data()


# Activate when slider or button are changed
length_slider.on_change("value", change_min_length)
type_buttons.on_change("active", type_change)
inch_button.on_click(change_data_source)

# Output to server
curdoc().add_root(
    row(
        column(length_slider, type_buttons, inch_button, width=400),
        column(p, sizing_mode="scale_both"),
    )
)


### Your Turn: Take one of your datasets and build something similar of your own
