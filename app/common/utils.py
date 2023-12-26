from datetime import datetime


def datetime_to_drf_str(value: datetime) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%S")
