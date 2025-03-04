import pytest
from geopandas import GeoDataFrame
from utils.point_data import _merge_point_data


def test_merge_point_data():
    point_data = GeoDataFrame({"x": [1, 2, 3], "y": [4, 5, 6], "zone": ["Zone1", "Zone2", "Metro Vancouver"]})

    forecast_data = {
        "offset1": GeoDataFrame({"x": [1, 2, 3], "y": [4, 5, 6], "forecast": [10, 20, 30]}),
        "offset2": GeoDataFrame({"x": [1, 2, 3], "y": [4, 5, 6], "forecast": [40, 50, 60]}),
    }

    expected_output = {
        "Zone1": {
            "offset1": GeoDataFrame({"x": [1], "y": [4], "forecast": [10], "zone": ["Zone1"]}),
            "offset2": GeoDataFrame({"x": [1], "y": [4], "forecast": [40], "zone": ["Zone1"]}),
        },
        "Zone2": {
            "offset1": GeoDataFrame({"x": [2], "y": [5], "forecast": [20], "zone": ["Zone2"]}),
            "offset2": GeoDataFrame({"x": [2], "y": [5], "forecast": [50], "zone": ["Zone2"]}),
        },
        "Vancouver": {
            "offset1": GeoDataFrame({"x": [3], "y": [6], "forecast": [30], "zone": ["Vancouver"]}),
            "offset2": GeoDataFrame({"x": [3], "y": [6], "forecast": [60], "zone": ["Vancouver"]}),
        },
    }

    result = _merge_point_data(point_data, forecast_data)

    for zone, offsets in expected_output.items():
        for offset, expected_df in offsets.items():
            result_df = result[zone][offset].reset_index(drop=True)
            expected_df = expected_df.reset_index(drop=True)

            print(result_df)
            print(expected_df)
            # Assert that the columns are the same
            assert list(result_df.columns) == list(expected_df.columns), (
                f"Columns mismatch: {result_df.columns} != {expected_df.columns}"
            )

            # Assert that the values are the same
            for column in result_df.columns:
                assert result_df[column].equals(expected_df[column]), (
                    f"Values mismatch in column '{column}': {result_df[column].tolist()} != {expected_df[column].tolist()}"
                )
