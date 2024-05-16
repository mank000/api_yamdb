from datetime import datetime


def year_validator() -> int:
    return int(datetime.now().year)
