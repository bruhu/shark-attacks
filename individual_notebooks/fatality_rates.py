def process_fatality_data(df):
    df.rename(columns={'unnamed:_11': 'fatal'}, inplace=True)
    replacement_dict = {
        'N': 'no',
        'Y': 'yes',
        'M': 'unknown',
        'F': 'unknown',
        'n': 'no',
        'Nq': 'unknown'
    }
    df['fatal'] = df['fatal'].fillna('unknown').replace(replacement_dict) #fill NaN vals with 'unknown' and replace unique values
    return df