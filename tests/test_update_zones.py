import geopandas as gpd
from pandas import DataFrame
from scripts.update_zones import _merge_zones

def test_merge_zones():
    test_data_frame = DataFrame(
        [
            {"Name": "Zone1", "geometry": "POINT (1 1)"},
            {"Name": "Zone1", "geometry": "POINT (2 2)"},
            {"Name": "Zone2", "geometry": "POINT (3 3)"},
        ]
    )
    test_geo_data_frame = gpd.GeoDataFrame(test_data_frame, geometry=gpd.points_from_xy([1, 2, 3], [1, 2, 3]))
    test_geo_data_frame.set_crs(epsg=4326, inplace=True)

    result = _merge_zones(test_geo_data_frame)

    assert result.shape[0] == 2
    assert "Zone1" in result["Name"].values
    assert "Zone2" in result["Name"].values