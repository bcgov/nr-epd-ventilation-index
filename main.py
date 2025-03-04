from utils.checker import needs_to_run
from utils.forecast import fetch_and_clean_data
from utils.output import generate_forecast_text_file
from utils.point_data import merge_point_data
from utils.reducer import calculate_weighted_means


def main():
    if needs_to_run():
        forecast_data = fetch_and_clean_data()
        forecast_data_with_extra_point_data = merge_point_data(forecast_data)
        weighted_means_data = calculate_weighted_means(forecast_data_with_extra_point_data)
        generate_forecast_text_file(weighted_means_data)
    else:
        print("Forecast already generated today.")


if __name__ == "__main__":
    main()
