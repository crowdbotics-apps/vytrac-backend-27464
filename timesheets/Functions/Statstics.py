import pandas as pd
from rest_framework.response import Response

from Functions.debuging import Debugging
from collections import OrderedDict, defaultdict


def statistics(data, getter):

    data = data
    resample = getter.get('resample')
    cal = getter.get('cal')
    df = pd.DataFrame(data)
    is_cal = True
    try:
        resample = resample.title()
        cal = cal.lower()
        df['date_created'] = pd.to_datetime(df['date_created'])
    except:
        pass

    try:
        df['date_created'] = pd.to_datetime(df['date_created'])
    except:
        is_cal = False

    if is_cal:
        df['date_created'] = df['date_created'].apply(lambda x: x.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
    #
    #     # df = df.groupby('field_value')
    #     # df = df.apply(lambda x: getattr(x.set_index('date_created').resample(resample), cal)())
    #
    #     # Debugging(df, color='blue')
    #
        if cal == 'duration':
            df = df.pivot(index='object_id', columns='field_value', values=['date_created'])
            # df['durations'] = df['False'].sub(df['True'])

            # Debugging(df.reset_index().to_dict('records'), color='yellow')

                # pivot(index='id', columns='field', values='value').rename(columns={'start_date': 'start', 'end_tmie': 'end'})

        # data = df.reset_index().to_dict('records')

    return data
