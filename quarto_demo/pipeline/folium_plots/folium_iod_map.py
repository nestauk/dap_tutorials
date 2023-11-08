import numpy as np
import folium
import pandas as pd
from folium.plugins import GroupedLayerControl
from quarto_demo.utils.folium_utils import creating_folium_layer
from quarto_demo.utils.preprocessing import (
    convert_range_to_list,
)
from quarto_demo import config, iod_config, PROJECT_DIR
from quarto_demo.getters.english_la_iod_data_2019 import get_english_la_iod_2019
from quarto_demo.getters.la_shapefiles_2019 import get_english_la_shapefiles_2019_gpd


def create_iod_folium_map(
    shapefiles: pd.DataFrame,
    iod_data: pd.DataFrame,
) -> folium.Map:
    """Creates the folium map for the IMD data.
    Args:
        shapefiles (pd.DataFrame): The ward shapefiles.
        iod_data (pd.DataFrame): The IMD data for 2019.
    Returns:
        folium.Map: The folium map for the IMD data.
    """

    # Loading the config parameters
    # Folium scheme
    folium_scheme = config["folium_scheme"]
    # Pulling in the IoD names and indices from the config file
    iod_names = iod_config["iod_names"]
    iod_indices = iod_config["iod_indices"]
    iod_tooltips = iod_config["iod_tooltip"]
    # Iod bins
    folium_domain = convert_range_to_list(iod_config["iod_bins"])

    # Creating the base map
    iod_map = folium.Map(
        # location=[52.475011, -1.888681],
        location=[52.497556, -1.738482],
        tiles=None,
        zoom_start=6,
        attr="Birmingham basemap",
    )
    folium.TileLayer("CartoDB positron", name="Birmingham basemap").add_to(iod_map)

    # Creating the list of choropleth map layers
    list_of_layers = []
    for iod_index, iod_name, iod_tooltip in zip(iod_indices, iod_names, iod_tooltips):
        # Creating the choropleth map layers
        list_of_layers.append(
            creating_folium_layer(
                outcome_map=iod_map,
                shapefiles=shapefiles,
                data=iod_data,
                data_col=iod_index,
                data_name=iod_tooltip,
                legend_name=iod_name,
                tooltip_fields=["lad19nm"] + iod_indices,
                tooltip_aliases=["Local Authority"] + iod_tooltips,
                bins=folium_domain,
                colour_scheme=folium_scheme,
                shapefile_geo="lad19cd",
                shapefile_merge=["lad19cd", "lad19nm", "region_name"],
                data_geo=["lad19cd", "lad19nm", "region_name"],
            )
        )

    # Adding the layer control; to allow you to switch between the layers
    iod_map.add_child(
        folium.map.LayerControl("topleft", overlay=False, hideSingleBase=True)
    )

    # Adding the grouped layer control so that the layers cannot overlap
    GroupedLayerControl(
        groups={"IMD": list_of_layers},
        collapsed=False,
        # position="topleft",
        maxHeight="50px",
    ).add_to(iod_map)

    return iod_map


if __name__ == "__main__":
    # Loading shapefiles
    shapefiles = get_english_la_shapefiles_2019_gpd()
    shapefiles.region_name = shapefiles.region_name.str.replace(
        "East of England", "East"
    )

    # Loading IMD data
    imd_deciles = get_english_la_iod_2019()

    # Creating the map
    iod_map = create_iod_folium_map(
        shapefiles=shapefiles,
        iod_data=imd_deciles,
    )
    # Saving the map
    iod_map.save(str(PROJECT_DIR) + "/outputs/figures/choropleth_map_iod.html")
