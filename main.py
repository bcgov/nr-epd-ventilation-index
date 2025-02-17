from utils.checker import needs_to_run
from utils.forecast import fetch_and_clean_data
from utils.grouping import group_forecast_data
from utils.output import generate_forecast_text_file
from utils.weights import apply_weights_simple
from utils.zones import get_ventilation_index_zones
from utils.reducer import calculate_weighted_means


def main():
    if needs_to_run():
        forecast_data = fetch_and_clean_data()
        weighted_forecast_data = apply_weights_simple(forecast_data)
        ventilation_index_zones = get_ventilation_index_zones()
        grouped_forecast_data = group_forecast_data(weighted_forecast_data, ventilation_index_zones)
        weighted_means_data = calculate_weighted_means(grouped_forecast_data)
        generate_forecast_text_file(weighted_means_data)
    else:
        print("Forecast already generated today.")


if __name__ == "__main__":
    main()
