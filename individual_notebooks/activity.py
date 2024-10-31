import pandas as pd
import numpy as np
import re
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


def word_count(shark_df):
    global most_common_words  # declare the global variable
    shark_df['activity'] = shark_df['activity'].fillna('').astype(str)  # replace NaN values with an empty string
    all_text = ' '.join(shark_df['activity'])  # combine all values into a single string
    words = re.findall(r'\w+', all_text.lower())  # split into words
    word_counts = Counter(words)  # count word frequency
    most_common_words = [word for word, count in word_counts.most_common(50) if len(word) >= 5]
    return most_common_words

def replace_values(shark_df, selected_values_to_replace):
    for word_to_replace in selected_values_to_replace:
        shark_df.loc[shark_df['activity'].str.contains(word_to_replace, case=False, na=False), 'activity'] = word_to_replace
    return shark_df