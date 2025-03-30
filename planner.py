import pandas as pd
import re
from dateutil import parser

def parse_response_to_plan(text):
    lines = text.strip().splitlines()
    table_lines = [line for line in lines if "|" in line and not line.strip().startswith("|-")]
    rows = []

    for line in table_lines[1:]:  # Skip the header
        parts = [p.strip() for p in line.strip().split("|") if p.strip()]
        if len(parts) == 3:
            phase, start, end = parts
            try:
                rows.append({
                    "Phase": phase,
                    "Start": parser.parse(start),
                    "End": parser.parse(end)
                })
            except:
                continue

    return pd.DataFrame(rows)
