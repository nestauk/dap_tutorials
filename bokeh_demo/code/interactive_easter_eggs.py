import pandas as pd

from bokeh.layouts import row, column
from bokeh.plotting import figure, curdoc, output_file, figure, output_file, save
from bokeh.models import ColumnDataSource, RangeSlider, RadioButtonGroup, CustomJS
from bokeh.models.widgets.buttons import Toggle

from bokeh.transform import factor_cmap, factor_mark
from bokeh.palettes import Spectral

import templates

### -----

egg_data = pd.read_csv("../data/easter_eggs.csv")

egg_data_inch = egg_data.copy()
egg_data_inch['length'] = egg_data['length']/2.54 
egg_data_inch['width'] = egg_data['width']/2.54 

source = ColumnDataSource(egg_data)

# Min and max
max_length = egg_data["length"].max()
max_width = egg_data["width"].max()


# Create a plot and label axes
p = figure(width=600,
           height=600,
           x_range=(0, max_length+1/10*max_length),
           y_range=(0, max_width+1/10*max_width),
           title="Easter egg widths and lengths"
           )
p.xaxis.axis_label = "Length (cm)"
p.yaxis.axis_label = "Width (cm)"


# Cosmetics
color_map = Spectral[4]
types = ["Chocolate egg", "Vegan chocolate egg", "Real egg"]
markers = ["hex", "circle_x", "triangle"]

# Scatter plot
fm = factor_mark("type", ["hex", "circle_x", "triangle"], types)
fc = factor_cmap("type", color_map, types)

p.scatter("length", "width",
          source=source, 
          legend_field="type",
          fill_alpha=0.4, 
          size=12,
          marker=fm,
          color=fc,
          )

p.legend.location = "top_left"

### -- Interactive widgets

# Length slider
range_slider = RangeSlider(
    start=0,
    end=max_length,
    value=(0, max_length),
    step=0.1,
    title="Length slider"
)

# Radio buttons with initia selection ("All")
type_buttons = RadioButtonGroup(labels=['All', 'Real egg', 'Chocolate egg', 'Vegan chocolate egg'], active=0)

# Toggle button for switching to inch and back to cm
inch_button = Toggle(
    label="Switch to inch",
    button_type="primary",
    width=50
)
combined_callback_code = """

var data = source.data;
var value = slider_value.value
var type = type_selection.active;
var typeact = type_selection.value;
var toggle = this.active;

if (toggle === true) {
  var original_data = inch_source.data;
  ax1[0].axis_label = "Lenght (inches)";
  ax2[0].axis_label = "Weight (inches)"; 

  }

else {
  var original_data = original_source.data;
  ax1[0].axis_label = "Lenght (cm)";
  ax2[0].axis_label = "Weight (cm)"; 
}

var max_length = Math.max.apply(Math, original_data['length']) ;
var max_width = Math.max.apply(Math, original_data['width']) ;

x_range.end = max_length + 1/10*max_length;
x_range.change.emit();
y_range.end = max_width + 1/10*max_width;
y_range.change.emit();

var button_dict =  {0:'All', 1:'Real egg', 2:'Chocolate egg', 3:'Vegan chocolate egg'};

for (var key in original_data) {
    data[key] = [];
    for (var i = 0; i < original_data['type'].length; ++i) {
        if ((type === 0 || original_data['type'][i] === button_dict[type]) &&
            (original_data['length'][i] >= value[0] && original_data['length'][i] <= value[1])) {
            data[key].push(original_data[key][i]);
        }
    }
}

source.change.emit();
"""

callback = CustomJS(
    args=dict(
        source=source,
        original_source=ColumnDataSource(egg_data),
        inch_source=ColumnDataSource(egg_data_inch),
        slider_value=range_slider,
        type_selection=type_buttons,
        inch_toggle=inch_button,
        ax1=p.xaxis, 
        ax2=p.yaxis,
        x_range=p.x_range,
        y_range=p.y_range,

    ),
    code=combined_callback_code
)


# Functions for updating data shown in plot

# Activate when slider or button are changed
range_slider.js_on_change("value", callback)
type_buttons.js_on_change("active", callback)
inch_button.js_on_click(callback)

# Averta font (could be atted to template)
p.yaxis.axis_label_text_font = "Averta"
p.xaxis.axis_label_text_font = "Averta"
p.title.text_font = "Averta"
p.legend.label_text_font = 'Averta'

# Save
output_file('../outputs/interactive_easter_eggs.html')

save(row(column(range_slider, type_buttons, inch_button, width=400), column(p, sizing_mode='scale_both')), template=templates.nesta_template)

### Your Turn: Take one of your datasets and build something similar of your own