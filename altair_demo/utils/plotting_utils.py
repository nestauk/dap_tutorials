"""
utils.plotting_utils

Functions for easier generation of graphs
"""

import altair as alt
import pandas as pd

ChartType = alt.vegalite.v4.api.Chart

# Fonts and colours
FONT = "Averta"
TITLE_FONT = "Averta"
FONTSIZE_TITLE = 16
FONTSIZE_SUBTITLE = 13
FONTSIZE_NORMAL = 13

NESTA_COLOURS = [
    "#0000FF",
    "#FDB633",
    "#18A48C",
    "#9A1BBE",
    "#EB003B",
    "#FF6E47",
    "#646363",
    "#0F294A",
    "#97D9E3",
    "#A59BEE",
    "#F6A4B7",
    "#D2C9C0",
    "#FFFFFF",
    "#000000",
]

def nestafont():
    """Define Nesta fonts"""
    return {
        "config": {
            "title": {"font": TITLE_FONT, "anchor": "start"},
            "axis": {"labelFont": FONT, "titleFont": FONT},
            "header": {"labelFont": FONT, "titleFont": FONT},
            "legend": {"labelFont": FONT, "titleFont": FONT},
            "range": {
                "category": NESTA_COLOURS,
                "ordinal": {
                    "scheme": NESTA_COLOURS
                },  # this will interpolate the colors
            },
        }
    }    

alt.themes.register("nestafont", nestafont)
alt.themes.enable("nestafont")


def configure_plots(fig, chart_title: str = "", chart_subtitle: str = ""):
    """Adds titles, subtitles; configures font sizes; adjusts gridlines"""
    return (
        fig.properties(
            title={
                "anchor": "start",
                "text": chart_title,
                "fontSize": FONTSIZE_TITLE,
                "subtitle": chart_subtitle,
                "subtitleFont": FONT,
                "subtitleFontSize": FONTSIZE_SUBTITLE,
            },
        )
        .configure_axis(
            gridDash=[1, 7],
            gridColor="grey",
            labelFontSize=FONTSIZE_NORMAL,
            titleFontSize=FONTSIZE_NORMAL,
        )
        .configure_legend(
            titleFontSize=FONTSIZE_NORMAL,
            labelFontSize=FONTSIZE_NORMAL,
        )
        .configure_view(strokeWidth=0)
    )


