import folium
from quarto_demo import config
from quarto_demo.utils.bindmap import bindmap
import pandas as pd

# Folium colour scheme
folium_scheme = config["folium_scheme"]


def creating_folium_layer(
    outcome_map: folium.Map,
    shapefiles: pd.DataFrame,
    data: pd.DataFrame,
    data_col: str,
    data_name: str,
    legend_name: str,
    tooltip_fields: list,
    tooltip_aliases: list,
    bins: list,
    colour_scheme: str = folium_scheme,
    fill_opacity: float = 0.6,
    line_opacity: float = 0.3,
    shapefile_geo: str = "wd22nm",
    shapefile_merge: list = ["wd22nm"],
    data_geo: str = ["ward"],
) -> folium.Map:
    """Creates a folium layer for a asq outcome as a choropleth map layer.

    Args:
        outcome_map (folium.Map): Folium map
        shapefiles (pd.DataFrame): Ward shapefiles
        data (pd.DataFrame): data to be mapped
        data_col (str): Column name of the data to be mapped
        data_name (str): Name of the layer
        legend_name (str): Name of the legend
        tooltip_fields (list): List of fields to be included in the tooltip
        tooltip_aliases (list): List of aliases for the fields to be included in the tooltip
        bins (list): List of bins for the choropleth map
        colour_scheme (str, optional): Colour scheme for the choropleth map. Defaults to folium_scheme.
        fill_opacity (float, optional): Fill opacity for the choropleth map. Defaults to 0.6.
        line_opacity (float, optional): Line opacity for the choropleth map. Defaults to 0.3.
        shapefile_geo (str, optional): Column name of the geometry wanted in shapefiles. Defaults to "wd22nm".
        shapefile_merge (list, optional): List of columns to be merged with the shapefiles. Defaults to ["wd22nm"].
        data_geo (list, optional): List of columns to be merged with the data. Defaults to ["ward"].
    Returns:
        folium.Map: Choropleth map layer.
    """

    # Merging the ward shapefiles with the asq data
    data_for_map = shapefiles.merge(
        data, left_on=shapefile_merge, right_on=data_geo, how="left"
    )

    # Creating the choropleth map layer
    map = folium.features.Choropleth(
        geo_data=data_for_map,
        data=data_for_map,
        columns=[shapefile_geo, data_col],
        key_on=f"feature.properties.{shapefile_geo}",
        fill_color=colour_scheme,
        fill_opacity=fill_opacity,
        line_opacity=line_opacity,
        nan_fill_opacity=0,
        legend_name=legend_name,
        name=data_name,
        bins=bins,
    )
    outcome_map.add_child(map)

    # To ensure the legend occurs only when you click on the layer, we add it separately.
    for key in map._children:
        if key.startswith("color_map"):
            branca_color_map = map._children[key]
            del map._children[key]
    outcome_map.add_child(branca_color_map)
    outcome_map.add_child(bindmap(map, branca_color_map))

    folium.GeoJsonTooltip(
        fields=tooltip_fields,
        aliases=tooltip_aliases,
    ).add_to(map.geojson)

    return map
