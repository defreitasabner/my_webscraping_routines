from datetime import datetime

def treat_string(text: str) -> str:
    treated_string = text.replace(';', ".").replace("'", "").replace('"', "").replace("\n", "").replace("\r", " ")
    return f'"{treated_string}"'

def datetime_convert(datetime_str: str) -> datetime:
    if type(datetime_str) is str and len(datetime_str) > 0:
        treated_datetime_str = datetime_str
        return datetime.strptime(treated_datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')