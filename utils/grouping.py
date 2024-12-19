from geopandas import GeoDataFrame


def group_forecast_data(
    forecast_data: dict[str, GeoDataFrame], zones_data: GeoDataFrame
) -> dict[str, dict[str, GeoDataFrame]]:
    grouped_forecast_data = {}

    for _index, zone_row in zones_data.iterrows():
        zone_name = zone_row["name"]
        zone_geometry = zone_row["geometry"]

        grouped_forecast_data[zone_name] = {}

        for forecast_time, forecast in forecast_data.items():
            grouped_forecast_data[zone_name][forecast_time] = forecast[forecast["geometry"].within(zone_geometry)]
            num_data_points = grouped_forecast_data[zone_name][forecast_time].shape[0]
            print(f"Grouped {num_data_points} data points for forecast {forecast_time} of {zone_name}")

    return grouped_forecast_data
