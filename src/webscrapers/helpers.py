def treat_string(text: str) -> str:
    return text.replace(';', ".").replace("'", "").replace('"', "")