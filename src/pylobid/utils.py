import re


def extract_coords(some_str: str) -> list:
    """Utility function to extract coordinates from a (WKT) string

    :param some_str: A string providing coordinates
    :type some_str: str

    :return: A list with the coordinates
    :rtype: list

    """
    regex = r"[+|-]\d+(?:\.\d*)?"
    matches = re.findall(regex, some_str, re.MULTILINE)
    return matches
