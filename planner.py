import pandas as pd

def parse_response_to_plan(text):
    # Simulate parsing AI response (replace with real parser if needed)
    data = {
        "Phase": ["Discovery", "Build"],
        "Start": ["2025-04-01", "2025-04-11"],
        "End": ["2025-04-10", "2025-06-01"],
    }
    df = pd.DataFrame(data)
    df["Start"] = pd.to_datetime(df["Start"])
    df["End"] = pd.to_datetime(df["End"])
    return df
