from freezegun import freeze_time

from utils.output import _generate_report_text, _get_report_data


@freeze_time("2024-11-19 08:00:00")
def test_generate_forecast_text_file():
    forecast_data = {
        "Fraser Canyon": {
            "012": 25.0,
            "024": 45.0,
            "048": 75.0,
        },
        "Kamloops": {
            "012": 30.0,
            "024": 50.0,
            "048": 80.0,
        },
    }

    filename, content = _generate_report_text(forecast_data)

    expected_content = """FLCN39 CWVR 191400
SMOKE CONTROL FORECAST FOR THE BC AND YUKON ISSUED BY ENVIRONMENT CANADA AT 7:00 AM PST
TUESDAY 19 NOVEMBER 2024 FOR TODAY.

MIXING HEIGHTS IN METRES ABOVE SEA LEVEL.  AVERAGE WINDS IN KM/H.

19-NOVEMBER-2024
BRITISH COLUMBIA                                TODAY                      TOMORROW
                     7:00 AM                    4:00 PM                    4:00 PM
                     VI         WND     MXG HT  VI         WND     MXG HT  VI         WND     MXG HT
                                KM/H    M                  KM/H    M                  KM/H    M
FRASER CANYON        25/POOR    NA      NA      45/FAIR    NA      NA      75/GOOD    NA      NA
KAMLOOPS             30/POOR    NA      NA      50/FAIR    NA      NA      80/GOOD    NA      NA


VENTILATION GUIDELINES:
POOR:   0-33
FAIR:   34-54
GOOD:   55-100
VENTILATION INDICES NORMALLY DROP TO POOR AFTER SUNSET.


END/
"""
    assert content == expected_content
    assert filename == "FLCN39_CWVR_2024-11-19.txt"

def test_get_report_data():
    forecast_data = {
        "Fraser Canyon": {
            "012": 25.0,
            "024": 45.0,
            "048": 75.0,
        },
        "Kamloops": {
            "012": 30.0,
            "024": 50.0,
            "048": 80.0,
        },
    }

    expected_report_data = """FRASER CANYON        25/POOR    NA      NA      45/FAIR    NA      NA      75/GOOD    NA      NA
KAMLOOPS             30/POOR    NA      NA      50/FAIR    NA      NA      80/GOOD    NA      NA"""

    assert _get_report_data(forecast_data) == expected_report_data


def test_get_report_data_with_na_values():
    forecast_data = {
        "Fraser Canyon": {
            "012": float("nan"),
            "024": 45.0,
            "048": 75.0,
        },
        "Kamloops": {
            "012": 30.0,
            "024": float("nan"),
            "048": 80.0,
        },
    }

    expected_report_data = """FRASER CANYON        NA         NA      NA      45/FAIR    NA      NA      75/GOOD    NA      NA
KAMLOOPS             30/POOR    NA      NA      NA         NA      NA      80/GOOD    NA      NA"""

    assert _get_report_data(forecast_data) == expected_report_data