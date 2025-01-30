import os
from datetime import datetime


def needs_to_run():
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_path = f"./reports/FLCN39_CWVR_{date_str}.txt"
    return not os.path.exists(file_path)
