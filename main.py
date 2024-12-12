from utils.forecast import fetch_and_clean_data
from utils.weights import apply_weights
from utils.zones import get_ventilation_index_zones


def main():
    forecast_data = fetch_and_clean_data()
    weighted_forecast_data = apply_weights(forecast_data)
    ventilation_index_zones = get_ventilation_index_zones()


if __name__ == "__main__":
    main()
