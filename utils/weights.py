from geopandas import GeoDataFrame
from pandas import Series


def _create_weight_column(forecast_data: dict[str, GeoDataFrame]) -> dict[str, GeoDataFrame]:
    forecasts_with_weight_column = {}
    for offset in forecast_data.keys():
        forecast_data[offset]["weight"] = Series(dtype=float)
        forecasts_with_weight_column[offset] = forecast_data[offset]
    return forecasts_with_weight_column


def _get_weights(forecast_data: dict[str, GeoDataFrame]) -> dict[str, GeoDataFrame]:
    # For now, fill the weights with 1. At some point in the future we will have
    # a weights configuration file generated by data scientists.
    forecasts_with_weights = {}
    for offset in forecast_data.keys():
        forecast_data[offset]["weight"] = 1.0
        forecasts_with_weights[offset] = forecast_data[offset]
    print("Applied weighting factor.")
    return forecasts_with_weights


def apply_weights(forecast_data: dict[str, GeoDataFrame]) -> dict[str, GeoDataFrame]:
    forecast_data_with_column = _create_weight_column(forecast_data)
    weighted_data = _get_weights(forecast_data_with_column)
    return weighted_data