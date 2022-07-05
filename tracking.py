import pandas as pd


def parse_prop(prop):
    if prop['type'] == 'number':
        return prop['number']
    elif prop['type'] == 'checkbox':
        return prop['checkbox']
    elif prop['type'] == 'date':
        return prop['date']['start']
    else:
        return None


def get_tracking(tracking_db):
    # 1. Pull out properties
    entries = [line['properties'] for line in tracking_db['results']]
    # 2. Pull out data
    records = [{p: parse_prop(e[p]) for p in e} for e in entries]
    print(records)
    # 3. Drop columns that we can't parse yet
    records = [{k: v for k, v in r.items() if v is not None} for r in records]
    print(records)
    # 4. Construct DataFrame
    df = pd.DataFrame.from_records(records, index='Date')
    df.index = pd.to_datetime(df.index)
    return df.sort_index()
