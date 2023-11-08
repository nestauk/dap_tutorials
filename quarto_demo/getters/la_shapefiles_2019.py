import altair as alt
import geopandas as gpd
from quarto_demo import PROJECT_DIR


def get_english_la_shapefiles_2019_gpd() -> gpd.GeoDataFrame:
    """Pulling in the English Local Authority (LA) shape files for 2019; with the England regions
    and LA codes/names. The Deciles are of the Average LSOA Score for each LA.
    See https://geoportal.statistics.gov.uk/search?collection=Dataset for the dataset.
    Note: You have to use a public url to pull in the shapefiles, it is an issue with altair/streamlit.
    Otherwise it won't plot the map.

    Returns:
        alt.Data: Data for Altair to produce the choropleths in streamlit.
    """
    geodata_la = gpd.read_file(
        str(PROJECT_DIR) + "/inputs/data/la_clean_shapefiles_2019_new.json"
    )

    return geodata_la
