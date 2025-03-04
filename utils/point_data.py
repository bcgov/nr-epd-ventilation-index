from geopandas import GeoDataFrame, read_file


def _read_point_data() -> GeoDataFrame:
    # Read point data from data/point_data.csv
    print("Reading point data from data/point_data.csv...")
    return read_file("data/point_data.csv")


def _merge_point_data(
    point_data: GeoDataFrame, forecast_data: dict[str, GeoDataFrame]
) -> dict[str, dict[str, GeoDataFrame]]:
    # Ensure 'x' and 'y' columns are of the same type
    point_data["x"] = point_data["x"].astype(int)
    point_data["y"] = point_data["y"].astype(int)

    merged_data = {}
    for offset, data in forecast_data.items():
        # Ensure 'x' and 'y' columns are of the same type
        data["x"] = data["x"].astype(int)
        data["y"] = data["y"].astype(int)

        # Merge the point data with the forecast data
        print(f"Merging point data with forecast data for {offset}...")
        merged = data.merge(point_data, on=["x", "y"], how="left")

        # Rename "Metro Vancouver" to "Vancouver" in the merged DataFrame
        merged["zone"] = merged["zone"].replace("Metro Vancouver", "Vancouver")

        # Group by zone name
        for zone_name, group in merged.groupby("zone"):
            if not zone_name:  # Skip zones with no name
                continue
            if zone_name not in merged_data:
                merged_data[zone_name] = {}
            merged_data[zone_name][offset] = group

    return merged_data


def merge_point_data(forecast_data: dict[str, GeoDataFrame]) -> dict[str, dict[str, GeoDataFrame]]:
    # Read point data from data/point_data.csv and merge it with forecast data.
    point_data = _read_point_data()
    merged_data = _merge_point_data(point_data, forecast_data)
    return merged_data
