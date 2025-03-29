import pandas as pd
import re
from dateutil import parser

def parse_response_to_plan(text):
    pattern = r"Phase:\\s*(.*?),\\s*Start:\\s*(\\w+\\s\\d{1,2},\\s\\d{4}),\\s*End:\\s*(\\w+\\s\\d{1,2},\\s\\d{4})"
    matches = re.findall(pattern, text)

    data = []
    for phase, start_str, end_str in matches:
        try:
            start = parser.parse(start_str)
            end = parser.parse(end_str)
            data.append({"Phase": phase.strip(), "Start": start, "End": end})
        except:
            continue

    return pd.DataFrame(data)