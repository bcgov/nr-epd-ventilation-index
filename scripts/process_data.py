import sys
from xarray import load_dataset
from geopandas import GeoDataFrame, read_file, points_from_xy
from geopandas.tools import sjoin
from scipy.spatial import cKDTree

# Read in a GRIB2 Forecast file, a CSV file containing weights data, and a KML
# file containing zones data, and output a CSV file that allows the main program
# to directly address this information without needing to perform costly
# calculations at runtime.


def _read_forecast_data(filename: str) -> GeoDataFrame:
    # Loads an ECC Grib2 file and filters the data to only include BC. Returns a GeoDataFrame projected to web mercator.
    print(f"Reading forecast data from {filename}...")
    forecast_dataframe = load_dataset(filename, engine="cfgrib").to_dataframe().reset_index()
    # Filter the data to only include BC.
    # From https://catalogue.data.gov.bc.ca/dataset/legally-defined-administrative-areas-of-bc/resource/d70a242e-ebc5-4b3d-a418-38abefa03fb2
    print("Filtering data to only include BC...")
    forecast_for_bc_dataframe = forecast_dataframe[
        (forecast_dataframe["latitude"] > 48.0)
        & (forecast_dataframe["latitude"] < 60.0)
        & (forecast_dataframe["longitude"] > -139.5)
        & (forecast_dataframe["longitude"] < -113.5)
    ]
    cleaned_dataframe = forecast_for_bc_dataframe.drop(
        columns=["time", "step", "surface", "valid_time", "unknown"], axis=1
    )
    geodataframe = (
        GeoDataFrame(
            cleaned_dataframe,
            geometry=points_from_xy(cleaned_dataframe["longitude"], cleaned_dataframe["latitude"]),
        )
        .set_crs(epsg=4326)
        .to_crs(epsg=3857)
    )
    return geodataframe


def _read_weights_data(filename: str) -> GeoDataFrame:
    # Loads a CSV file containing weights data and returns a GeoDataFrame projected to web mercator.
    print(f"Reading weights data from {filename}...")
    weights_dataframe = read_file(filename)
    weights_geodataframe = (
        GeoDataFrame(weights_dataframe, geometry=points_from_xy(weights_dataframe["lon"], weights_dataframe["lat"]))
        .set_crs(epsg=4326)
        .to_crs(epsg=3857)
    )

    return weights_geodataframe


def _read_zones_data(filename: str) -> GeoDataFrame:
    # Loads a GeoJSON file containing zones data and returns a GeoDataFrame projected to web mercator.
    print(f"Reading zones data from {filename}...")
    zones_geodataframe = read_file(filename).to_crs(epsg=3857)
    print("Merging zones by name...")
    merged_zones_geodataframe = zones_geodataframe.dissolve(by="Name").reset_index().drop(columns=["Description"])
    return merged_zones_geodataframe


def _add_weights_and_zones_to_forecast_points(
    forecast_data: GeoDataFrame, weights_data: GeoDataFrame, zones_data: GeoDataFrame
) -> GeoDataFrame:
    # Add a weight column to the forecast data based on the nearest neighbour in the weights data.
    print("Determining the weight for each forecast point...")
    # Create a KDTree for fast spatial indexing
    weights_tree = cKDTree(weights_data.geometry.apply(lambda geom: (geom.x, geom.y)).tolist())
    # Query the KDTree for nearest neighbors
    _distances, indices = weights_tree.query(forecast_data.geometry.apply(lambda geom: (geom.x, geom.y)).tolist())
    # Assign the weights based on nearest neighbors
    forecast_data["weight"] = weights_data.iloc[indices]["cfactor"].values

    # Determine the name of the zone that each point resides within
    print("Determining the zone for each forecast point...")
    forecast_data_with_zones = sjoin(forecast_data, zones_data, how="left", predicate="within")
    forecast_data_with_zones = forecast_data_with_zones.rename(columns={"Name": "zone"})
    forecast_data_with_zones = forecast_data_with_zones.drop(columns=["index_right"])
    return forecast_data_with_zones


def _write_baked_data(baked_data: GeoDataFrame) -> None:
    # Write the baked data to a CSV file.
    print("Writing point data to data/baked_data.csv...")
    baked_data.to_csv("data/point_data.csv", index=False)


def _process_weights(forecast_filename: str, weights_filename: str, zones_filename: str) -> None:
    forecast_data = _read_forecast_data(forecast_filename)
    weights_data = _read_weights_data(weights_filename)
    zones_data = _read_zones_data(zones_filename)
    baked_data = _add_weights_and_zones_to_forecast_points(forecast_data, weights_data, zones_data)
    _write_baked_data(baked_data)


if __name__ == "__main__":
    # Accept the filename of a grib2 forecast file as a command line argument.
    if len(sys.argv) < 4:
        print("Usage: process_zones.py <forecast_filename> <weights_filename> <zones_filename>")
        sys.exit(1)

    _process_weights(sys.argv[1], sys.argv[2], sys.argv[3])
