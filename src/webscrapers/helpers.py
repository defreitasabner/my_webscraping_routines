def treat_string(text: str) -> str:
    treated_string = text.replace(';', ".").replace("'", "").replace('"', "").strip("\n").strip("\r")
    return f'"{treated_string}"'