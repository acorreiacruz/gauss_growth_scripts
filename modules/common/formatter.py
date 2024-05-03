from datetime import date, datetime


class Formatter:
    def string_from_date(self, value: date) -> str:
        return datetime.strftime(value, "%Y-%m-%d")
    
    def string_from_datetime(self, value: datetime, format: str = "%Y-%m-%dT%H:%M:%S.%f") -> str:
        return datetime.strftime(value, format)