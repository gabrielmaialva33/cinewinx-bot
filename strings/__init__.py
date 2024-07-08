import logging
import os
from typing import List

import yaml

languages = {}
commands = {}

languages_present = {}


def get_command(value: str) -> List:
    return commands["command"][value]


def get_string(lang: str) -> dict:
    return languages[lang]


# load commands from the strings folder
for filename in os.listdir(r"./strings"):
    if filename.endswith(".yml"):
        language_name = filename[:-4]
        commands[language_name] = yaml.safe_load(
            open(r"./strings/" + filename, encoding="utf8")
        )

# load all languages present in the strings/langs folder
for filename in os.listdir(r"./strings/langs/"):
    if "pt-br" not in languages:
        languages["pt-br"] = yaml.safe_load(
            open(r"./strings/langs/pt-br.yml", encoding="utf8")
        )
        languages_present["pt-br"] = languages["pt-br"]["name"]

    if filename.endswith(".yml"):
        language_name = filename[:-4]
        if language_name == "pt-br":
            continue
        languages[language_name] = yaml.safe_load(
            open(r"./strings/langs/" + filename, encoding="utf8")
        )
        for item in languages["pt-br"]:
            if item not in languages[language_name]:
                languages[language_name][item] = languages["pt-br"][item]
    try:
        languages_present[language_name] = languages[language_name]["name"]
    except Exception as e:
        logging.exception(e)
        print("There is some issue with the language file inside bot.")
        exit()
