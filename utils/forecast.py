from datetime import date
from os import makedirs
from urllib.error import URLError
from urllib.request import urlretrieve
from pandas import DataFrame
from xarray import load_dataset, Dataset
from geopandas import points_from_xy, GeoDataFrame


BASE_URL = "https://dd.weather.gc.ca/model_hrdps/continental/2.5km"
OFFSETS = ["012", "024", "048"]


def _build_urls_for_posting_time(posting_time: str) -> dict[str, str]:
    # The url for the data sources will be a combination of yesterday's date,
    # plus an offset in number of hours (UTC) into the future for the forecast.
    # To build the report I need to fetch the 12, 24, and 48 hour forecast data
    # for the data posted at 00 (midnight).
    urls: dict[str, str] = {}
    # The date in the filename is represented as "YYYYmmdd"
    today = date.today().strftime("%Y%m%d")
    for offset in OFFSETS:
        urls[offset] = (
            f"{BASE_URL}/{posting_time}/{offset}/{today}T{posting_time}Z_MSC_HRDPS_VI_Sfc_RLatLon0.0225_PT{offset}H.grib2"
        )

    info = "\n".join([url for _, url in urls.items()])
    print(f"Generated URLs:\n{info}\n")

    return urls

def _try_urls(urls: dict[str, str]) -> None:
    for offset, url in urls.items():
        print(f"Fetching {url}...")
        urlretrieve(url, f"./tmp/{offset}.grib2")
    print("Done.\n")


def _fetch_data(urls: dict[str, str]) -> None:
    # Download the 12h, 24h, and 48h ventilation index forecast files from the
    # Environment Canada data-mart.
    print("Trying to fetch data for the 00 posting time.")
    urls = _build_urls_for_posting_time("00")
    try:
        _try_urls(urls)
    except URLError:
        print("Failed to fetch data for the 00 posting time. Trying the 06 posting time.")
        urls = _build_urls_for_posting_time("06")
        try:
            _try_urls(urls)
        except URLError:
            print("Failed to fetch data for the 06 posting time. Trying the 12 posting time.")
            urls = _build_urls_for_posting_time("12")
            try:
                _try_urls(urls)
            except URLError:
                print("Failed to fetch data for the 12 posting time. Trying the 18 posting time.")
                urls = _build_urls_for_posting_time("18")
                try:
                    _try_urls(urls)
                except URLError:
                    print("Failed to fetch data for the 18 posting time. Exiting.")
                    exit(1)


def _read_data() -> dict[str, Dataset]:
    # Load the data from files into memory.
    datasets: dict[str, Dataset] = {}
    for offset in OFFSETS:
        datasets[offset] = load_dataset(f"./tmp/{offset}.grib2", engine="cfgrib")

    num_data_points = sum([dataset.sizes["x"] * dataset.sizes["y"] for dataset in datasets.values()])
    print(f"Loaded {num_data_points} data points.")

    return datasets


def _build_data_frames(datasets: dict[str, Dataset]) -> dict[str, DataFrame]:
    data_frames: dict[str, DataFrame] = {}
    for offset in datasets.keys():
        data_frames[offset] = datasets[offset].to_dataframe().reset_index()

    return data_frames


def _filter_data(canada_data_frames: dict[str, Dataset]) -> dict[str, DataFrame]:
    # Filter the data to only include BC.
    # From https://catalogue.data.gov.bc.ca/dataset/legally-defined-administrative-areas-of-bc/resource/d70a242e-ebc5-4b3d-a418-38abefa03fb2
    bc_data_frames: dict[str, DataFrame] = {}
    for offset in canada_data_frames.keys():
        canada_data_frame = canada_data_frames[offset]

        # Filter to the legal bounds of BC.
        bc_data_frames[offset] = canada_data_frame[
            (canada_data_frame["latitude"] > 48.0)
            & (canada_data_frame["latitude"] < 60.0)
            & (canada_data_frame["longitude"] > -139.5)
            & (canada_data_frame["longitude"] < -113.5)
        ]

    num_data_points = sum([data_frame.shape[0] for data_frame in bc_data_frames.values()])
    print(f"Filtered data to {num_data_points} data points.")

    return bc_data_frames


def _clean_data(data_frames: dict[str, DataFrame]) -> dict[str, DataFrame]:
    # Filter unused columns.
    trimmed_data_frames: dict[str, DataFrame] = {}
    for offset in data_frames.keys():
        data_frame = data_frames[offset]
        trimmed_data_frames[offset] = data_frame.drop(columns=["time", "step", "surface", "valid_time"], axis=1)

    # There is no label for the ventilation index column, so it gets the default label of "unknown".
    renamed_data_frames: dict[str, DataFrame] = {}
    for offset in data_frames.keys():
        data_frame = trimmed_data_frames[offset]
        renamed_data_frames[offset] = data_frame.rename(columns={"unknown": "ventilation_index"})

    print("Cleaned DataFrames.")
    return renamed_data_frames


def _build_geo_data_frames(data_frames: dict[str, DataFrame]) -> dict[str, GeoDataFrame]:
    geo_data_frames: dict[str, GeoDataFrame] = {}
    for offset in data_frames.keys():
        geo_data_frame = GeoDataFrame(
            data_frames[offset],
            geometry=points_from_xy(data_frames[offset]["longitude"], data_frames[offset]["latitude"]),
        )
        # This is the CRS for the 1984 GPS standard (latitude/longitude).
        geo_data_frame.set_crs(epsg=4326, inplace=True)
        # Converting it to web mercator to be compatible with ventilation index
        # zones.
        geo_data_frame.to_crs(epsg=3857, inplace=True)
        geo_data_frames[offset] = geo_data_frame

    print("Built GeoDataFrames.")
    return geo_data_frames


def fetch_and_clean_data() -> dict[str, GeoDataFrame]:
    # The final data frame will have columns: y, x, latitude, longitude, ventilation_index, geometry
    makedirs("./tmp", exist_ok=True)

    _fetch_data()
    datasets = _read_data()
    data_frames = _build_data_frames(datasets)
    filtered_data_frames = _filter_data(data_frames)
    clean_data_frames = _clean_data(filtered_data_frames)
    geo_data_frames = _build_geo_data_frames(clean_data_frames)

    return geo_data_frames


if __name__ == "__main__":
    fetch_and_clean_data()
