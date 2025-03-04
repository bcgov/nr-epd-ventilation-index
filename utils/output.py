from datetime import datetime
from os import makedirs
import pandas as pd

REPORTS_DIR = "reports/"

# Mapping the zone names used by BC to the zone names from the legacy report
# produced by Environment Canada.
ZONE_NAME_MAP = {
    "Fraser Canyon": "FRASER CANYON",
    "Kamloops": "KAMLOOPS",
    "Okanagan": "OKANAGAN",
    "Salmon Arm": "SALMON ARM",
    "Castlegar": "CASTLEGAR",
    "Cranbrook": "CRANBROOK",
    "Revelstoke": "REVELSTOKE",
    "Golden": "GOLDEN",
    "Sparwood": "SPARWOOD",
    "Clearwater": "CLEARWATER",
    "Quesnel": "QUESNEL",
    "100 Mile House": "100 MILE",
    "Williams Lake": "WILLIAMS LAKE",
    "Puntzi Mountain": "PUNTZI MTN",
    "McBride": "MCBRIDE",
    "Prince George": "PRINCE GEORGE",
    "Vanderhoof": "VANDERHOOF",
    "Burns Lake": "BURNS LAKE",
    "Smithers": "SMITHERS",
    "Mackenzie": "MACKENZIE",
    "Chetwynd": "CHETWYND",
    "Fort St John": "FT ST JOHN",
    "Fort Nelson": "FORT NELSON",
    "Watson Lake": "WATSON LAKE",
    "Atlin": "ATLIN",
    "Dease Lake": "DEASE LAKE",
    "Vancouver": "VANCOUVER",
    "Fraser Valley": "FRASER VALLEY",
    "Squamish": "SQUAMISH",
    "Pemberton": "PEMBERTON",
    "Sechelt": "SECHELT",
    "Powell River": "POWELL RIVER",
    "South Vancouver Island": "SRN VAN ISLD",
    "Central Vancouver Island": "CNTRL VAN ISLD",
    "Tofino": "TOFINO",
    "North Vancouver Island": "NRN VAN ISLD",
    "Bella Coola": "BELLA COOLA",
    "Terrace": "TERRACE",
    "Prince Rupert": "PRINCE RUPERT",
    "Haida Gwaii": "SANDSPIT",
    "Stewart": "STEWART",
}


def _get_vi_report(value: int) -> str:
    if value <= 33:
        return f"{value}/POOR"
    if value <= 54:
        return f"{value}/FAIR"
    return f"{value}/GOOD"


def _get_report_data(forecast_data: dict[str, dict[str, float]]) -> str:
    # The expect format for the data structure is:
    # {
    #     "zone_name": {
    #         "012": 0.0,
    #         "024": 0.0,
    #         "048": 0.0,
    #     },
    # }
    lines = []
    for zone_name, forecast in forecast_data.items():
        zone_name = ZONE_NAME_MAP[zone_name]

        vi_now = round(forecast["012"]) if not pd.isna(forecast["012"]) else "NA"
        vi_today = round(forecast["024"]) if not pd.isna(forecast["024"]) else "NA"
        vi_tomorrow = round(forecast["048"]) if not pd.isna(forecast["048"]) else "NA"

        report_now = _get_vi_report(vi_now) if vi_now != "NA" else "NA"
        report_today = _get_vi_report(vi_today) if vi_today != "NA" else "NA"
        report_tomorrow = _get_vi_report(vi_tomorrow) if vi_tomorrow != "NA" else "NA"

        lines.append(
            f"{zone_name:<20} {report_now:<7}    NA      NA      {report_today:<7}    NA      NA      {report_tomorrow:<7}    NA      NA"
        )

    return "\n".join(lines)


def _generate_report_text(forecast_data: dict[str, dict[str, float]]) -> tuple[str, str]:
    now = datetime.now()
    day_of_month = now.strftime("%d")
    dst = "PDT" if now.tzname() == "PDT" else "PST"
    time_of_issue_utc = "1400" if dst == "PST" else "1300"
    full_date = now.strftime("%A %-d %B %Y").upper()
    short_date = now.strftime("%-d-%B-%Y").upper()
    report_data = _get_report_data(forecast_data)
    filename = f"FLCN39_CWVR_{now.strftime('%Y-%m-%d')}.txt"

    output = f"""FLCN39 CWVR {day_of_month}{time_of_issue_utc}
SMOKE CONTROL FORECAST FOR THE BC AND YUKON ISSUED BY ENVIRONMENT CANADA AT 7:00 AM {dst}
{full_date} FOR TODAY.

MIXING HEIGHTS IN METRES ABOVE SEA LEVEL.  AVERAGE WINDS IN KM/H.

{short_date}
BRITISH COLUMBIA                                TODAY                      TOMORROW
                     7:00 AM                    4:00 PM                    4:00 PM
                     VI         WND     MXG HT  VI         WND     MXG HT  VI         WND     MXG HT
                                KM/H    M                  KM/H    M                  KM/H    M
{report_data}


VENTILATION GUIDELINES:
POOR:   0-33
FAIR:   34-54
GOOD:   55-100
VENTILATION INDICES NORMALLY DROP TO POOR AFTER SUNSET.


END/
"""

    return filename, output


def generate_forecast_text_file(forecast_data: dict[str, dict[str, float]]) -> None:
    filename, output = _generate_report_text(forecast_data)

    print(f"outputting to file {REPORTS_DIR}{filename}")
    print("==============")
    print(output)

    makedirs(REPORTS_DIR, exist_ok=True)
    with open(f"{REPORTS_DIR}{filename}", "w") as f:
        f.write(output)
