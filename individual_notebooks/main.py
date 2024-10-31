import pandas as pd
import numpy as np
import re
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

shark_df = pd.read_excel('../shark-dataset.xls')
# create dataframe copy
original_df = shark_df.copy()
shark_df

unused_columns = ['type', 'state', 'name', 'location', 'species', 'source', 'pdf', 'href_formula', 'href', 'case_number', 'case_number.1', 'original_order', 'unnamed:_21', 'unnamed:_22', 'time', 'injury']

from column_cleaning import clean_columns

shark_df = clean_columns(shark_df)

start_year = 2014
end_year = 2024

shark_df = shark_df[(shark_df["year"] >= start_year) & (shark_df["year"] <= end_year)]

#convert float in year to int
shark_df["year"] = shark_df["year"].fillna(0).astype(int)

# remove invalid rows with "2014" as date
shark_df = shark_df.drop(shark_df.index[-2:])


total_count_spring = 298
total_count_summer = 405
total_count_autumn = 290
total_count_winter = 231

# shark_df
# shark_df.head()

# Function to parse different date formats

from date_time import parse_date

# Create datetime_column and string_column
shark_df["datetime_column"] = shark_df["date"].apply(parse_date)
shark_df["string_column"] = shark_df["date"].apply(lambda x: x if isinstance(x, str) else None)

# Drop rows with invalid datetime values
shark_df = shark_df[shark_df["datetime_column"].notna()]

# Extract month and year from datetime_column
shark_df['month'] = shark_df["datetime_column"].apply(lambda x: x.month if pd.notnull(x) else None)
shark_df['year'] = shark_df["datetime_column"].apply(lambda x: x.year if pd.notnull(x) else None)
#shark_df['month'] = shark_df["datetime_column"].dt.month
#shark_df['year'] = shark_df["datetime_column"].dt.year

# Define season mapping
season_mapping = {
    "Spring": [3, 4, 5],
    "Summer": [6, 7, 8],
    "Autumn": [9, 10, 11],
    "Winter": [12, 1, 2]
}

from date_time import what_season

# Assign season based on the extracted month
shark_df['season'] = shark_df['month'].apply(what_season)

# Check the resulting DataFrame
print(shark_df[['date', 'datetime_column', 'string_column', 'year', 'month', 'season']])

#fatality rates

from fatality_rates import process_fatality_data

shark_df = process_fatality_data(shark_df)

#Activity column cleaning
# values to a common case
shark_df['activity'] = shark_df['activity'].str.strip().str.lower().str.replace(r"[\"']", '', regex=True)

most_common_words = []

from activity import word_count

most_common_words = word_count(shark_df)

selected_values_to_replace = ['surfing', 'diving', 'fishing', 'swimming', 'wading', 'bathing', 'snorkeling', 'kayaking', 'body boarding', 'scuba diving']

from activity import replace_values

shark_df = replace_values(shark_df, selected_values_to_replace)

# remove empty values
shark_df = shark_df[shark_df['activity'].apply(lambda x: x.strip() != '')]

# retrieve 10 top activities within filtering step
shark_df = shark_df[shark_df['activity'].isin((lambda x: x.index)(shark_df['activity'].value_counts().head(10)))] 

#Sex column cleaning

shark_df['sex'] = shark_df['sex'].str.strip()

# Replace specific values
shark_df['sex'] = shark_df['sex'].replace({
    'M': 'M', 
    'F': 'F',  
    'N': np.nan,  
    'M x 2': 'M', 
    'lli': np.nan,  
    '.': np.nan,  
    ' M': 'M'  
})

shark_df['sex']= shark_df['sex'].fillna('unknown')

#Calculate the counts of "M" and "F"
total_known = shark_df['sex'].value_counts()
m_count = total_known.get('M', 0)
f_count = total_known.get('F', 0)
total = m_count + f_count

#Calculate the percentages of "M" and "F"
if total > 0:
    m_percentage = m_count / total
    f_percentage = f_count / total
else:
    m_percentage = 0.5  # Default to equal distribution if no known values
    f_percentage = 0.5

# Determine the number of "Unknown" values
unknown_count = shark_df['sex'].value_counts().get('unknown', 0)

# Calculate how many "Unknown" values to fill with "M" and "F"
m_fill_count = int(m_percentage * unknown_count)
f_fill_count = unknown_count - m_fill_count  # Ensure all "Unknown" are assigned

# Get indices of the "Unknown" entries
unknown_indices = shark_df[shark_df['sex'] == 'unknown'].index

# Randomly shuffle the "Unknown" indices
shuffled_indices = np.random.permutation(unknown_indices)

# Split the shuffled indices into two groups for "M" and "F"
m_indices = shuffled_indices[:m_fill_count]
f_indices = shuffled_indices[m_fill_count:]

# Assign "M" and "F" to the split indices
shark_df.loc[m_indices, 'sex'] = 'M'
shark_df.loc[f_indices, 'sex'] = 'F'

# Verify replacements by checking updated counts
# print(shark_df['sex'].value_counts())

#age column cleaning

from age_cleaning import convert_descriptive_age

shark_df['age'] = shark_df['age'].apply(convert_descriptive_age)

from age_cleaning import convert_to_first_age

shark_df['age'] = shark_df['age'].apply(convert_to_first_age)

from age_cleaning import convert_half_age

shark_df['age'] = shark_df['age'].apply(convert_half_age)

#Convert any remaining irregular entries to NaN
from age_cleaning import convert_irregular_entries

shark_df['age'] = shark_df['age'].apply(convert_irregular_entries)

#convert to numeric
shark_df['age'] = pd.to_numeric(shark_df['age'], errors='coerce')

#Replace NaN values with the mode of the age column
age_mode = shark_df['age'].mode()[0]
shark_df['age'] = shark_df['age'].fillna(age_mode)

#convert type to int
shark_df['age'] = shark_df['age'].astype(int)

# capitalize names except for 'USA', handle two-word countries

from country_cleaning import country_formatting

shark_df = country_formatting(shark_df)

# filter df based on the top 10 countries
shark_df = shark_df[shark_df['country'].isin(shark_df['country'].value_counts().head(10).index)]

shark_final_df = shark_df.to_csv('shark_final_df.csv', index=False)
shark_final_df

# we went from 6973 rows x 23 columns to 904 rows x 7 columns
