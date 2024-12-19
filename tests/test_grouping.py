from geopandas import GeoDataFrame, points_from_xy
from pandas import DataFrame
from shapely import Polygon

from utils.grouping import group_forecast_data


def test_group_forecast_data():
    test_data_frame_1 = DataFrame(
        [
            {"x": 0, "y": 0, "latitude": 49, "longitude": -130, "ventilation_index": 0.43},
            {"x": 0, "y": 1, "latitude": 49, "longitude": -132, "ventilation_index": 0.44},
        ]
    )
    test_data_frame_2 = DataFrame(
        [
            {"x": 0, "y": 0, "latitude": 49, "longitude": -130, "ventilation_index": 0.50},
            {"x": 0, "y": 1, "latitude": 49, "longitude": -132, "ventilation_index": 0.51},
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

    test_zone_polygon_1 = Polygon(((-131.0, 48.0), (-131.0, 50.0), (-129.0, 50.0), (-129.0, 48.0), (-131.0, 48.0)))
    test_zone_polygon_2 = Polygon(((-133.0, 48.0), (-133.0, 50.0), (-131.0, 50.0), (-131.0, 48.0), (-133.0, 48.0)))
    test_zones = GeoDataFrame(
        [
            {"name": "Zone 1", "geometry": test_zone_polygon_1},
            {"name": "Zone 2", "geometry": test_zone_polygon_2},
        ]
    )
    test_zones.set_crs(epsg=4326, inplace=True)
    test_zones.to_crs(epsg=3857, inplace=True)

    result = group_forecast_data(test_data, test_zones)

    assert "Zone 1" in result
    assert "012" in result["Zone 1"]
    assert "024" in result["Zone 1"]
    assert result["Zone 1"]["012"].loc[0]["ventilation_index"] == 0.43
    assert result["Zone 1"]["024"].loc[0]["ventilation_index"] == 0.50

    assert "Zone 2" in result
    assert "012" in result["Zone 2"]
    assert "024" in result["Zone 2"]
    assert result["Zone 2"]["012"].loc[1]["ventilation_index"] == 0.44
    assert result["Zone 2"]["024"].loc[1]["ventilation_index"] == 0.51
