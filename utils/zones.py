import lzma

from geopandas import read_file, GeoDataFrame

COMPRESSED_FILEPATH = "./data/ventilation_index_zones.geojson.xz"
DECOMPRESSED_FILEPATH = "./tmp/ventilation_index_zones.geojson"


def _decompress_ventilation_index_zones() -> None:
    with lzma.open(COMPRESSED_FILEPATH, "r") as f_in:
        bytes = f_in.read()
    with open(DECOMPRESSED_FILEPATH, "wb") as f_out:
        f_out.write(bytes)


def get_ventilation_index_zones() -> GeoDataFrame:
    # The zones data frame has columns: Name, Geometry
    _decompress_ventilation_index_zones()
    ventilation_index_zones = read_file(DECOMPRESSED_FILEPATH)
    # Re-project zones data from WGS 84 to web mercator to be compatible with
    # the forecast data.
    ventilation_index_zones.to_crs(epsg=3857, inplace=True)
    print(f"Loaded {ventilation_index_zones.shape[0]} ventilation index zones.")
    return ventilation_index_zones


if __name__ == "__main__":
    get_ventilation_index_zones()
