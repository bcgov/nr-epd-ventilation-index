from forecast import fetch_and_clean_data
from weights import apply_weights_simple


OUTPUT_FILEPATH = "./tmp/sample.csv"


def generate_csv_sample() -> None:
    # Generate a sample csv file that can be ingested by the weighting algorithm.
    forecasts = fetch_and_clean_data()
    single_forecast = {"012": forecasts["012"]}
    weighted_forecast = apply_weights_simple(single_forecast)

    weighted_forecast["012"].to_csv(OUTPUT_FILEPATH, columns=["y", "x", "latitude", "longitude", "weight"], index=False)


if __name__ == "__main__":
    generate_csv_sample()
