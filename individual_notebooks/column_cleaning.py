

unused_columns = ['type', 'state', 'name', 'location', 'species', 'source', 'pdf', 'href_formula', 'href', 'case_number', 'case_number.1', 'original_order', 'unnamed:_21', 'unnamed:_22', 'time', 'injury']

def clean_columns(df):
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_", regex=False) # lowercase col names, remove+replace empty spaces
    df.rename(columns={'unnamed:_11': 'fatal'}, inplace=True)
    df = df.drop(unused_columns, axis=1, errors='ignore')
    return df
