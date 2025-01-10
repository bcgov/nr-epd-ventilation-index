from geopandas import GeoDataFrame

from utils.reducer import calculate_weighted_means


def test_calculate_weighted_means():
    data_1 = GeoDataFrame({"ventilation_index": [1.0, 2.0, 3.0], "weight": [0.5, 1.0, 1.5]})
    data_2 = GeoDataFrame({"ventilation_index": [2.0, 3.0, 4.0], "weight": [1.0, 1.0, 1.0]})
    grouped_forecast_data = {"zone_1": {"time_1": data_1, "time_2": data_2}}

    expected_result = {
        "zone_1": {
            "time_1": (1.0 * 0.5 + 2.0 * 1.0 + 3.0 * 1.5) / (0.5 + 1.0 + 1.5),
            "time_2": (2.0 * 1.0 + 3.0 * 1.0 + 4.0 * 1.0) / (1.0 + 1.0 + 1.0),
        }
    }

    result = calculate_weighted_means(grouped_forecast_data)

    assert result == expected_result
