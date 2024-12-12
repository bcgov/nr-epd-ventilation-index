from geopandas import read_file, GeoDataFrame


def get_ventilation_index_zones() -> GeoDataFrame:
    ventilation_index_zones: GeoDataFrame = read_file("./data/ventilation_index_zones.geojson")
    print(f"loaded {ventilation_index_zones.shape[0]} ventilation index zones.")
    return ventilation_index_zones


if __name__ == "__main__":
    get_ventilation_index_zones()
