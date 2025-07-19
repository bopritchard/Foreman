# mapper.py

# Naive field mapping: maps common CSV headers to internal field names

DEFAULT_MAPPING = {
    'full_name': 'name',
    'email': 'customerEmail',
    'joined_on': 'signupDate'
}

def map_fields(df):
    df = df.copy()
    mapped_cols = {}
    for col in df.columns:
        key = col.strip().lower()
        mapped_cols[col] = DEFAULT_MAPPING.get(key, col)
    df.rename(columns=mapped_cols, inplace=True)
    return df
