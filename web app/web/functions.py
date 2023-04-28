import json
import os
import re
from random import randint


def read_generalization_json(base_dir, localization_language="en"):
    language_file = f"{str(base_dir)}/i18n/{str(localization_language)}.json"
    if os.path.isfile(language_file):
        with open(language_file) as file:
            data = json.load(file)
        return data
    return {}


def read_robots(base_dir):
    robots_file = f"{str(base_dir)}/robots.txt"
    if os.path.isfile(robots_file):
        with open(robots_file, "r") as file:
            data = file.read()
        return data
    return ""


def read_country(base_dir, localization_language="en"):
    country_file = f"{str(base_dir)}/i18n/country-{localization_language}.json"
    if os.path.isfile(country_file):
        with open(country_file) as file:
            data = json.load(file)
        return data
    return {}


def generate_verify_code(length=3):
    range_start = 10 ** (length - 1)
    range_end = (10**length) - 1
    return randint(range_start, range_end)


def is_valid_recived_field(request, fieldlist):
    return all(value in list(fieldlist) for value in list(request))


def is_valid_mobile(string):
    mobile_regex = "^09(1[0-9]|3[1-9])-?[0-9]{3}-?[0-9]{4}$"
    return bool(re.search(mobile_regex, string))


def is_valid_email(string):
    string = string.lower()
    email_regex = "^[a-z0-9\.]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    return bool(re.search(email_regex, string))


def is_valid_country_code(base_dir, code):
    country_file = f"{str(base_dir)}/i18n/country.json"
    if os.path.isfile(country_file):
        with open(country_file) as file:
            data = json.load(file)
        data = list(data["country"])
        for value in data:
            if code == value["code"]:
                return True
    return False


def code_to_country(base_dir, code, localization_language="en"):
    country_file = f"{str(base_dir)}/i18n/country-{localization_language}.json"
    if os.path.isfile(country_file):
        with open(country_file) as file:
            data = json.load(file)
        data = list(data["country"])
        for value in data:
            if code == value["code"]:
                return value["name"]
    return ""
