import datetime


BASE_URL = "https://dd.weather.gc.ca/model_hrdps/continental/2.5km"
OFFSETS = ["012", "024", "048"]
POSTING_TIME = "00"


def _build_urls() -> dict[str, str]:
    # The url for the data sources will be a combination of yesterday's date,
    # plus an offset in number of hours (UTC) into the future for the forecast.
    # To build the report I need to fetch the 12, 24, and 48 hour forecast data
    # for the data posted at 00 (midnight).
    urls: dict[str, str] = {}
    # The date in the filename is represented as "YYYYmmdd"
    today = datetime.date.today().strftime("%Y%m%d")
    for offset in OFFSETS:
        urls[offset] = (
            f"{BASE_URL}/{POSTING_TIME}/{offset}/{today}T{POSTING_TIME}Z_MSC_HRDPS_VI_Sfc_RLatLon0.0225_PT{offset}H.grib2"
        )
    info = "\n".join([url for _, url in urls.items()])
    print(f"Generated URLs:\n{info}\n")

    return urls


def fetch_and_clean_data():
    urls = _build_urls()
    pass
