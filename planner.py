import pandas as pd
import re
from dateutil import parser

def parse_response_to_plan(text):
    """
    Parses GPT response and extracts phase name, start and end dates.
    Returns a DataFrame with columns: Phase, Start, End
    """
    pattern = r"(?P<phase>.*?):\s*(?P<start>\\w+\\s\\d{{1,2}},\\s\\d{{4}})[\\s\\-–to]+(?P<end>\\w+\\s\\d{{1,2}},\\s\\d{{4}})"
    matches = re.findall(pattern, text)

    data = []
    for match in matches:
        phase, start_str, end_str = match
        try:
            start = parser.parse(start_str)
            end = parser.parse(end_str)
            data.append({"Phase": phase.strip(), "Start": start, "End": end})
        except:
            continue

    return pd.DataFrame(data)
