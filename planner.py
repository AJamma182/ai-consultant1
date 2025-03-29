import pandas as pd
import re
from dateutil import parser

def parse_response_to_plan(text):
    # Auto-fix formatting by adding newlines before each "Phase:"
    text = re.sub(r"(?!^)\\s+(?=Phase:)", "\n", text)

    pattern = r"Phase:\\s*(.*?),\\s*Start:\\s*(.*?),\\s*End:\\s*(.*?)\\s*$"
    matches = re.findall(pattern, text, re.MULTILINE)

    data = []
    for phase, start_str, end_str in matches:
        try:
            start = parser.parse(start_str)
            end = parser.parse(end_str)
            data.append({"Phase": phase.strip(), "Start": start, "End": end})
        except:
            continue

    return pd.DataFrame(data)
