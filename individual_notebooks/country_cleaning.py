import pandas as pd
import numpy as np
import re
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


# capitalize names except for 'USA', handle two-word countries
def country_formatting(df):
    df['country'] = df['country'].apply(lambda x: 
        ' '.join(word.capitalize() for word in x.split()) if isinstance(x, str) and x.lower() != 'usa' else x)
    return df

