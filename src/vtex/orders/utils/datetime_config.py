from datetime import datetime, timedelta, timezone

class DateTimeConfig:
    def __init__(self) -> None:
        self.TIMEZONE = "America/Sao_Paulo"
        self.TODAY_UTC = datetime.now(tz=timezone.utc)
        self.YESTERDAY_UTC =  self.TODAY_UTC - timedelta(days=1)
        self.YESTERDAY_UTC_DATE = self.YESTERDAY_UTC.date()
        self.YESTERDAY_UTC_START = self.YESTERDAY_UTC.replace(hour=0, minute=0, second=0, microsecond=0)
        self.YESTERDAY_UTC_END = self.YESTERDAY_UTC.replace(hour=23, minute=59, second=59, microsecond=0)