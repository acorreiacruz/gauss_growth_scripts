from datetime import date, datetime


class Formatter:
    @staticmethod
    def string_from_date(value: date) -> str:
        return datetime.strftime(value, "%Y-%m-%d")
    
    @staticmethod
    def string_from_datetime(value: datetime, format: str = "%Y-%m-%dT%H:%M:%S.%f") -> str:
        return datetime.strftime(value, format)

    @staticmethod
    def convert_utc_str_to_timezone(value: str, format: str = "%Y-%m-%dT%H:%M:%S.%f%z", timezone: str = "America/Sao_Paulo") -> datetime:
        subsecond_start = value.index(".") + 1
        subsecond_end = value.index("+")
        subseconds = value[subsecond_start:subsecond_end]
        adjusted_subsecond = subseconds[:6] if len(subseconds) > 6 else subseconds.ljust(6, "0")
        value = value[:subsecond_start] + adjusted_subsecond + value[subsecond_end:]
        return datetime.strptime(value, format).astimezone(pytz.timezone(timezone))
    
    @staticmethod
    def clean_phone(value: str) -> str:
        return re.sub(r'\D', '', value)
    
    @staticmethod
    def clean_cpf_cnpj(value: str) -> str:
        return re.sub(r'\D', '', value)