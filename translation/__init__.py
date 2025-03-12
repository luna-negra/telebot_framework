import yaml


# list, dict, str
def translate(domain:str, key:str, language_code:str="en"):
    with open(f"translation/{domain.replace("_", "/")}.yml", mode="r", encoding="utf-8") as file:
        content = dict(yaml.safe_load(file))

    try:
        return content.get(key.lower()).get(language_code)
    except AttributeError:
        return key