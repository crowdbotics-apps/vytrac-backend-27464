import pandas as pd
from rest_framework.response import Response

from Functions.debuging import Debugging


def statistics(data, getter):
    data = data
    resample = getter.get('resample')
    cal = getter.get('cal')
    df = pd.DataFrame(data)
    # df['date_created'] = pd.to_datetime(df['date_created'])
    # try:
    #
    #
    #
    #     # df['date_created'] = df['date_created'].apply(lambda x: x.dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ%')).reset_index().to_dict('records')
    #     # df = df.pivot(index='object_id', columns='field_value', values='date_created')
    #     # df = df.fillna('')
    #
    #
    #     # TODO keep time value don't drop
    #
    #     # data = df.reset_index(drop=True).to_dict('records')
    #
    #     # Debugging(data, color='blue')
    #     # Debugging(df, color='red')
    # except:
    #     pass

    if resample and cal:
        resample = resample.title()
        cal = cal.lower()
        df = df.groupby('field_value')
        # TODO
        # df = df.apply(lambda x: getattr(x.set_index('date_created').resample(resample), cal)())
        Debugging(data[0]['date_created'], color='green') #TODO day should ==14
        Debugging(data[1]['date_created'], color='green')#TODO day should ==15
    return data
