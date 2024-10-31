import pandas as pd
import numpy as np
import re
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def parse_date(date_str):
    if isinstance(date_str, str):
        try: 
            return pd.to_datetime(date_str)  # Try direct conversion
        except ValueError:
            match = re.search(r'(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}-[A-Za-z]{3}-\d{4}|\b[A-Za-z]{3}-\d{4}\b)', date_str)
            if match:
                date_str = match.group(0)
                try:
                    return datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    try:
                        return datetime.strptime(date_str, "%d-%b-%Y")
                    except ValueError:
                        try:
                            return datetime.strptime(date_str, "%b-%Y")
                        except ValueError:
                            return None  # Return None for invalid formats
    elif isinstance(date_str, datetime):
        return date_str  # Return the datetime object as is
    return None  # Return None if not a string or datetime

season_mapping = {
    "Spring": [3, 4, 5],
    "Summer": [6, 7, 8],
    "Autumn": [9, 10, 11],
    "Winter": [12, 1, 2]
}

# Function to assign season based on month
def what_season(month):
    for season, months in season_mapping.items():
        if month in months:
            return season
    return None