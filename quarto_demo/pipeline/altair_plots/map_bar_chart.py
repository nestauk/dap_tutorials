import altair as alt
from altair import Data, Chart
import geopandas as gpd
import pandas as pd
from quarto_demo.utils.preprocessing import convert_range_to_list
from quarto_demo import config, iod_config


def create_map_bar_plot(
    data: pd.DataFrame,
    geodata_la: gpd.GeoDataFrame,
    region: str,
    iod_of_interest: str = "Index of Multiple Deprivation (IMD)",
) -> Chart:
    """
    Creates an interactive map and bar chart for the IoD deciles of the selected region.

    Args:
        data (pd.DataFrame): DataFrame with the IoD deciles.
        geodata_la (alt.Data): GeoJSON file with the shapefiles of the regions.
        region (str): Name of the region to plot.

    Returns:
        alt.Chart: Interactive map and bar chart.
    """
    # Altair map struggles with epsg 4326, so convert to 3857
    geodata_la = geodata_la.to_crs(epsg=3857)
    # Altair theme
    theme_altair = config["altair_theme"]
    # Nesta colour palette
    nesta_colours = config["nesta_colours"]
    altair_domain = convert_range_to_list(config["altair_domain"])

    # Pulling in the IoD names and indices from the config file
    iod_names = iod_config["iod_names"]
    iod_indices = iod_config["iod_indices"]
    iod_tooltip = iod_config["iod_tooltip"]
    # Creating Dictionaries to link the two indices
    iod_dict = dict(zip(iod_names, iod_indices))
    iod_dict_inv = dict(zip(iod_indices, iod_names))

    # Creating the selection for the map
    la_select = alt.selection_single(fields=["lad19nm"])
    la_select_all = alt.selection_single(fields=["lad19nm"], empty="none")

    # Creating a melted version of the data for the bar chart
    la_melt = (
        pd.melt(
            data,
            id_vars=["lad19cd", "lad19nm", "region_name"],
            value_vars=iod_indices,
        )
        .rename(columns={"variable": "iod", "value": "decile"})
        .assign(iod_name=lambda df: df.iod.replace(iod_dict_inv))
    )

    # Creating a list of the local authorities to plot
    las_to_plot = list(data[data["region_name"] == region].lad19nm)

    # Creating the colour scale for the map
    color_las = alt.condition(
        la_select,
        alt.Color(
            f"{iod_dict[iod_of_interest]}:O",
            scale=alt.Scale(
                domain=altair_domain, scheme=config["altair_scheme"], reverse=False
            ),
            title=iod_of_interest,
            legend=alt.Legend(orient="top"),
        ),
        alt.value("lightgray"),
    )

    # Creating the interactive map
    choro_region = (
        alt.Chart(geodata_la)
        .mark_geoshape(
            stroke="black",
        )
        .transform_lookup(
            lookup="lad19nm",
            from_=alt.LookupData(
                data,
                "lad19nm",
                ["lad19nm", "region_name"] + iod_indices,
            ),
        )
        .transform_filter(alt.FieldOneOfPredicate(field="lad19nm", oneOf=las_to_plot))
        .encode(
            color=color_las,
            tooltip=[alt.Tooltip("lad19nm:N", title="Local Authority")]
            + [
                alt.Tooltip(f"{ind}:O", title=name, format="1.2f")
                for ind, name in zip(iod_indices, iod_tooltip)
            ],
        )
        .project("identity", reflectY=True)
        .add_selection(la_select, la_select_all)
        .properties(width=500, height=500)
    )

    # Creating the bar chart
    choro_bar = (
        alt.Chart(la_melt)
        .mark_bar(color=nesta_colours[1])
        .encode(
            x=alt.X(
                "decile:Q",
                title="Decile",
                scale=alt.Scale(domain=[0, 10]),
                axis=alt.Axis(tickMinStep=1),
            ),
            y=alt.Y(
                "iod_name:N",
                title=" ",
                sort=iod_names,
                axis=alt.Axis(titlePadding=330),
            ),
        )
        .transform_filter(la_select_all)
        .properties(width=400, height=400)
    )

    # Adding text to the bar chart
    la_text = (
        alt.Chart(la_melt)
        .mark_text(dy=-210, size=20, color="darkgray")
        .encode(text="lad19nm:N")
        .transform_filter(la_select_all)
    )
    bar_chart = alt.layer(choro_bar, la_text)

    # Combines the two charts together and adds some configurations
    choro_region_la = alt.vconcat(choro_region, bar_chart, center=True).configure(
        **theme_altair
    )
    return choro_region_la
