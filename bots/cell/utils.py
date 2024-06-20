
from datetime import datetime, timedelta
from tzlocal import get_localzone


def convert_datetime(utc_time):
    utc_time = "2024-06-19T20:34:17.354Z"
    raw = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone(tz="UTC")