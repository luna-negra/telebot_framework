import yaml


# list, dict, str
def translate(domain:str, key:str, language_code:str):
    with open(f"translation/{domain}.yml", mode="r", encoding="utf-8") as file:
        content = dict(yaml.safe_load(file))

    try:
        return content.get(key).get(language_code)
    except AttributeError:
        return key