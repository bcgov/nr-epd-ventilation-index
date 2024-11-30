from datetime import datetime
from pandas import DataFrame
from freezegun import freeze_time
from xarray import Dataset
from geopandas import GeoDataFrame

from utils.data_fetch import _build_geo_data_frames, _build_urls, _build_data_frames, _clean_data, _filter_data


@freeze_time("2024-11-19")
def test_build_urls():
    offset_1 = "012"
    offset_2 = "024"
    offset3 = "048"
    url_1 = "https://dd.weather.gc.ca/model_hrdps/continental/2.5km/00/012/20241119T00Z_MSC_HRDPS_VI_Sfc_RLatLon0.0225_PT012H.grib2"
    url_2 = "https://dd.weather.gc.ca/model_hrdps/continental/2.5km/00/024/20241119T00Z_MSC_HRDPS_VI_Sfc_RLatLon0.0225_PT024H.grib2"
    url_3 = "https://dd.weather.gc.ca/model_hrdps/continental/2.5km/00/048/20241119T00Z_MSC_HRDPS_VI_Sfc_RLatLon0.0225_PT048H.grib2"

    urls = _build_urls()

    assert offset_1 in urls.keys()
    assert offset_2 in urls.keys()
    assert offset3 in urls.keys()
    assert urls[offset_1] == url_1
    assert urls[offset_2] == url_2
    assert urls[offset3] == url_3


def test_build_dataframes():
    # This is an extremely minimal example of the structure of the data I've
    # seen from Environment Canada for my purposes. I'm no data scientist,
    # however.
    dataset_1 = Dataset(
        {
            "unknown": (["loc"], [0.50]),
            "latitude": (["loc"], [49]),
            "longitude": (["loc"], [-130]),
        },
        coords={
            "x": (["loc"], [1]),
            "y": (["loc"], [1]),
        },
    )
    dataset_2 = Dataset(
        {
            "unknown": (["loc"], [0.43]),
            "latitude": (["loc"], [49]),
            "longitude": (["loc"], [-130]),
        },
        coords={
            "x": (["loc"], [1]),
            "y": (["loc"], [1]),
        },
    )

    datasets = {
        "012": dataset_1,
        "024": dataset_2,
    }

    result = _build_data_frames(datasets)

    assert "012" in result
    assert isinstance(result["012"], DataFrame)
    assert "024" in result
    assert isinstance(result["024"], DataFrame)


def test_filter_data():
    data_frame_1 = DataFrame(
        [
            {
                "y": 1,
                "x": 1,
                "latitude": 49,
                "longitude": -130,
                "unknown": 0.50,
            },
            {
                "y": 2,
                "x": 1,
                "latitude": 49,
                "longitude": -150,
                "unknown": 0.67,
            },
        ]
    )
    data_frame_2 = DataFrame(
        [
            {
                "y": 1,
                "x": 1,
                "latitude": 49,
                "longitude": -130,
                "unknown": 0.43,
            },
            {
                "y": 2,
                "x": 1,
                "latitude": 49,
                "longitude": -150,
                "unknown": 0.21,
            },
        ]
    )
    data_frames = {
        "012": data_frame_1,
        "024": data_frame_2,
    }

    result = _filter_data(data_frames)

    assert "012" in result
    test_frame_1 = result["012"]
    assert test_frame_1[test_frame_1["longitude"] == -150].empty

    assert "024" in result
    test_frame_2 = result["024"]
    assert test_frame_2[test_frame_2["longitude"] == -150].empty


def test_clean_data():
    data_frame_1 = DataFrame(
        [
            {
                "y": 1,
                "x": 1,
                "time": datetime.now(),
                "step": 1,
                "surface": 0,
                "valid_time": 24,
                "latitude": 49,
                "longitude": -130,
                "unknown": 0.50,
            },
        ]
    )
    data_frame_2 = DataFrame(
        [
            {
                "y": 1,
                "x": 1,
                "time": datetime.now(),
                "step": 1,
                "surface": 0,
                "valid_time": 24,
                "latitude": 49,
                "longitude": -130,
                "unknown": 0.43,
            },
        ]
    )
    data_frames = {
        "012": data_frame_1,
        "024": data_frame_2,
    }

    result = _clean_data(data_frames)

    assert "012" in result
    test_frame_1 = result["012"]
    assert "time" not in test_frame_1.columns.values
    assert "step" not in test_frame_1.columns.values
    assert "surface" not in test_frame_1.columns.values
    assert "valid_time" not in test_frame_1.columns.values
    assert "x" in test_frame_1.columns.values
    assert "y" in test_frame_1.columns.values
    assert "latitude" in test_frame_1.columns.values
    assert "longitude" in test_frame_1.columns.values
    assert "ventilation_index" in test_frame_1.columns.values

    assert "024" in result
    test_frame_2 = result["012"]
    assert "time" not in test_frame_2.columns.values
    assert "step" not in test_frame_2.columns.values
    assert "surface" not in test_frame_2.columns.values
    assert "valid_time" not in test_frame_2.columns.values
    assert "x" in test_frame_2.columns.values
    assert "y" in test_frame_2.columns.values
    assert "latitude" in test_frame_2.columns.values
    assert "longitude" in test_frame_2.columns.values
    assert "ventilation_index" in test_frame_2.columns.values


def test_build_geo_data_frames():
    # This test generates false warnings. See:
    # https://github.com/geopandas/geopandas/issues/3430
    # https://github.com/pyproj4/pyproj/issues/1307
    data_frame_1 = DataFrame(
        [
            {
                "y": 1,
                "x": 1,
                "latitude": 49,
                "longitude": -130,
                "ventilation_index": 0.50,
            },
        ]
    )
    data_frame_2 = DataFrame(
        [
            {
                "y": 1,
                "x": 1,
                "latitude": 49,
                "longitude": -130,
                "ventilation_index": 0.43,
            },
        ]
    )
    data_frames = {
        "012": data_frame_1,
        "024": data_frame_2,
    }

    result = _build_geo_data_frames(data_frames)

    assert "012" in result
    geo_data_frame_1 = result["012"]
    assert isinstance(geo_data_frame_1, GeoDataFrame)
    assert "geometry" in geo_data_frame_1.columns.values
    assert geo_data_frame_1.crs.name == "WGS 84 / Pseudo-Mercator"

    assert "024" in result
    geo_data_frame_2 = result["024"]
    assert isinstance(geo_data_frame_2, GeoDataFrame)
    assert "geometry" in geo_data_frame_2.columns.values
    assert geo_data_frame_2.crs.name == "WGS 84 / Pseudo-Mercator"
