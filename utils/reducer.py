from geopandas import GeoDataFrame
import pandas as pd

def calculate_weighted_means(grouped_forecast_data: dict[dict[str, GeoDataFrame]]) -> dict[dict[str, float]]:
    result = {}
    for zone_name, forecasts in grouped_forecast_data.items():
        for forecast_time, data in forecasts.items():
            # Ensure 'ventilation_index' and 'weight' columns are numeric
            data["ventilation_index"] = pd.to_numeric(data["ventilation_index"], errors="coerce")
            data["weight"] = pd.to_numeric(data["weight"], errors="coerce")

            # Weighted mean is the sum of the product of the values and weights
            # divided by the sum of the weights.
            weighted_mean = (data["ventilation_index"] * data["weight"]).sum() / data["weight"].sum()
            if zone_name not in result:
                result[zone_name] = {}
            result[zone_name][forecast_time] = weighted_mean
            print(f"Calculated weighted mean for {zone_name} at {forecast_time}: {weighted_mean}")
    return result
