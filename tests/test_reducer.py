from geopandas import GeoDataFrame
import pytest
from utils.reducer import calculate_weighted_means

def test_calculate_weighted_means():
    data = {
        "zone1": {
            "012": GeoDataFrame({"ventilation_index": [10, 20, 30], "weight": [1, 2, 3]}),
            "024": GeoDataFrame({"ventilation_index": [40, 50, 60], "weight": [4, 5, 6]}),
        },
        "zone2": {"012": GeoDataFrame({"ventilation_index": [70, 80, 90], "weight": [7, 8, 9]})},
    }

    expected_result = {
        "zone1": {
            "012": pytest.approx(23.333333333333332),
            "024": pytest.approx(51.333333333333336),
        },
        "zone2": {"012": pytest.approx(80.83333333333)},
    }

    result = calculate_weighted_means(data)
    for zone, forecasts in expected_result.items():
        for time, expected_value in forecasts.items():
            assert float(result[zone][time]) == expected_value