import pandas as pd

from bokeh.layouts import row, column
from bokeh.plotting import figure, curdoc, output_file, figure, output_file, save
from bokeh.models import ColumnDataSource, RangeSlider, RadioButtonGroup, CustomJS
from bokeh.models.widgets.buttons import Button

from bokeh.transform import factor_cmap, factor_mark
from bokeh.palettes import Spectral

### -----

egg_data = pd.read_csv("../data/easter_eggs.csv")

egg_data_inch = egg_data.copy()
egg_data_inch['length'] = egg_data['length']/2.54 
egg_data_inch['width'] = egg_data['width']/2.54 

source = ColumnDataSource(egg_data)

# Min and max
min_length = egg_data["length"].min()
max_length = egg_data["length"].max()

min_width = egg_data["width"].min()
max_width = egg_data["width"].max()


# Create a plot and label axes
p = figure(width=800,
           height=800,
           x_range=(0, max_length),
           y_range=(0, max_width),
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

scatter_plot = p.scatter("length", "width",
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
    start=min_length,
    end=max_length,
    value=(min_length, max_length),
    step=0.1,
    title="Minimum Length"
)

# Radio buttons with initia selection ("All")
type_buttons = RadioButtonGroup(labels=['All', 'Real egg', 'Chocolate egg', 'Vegan chocolate egg'], active=0)


combined_callback_code = """
var data = source.data;
var original_data = original_source.data;
var value = slider_value.value
console.log("value: " + value);
var type = type_selection.active;
var typeact = type_selection.value;

var button_dict =  {0:'All', 1:'Real egg', 2:'Chocolate egg', 3:'Vegan chocolate egg'};

console.log("type: " + type);

console.log("type: " + value[0]);

console.log(button_dict[type]);


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
        slider_value=range_slider,
        type_selection=type_buttons,
    ),
    code=combined_callback_code
)

switched_to_inch = False

inch_button = Button(
    label="Switch to inch",
    button_type="primary",
    width=50
)

# Functions for updating data shown in plot

# Activate when slider or button are changed
range_slider.js_on_change("value", callback)
type_buttons.js_on_change("active", callback)

output_file('../outputs/interactive_easter_eggs.html')



template= template = """{% block postamble %}

    <style type="text/css">
      @font-face {
        font-family: "Averta";
        src: url("Intelligent Design - Averta-Regular.otf") format("truetype");
        }
      p.customfont { 
        font-family: "Averta";
        }

    .bk-root .bk-btn-primary  {
        color: #FDFEFE;
        background-color: #0000FF;
        border-color: #21618C;
        }

    .bk-root .bk-btn-default.bk-active {
        color: #FDFEFE;
        background-color: #0000FF;
        border-color: #21618C;
        }

    input[type="checkbox"] {
        accent-color: 
        }
    
    .bk-root {font-family: Averta}

    .bok-root div.bk-tooltip.bk-left

    {
        color: #0000FF;
    }

     .bk-root .bk-tooltip {
        color: #0000FF;
    }

    .center {
     
      display: flex;
      justify-content: center;
      font-family: "Averta";

      }

    spinner-wrapper {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: #ff6347;
      z-index: 999999;
      }

      @keyframes rotate {
        from {
          transform: rotate(0deg);
        }
      
        to {
          transform: rotate(360deg);
        }
      }
      
      .spinner {
      width: 40px;
      height: 40px;
      background-image: url("hp_icon.png");
      background-size: 100px;
      animation: rotate 2s linear infinite;
      }

    .spinner{
        width: 100px;
        height: 100px; 
        margin: 50px auto 0;
        border-radius: 50%;
        border: 20px solid #0000FF;
        border-left-color: transparent;
        position: relative; 
        animation: 5s rotIvs infinite linear; 
    } 
    
    .spinner:before{
        content: "";
        width: calc(100% + 40px);
        height: calc(100% + 40px);
        border-radius: 50%;
        border: 20px dashed #0000FF;
        transform: translateX(-50%) translateY(-50%);
        position: absolute;
        top: 50%;
        left: 50%;
        animation: 2s rot infinite linear;
    } 

    @keyframes rot{
        100%{ transform: translateX(-50%) translateY(-50%) rotate(360deg); }
    }
    @keyframes rotIvs{
        100%{ transform: rotate(360deg); }
    } 
    
      </style> 
    {% endblock %} """


save(row(column(range_slider, type_buttons, inch_button), p), template=template)
### Your Turn: Take one of your datasets and build something similar of your own