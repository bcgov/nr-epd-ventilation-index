from utils.forecast import fetch_and_clean_data
from utils.weights import apply_weights


def main():
    forecast_data = fetch_and_clean_data()
    weighted_forecast_data = apply_weights(forecast_data)


if __name__ == "__main__":
    main()
