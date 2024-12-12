from geopandas import points_from_xy, GeoDataFrame
from numpy import nan
from numpy.testing import assert_equal
from pandas import DataFrame

from utils.weights import _create_weight_column, _apply_weight_of_1


def test_create_weights_column():
    test_data_frame_1 = DataFrame(
        [
            {"x": 0, "y": 0, "latitude": 49, "longitude": -130, "ventilation_index": 0.43},
            {"x": 0, "y": 1, "latitude": 49, "longitude": -131, "ventilation_index": 0.44},
        ]
    )
    test_data_frame_2 = DataFrame(
        [
            {"x": 0, "y": 0, "latitude": 49, "longitude": -130, "ventilation_index": 0.50},
            {"x": 0, "y": 1, "latitude": 49, "longitude": -131, "ventilation_index": 0.51},
        ]
    )
    test_geo_data_frame_1 = GeoDataFrame(
        test_data_frame_1, geometry=points_from_xy(test_data_frame_1["longitude"], test_data_frame_1["latitude"])
    )
    test_geo_data_frame_2 = GeoDataFrame(
        test_data_frame_2, geometry=points_from_xy(test_data_frame_2["longitude"], test_data_frame_2["latitude"])
    )
    test_geo_data_frame_1.set_crs(epsg=4326, inplace=True)
    test_geo_data_frame_2.set_crs(epsg=4326, inplace=True)
    test_geo_data_frame_1.to_crs(epsg=3857, inplace=True)
    test_geo_data_frame_2.to_crs(epsg=3857, inplace=True)
    test_data = {
        "012": test_geo_data_frame_1,
        "024": test_geo_data_frame_2,
    }

    result = _create_weight_column(test_data)

    assert "012" in result
    geo_data_frame_with_weight_column_1 = result["012"]
    assert "weight" in geo_data_frame_with_weight_column_1.columns.values
    assert_equal(geo_data_frame_with_weight_column_1.loc[0]["weight"], nan)
    assert_equal(geo_data_frame_with_weight_column_1.loc[1]["weight"], nan)

    assert "024" in result
    geo_data_frame_with_weight_column_2 = result["024"]
    assert "weight" in geo_data_frame_with_weight_column_2.columns.values
    assert_equal(geo_data_frame_with_weight_column_2.loc[0]["weight"], nan)
    assert_equal(geo_data_frame_with_weight_column_2.loc[1]["weight"], nan)


def test_get_weights():
    test_data_frame_1 = DataFrame(
        [
            {"x": 0, "y": 0, "latitude": 49, "longitude": -130, "ventilation_index": 0.43, "weight": nan},
            {"x": 0, "y": 1, "latitude": 49, "longitude": -131, "ventilation_index": 0.44, "weight": nan},
        ]
    )
    test_data_frame_2 = DataFrame(
        [
            {"x": 0, "y": 0, "latitude": 49, "longitude": -130, "ventilation_index": 0.50, "weight": nan},
            {"x": 0, "y": 1, "latitude": 49, "longitude": -131, "ventilation_index": 0.51, "weight": nan},
        ]
    )
    test_geo_data_frame_1 = GeoDataFrame(
        test_data_frame_1, geometry=points_from_xy(test_data_frame_1["longitude"], test_data_frame_1["latitude"])
    )
    test_geo_data_frame_2 = GeoDataFrame(
        test_data_frame_2, geometry=points_from_xy(test_data_frame_2["longitude"], test_data_frame_2["latitude"])
    )
    test_geo_data_frame_1.set_crs(epsg=4326, inplace=True)
    test_geo_data_frame_2.set_crs(epsg=4326, inplace=True)
    test_geo_data_frame_1.to_crs(epsg=3857, inplace=True)
    test_geo_data_frame_2.to_crs(epsg=3857, inplace=True)
    test_data = {
        "012": test_geo_data_frame_1,
        "024": test_geo_data_frame_2,
    }

    result = _apply_weight_of_1(test_data)

    assert "012" in result
    geo_data_frame_with_weights_1 = result["012"]
    assert geo_data_frame_with_weights_1.loc[0]["weight"] == 1.0
    assert geo_data_frame_with_weights_1.loc[1]["weight"] == 1.0

    assert "024" in result
    geo_data_frame_with_weights_2 = result["024"]
    assert geo_data_frame_with_weights_2.loc[0]["weight"] == 1.0
    assert geo_data_frame_with_weights_2.loc[1]["weight"] == 1.0
