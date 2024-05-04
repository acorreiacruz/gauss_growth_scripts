from datetime import date, datetime


class Formatter:
    @staticmethod
    def string_from_date(value: date) -> str:
        return datetime.strftime(value, "%Y-%m-%d")
    
    @staticmethod
    def string_from_datetime(value: datetime, format: str = "%Y-%m-%dT%H:%M:%S.%f") -> str:
        return datetime.strftime(value, format)