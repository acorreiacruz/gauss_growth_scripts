from datetime import datetime, timedelta
import pytz

class DateTimeConfig:
    def __init__(self) -> None:
        self.TIMEZONE = pytz.timezone("America/Sao_Paulo")
        self.TODAY_TZ = datetime.now(tz=self.TIMEZONE)
        self.TODAY_UTC = self.TODAY_TZ.astimezone(pytz.utc)
        self.YESTERDAY_TZ = self.TODAY_TZ - timedelta(days=1)
        self.YESTERDAY_TZ_START = self.YESTERDAY_TZ.replace(hour=0, minute=0, second=0, microsecond=0)
        self.YESTERDAY_TZ_END = self.YESTERDAY_TZ.replace(hour=23, minute=59, second=59, microsecond=9)
        self.YESTERDAY_UTC_START = self.YESTERDAY_TZ_START.astimezone(pytz.utc)
        self.YESTERDAY_UTC_END = self.YESTERDAY_TZ_END.astimezone(pytz.utc)