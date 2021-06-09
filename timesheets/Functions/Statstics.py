import pandas as pd
from rest_framework.response import Response

from Functions.debuging import Debugging


def statistics(data, getter):
    data = data
    try:
        cal = getter.get('cal').lower()
        resample = getter.get('resample').title()

        resample = resample.title()
        cal = cal.lower()
        df = pd.DataFrame(data)
        df['date_created'] = pd.to_datetime(df['date_created'])
        # df = df.pivot(index='object_id', columns='field_value', values='date_created')
        df = df.fillna('')
        df = df.groupby('field_target').apply(
            lambda x: getattr(x.set_index('date_created').resample(resample), cal)())
        # df['date_created'] = df['date_created'].apply(lambda x: x.dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ%')).reset_index().to_dict('records')

        # TODO keep time value don't drop

        data = df.reset_index(drop=True).to_dict('records')

        # Debugging(data, color='blue')
        # Debugging(df, color='red')
    except:
        pass

    return data
