import re


def locate_with_default(pattern: str, input_data: str, default=None):
    """
    """

    pattern = re.compile(pattern)
    matches = pattern.search(input_data)
    return matches.group(1) if matches else default