import pandas as pd
import numpy as np
import re
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


def convert_descriptive_age(value):
    if pd.isnull(value):
        return np.nan
    value = str(value).strip().lower()
    if value in ["teen", "teens"]:
        return 15  # Approximate age for teenagers
    elif value == "adult":
        return 30  # General average for adult age
    elif value in ["middle age", '"middle-age"']:
        return 45  # Approximate age for middle age
    elif value == "elderly":
        return 70  # Approximate age for elderly
    elif value in ["a minor", "young"]:
        return 10  # Assume a minor is around 10 years old
    elif value == "infant" or value == "9 months" or value == "2 to 3 months":
        return 1  # Age 1 for infants
    elif "month" in value:
        return 1  # Treat other month values as infants
    return value

def convert_to_first_age(value):
    if isinstance(value, str):
        numbers = re.findall(r'\d+', value)
        if numbers:
            return int(numbers[0])  
    return value

def convert_half_age(value):
    if isinstance(value, str) and "½" in value:
        # Replace "½" with ".5" and convert to float
        return float(value.replace("½", ".5"))
    return value  

def convert_irregular_entries(value):
    if isinstance(value, str) and not any(char.isdigit() for char in value):
        return np.nan  
    return value