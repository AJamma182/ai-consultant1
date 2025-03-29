import pandas as pd
import re
from dateutil import parser

def parse_response_to_plan(text):
    '''
    Parses GPT response and extracts a list of phases with start/end dates.
    Returns a DataFrame with columns: Phase, Start, End
    '''
    pattern = r"(?P<phase>.*?):\s*(?P<start>\w+\s\d{1,2},\s\d{4})[\s\-–to]+(?P<end>\w+\s\d{1,2},\s\d{4})"
    matches = re.findall(pattern, text)

    phases = []
    for match in matches:
        phase, start_str, end_str = match
        try:
            start_date = parser.parse(start_str)
            end_date = parser.parse(end_str)
            phases.append({
                "Phase": phase.strip(),
                "Start": start_date,
                "End": end_date
            })
        except Exception:
            continue

    return pd.DataFrame(phases)
