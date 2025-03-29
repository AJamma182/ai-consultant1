import pandas as pd
import re
from dateutil import parser

def parse_response_to_plan(text):
    lines = text.strip().splitlines()
    data = []
    phase_name = start_date = end_date = None

    for line in lines:
        if "Phase" in line:
            match = re.search(r"Phase\\s\\d+:\\s*(.+)", line)
            if match:
                phase_name = match.group(1).strip()
        elif "Start Date" in line:
            start_date = parser.parse(line.split(":", 1)[1].strip())
        elif "End Date" in line:
            end_date = parser.parse(line.split(":", 1)[1].strip())
            if phase_name and start_date and end_date:
                data.append({
                    "Phase": phase_name,
                    "Start": start_date,
                    "End": end_date
                })
                # Reset after adding
                phase_name = start_date = end_date = None

    return pd.DataFrame(data)
