import lzma
import geopandas as gpd
import sys
import os

OUTPUT_FILENAME = "tmp/ventilation_index_zones.geojson"
COMPRESSED_OUTPUT_FILENAME = "data/ventilation_index_zones.geojson.xz"


def _read_zones_from_file(filename: str) -> gpd.GeoDataFrame:
    return gpd.read_file(filename)


def _merge_zones(unmerged_zones: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    # Dissolve zones with the same name. This will perform a union on the geometries.
    merged_zones = unmerged_zones.dissolve(by="Name")
    merged_zones.reset_index(inplace=True)
    return merged_zones


def _write_file(merged_zones: gpd.GeoDataFrame) -> None:
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    merged_zones.to_file(OUTPUT_FILENAME, driver="GeoJSON")


def _compress_file() -> None:
    # GitHub has a filesize limit of 50MB. The shapefile is 60MB, so it should be compressed at rest.
    with open(OUTPUT_FILENAME, "rb") as f_in:
        bytes = f_in.read()
    with lzma.open(COMPRESSED_OUTPUT_FILENAME, "w") as f_out:
        f_out.write(bytes)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: update_zones.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    print(f"Reading zones from {filename}...")
    unmerged_zones = _read_zones_from_file(filename)
    print("Merging zones...")
    merged_zones = _merge_zones(unmerged_zones)
    _write_file(merged_zones)
    print("Compressing file...")
    _compress_file()
    print(f"Compressed and wrote {merged_zones.shape[0]} zones to {OUTPUT_FILENAME}.")
    print(f"Commit and push {COMPRESSED_OUTPUT_FILENAME} to GitHub to apply the changes.")
