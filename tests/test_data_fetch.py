import pytest
from freezegun import freeze_time

from utils.data_fetch import _build_urls


class TestBuildUrls:
    @freeze_time("2024-11-19")
    def test_urls_correct(self):
        offset1 = "012"
        offset2 = "024"
        offset3 = "048"
        url1 = "https://dd.weather.gc.ca/model_hrdps/continental/2.5km/00/012/20241119T00Z_MSC_HRDPS_VI_Sfc_RLatLon0.0225_PT012H.grib2"
        url2 = "https://dd.weather.gc.ca/model_hrdps/continental/2.5km/00/024/20241119T00Z_MSC_HRDPS_VI_Sfc_RLatLon0.0225_PT024H.grib2"
        url3 = "https://dd.weather.gc.ca/model_hrdps/continental/2.5km/00/048/20241119T00Z_MSC_HRDPS_VI_Sfc_RLatLon0.0225_PT048H.grib2"

        urls = _build_urls()

        assert offset1 in urls.keys()
        assert offset2 in urls.keys()
        assert offset3 in urls.keys()
        assert urls[offset1] == url1
        assert urls[offset2] == url2
        assert urls[offset3] == url3
