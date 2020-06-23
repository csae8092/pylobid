import re


def extract_coords(some_str):
    regex = r"[+|-]\d+(?:\.\d*)?"
    matches = re.findall(regex, some_str, re.MULTILINE)
    return matches
