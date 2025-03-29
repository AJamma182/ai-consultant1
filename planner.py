import pandas as pd
import re
from dateutil import parser

def parse_response_to_plan(text):
    '''
    Parses GPT response and extracts a list of phases with start/end dates.
    Returns a DataFrame with columns: Phase, Start, End
    '''
    pattern = r"(.*?):\s*(\w+\s\d{1,2},\s\d{4})\s*[–-]\s*(\w+\s\d{1,2},\s\d{4})"
    matches = re.findall(pattern, text)

    phases = []
    for match in matches:
        phase_name = match[0].strip()
        try:
            start_date = parser.parse(match[1])
            end_date = parser.parse(match[2])
            phases.append({
                "Phase": phase_name,
                "Start": start_date,
                "End": end_date
            })
        except Exception:
            continue

    return pd.DataFrame(phases)
