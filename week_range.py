import calendar
from datetime import datetime

import pandas as pd


def week_range():
    start_date = '2023-01-01'
    end_date = '2023-01-31'

    date_list = pd.date_range(start=start_date, end=end_date)
    df = pd.DataFrame({'date': date_list})

    df['date'] = pd.to_datetime(df['date'])
    df['weekday'] = df['date'].dt.weekday
    df['year_month'] = df['date'].dt.strftime("%Y-%m")
    grp = df.groupby('year_month')
    df['date'].dt.strftime("%V")
    append_df = []
    for name, group in grp:
        def week_in_month(date):
            print(date.isocalendar()[1])
            return (1 + date.isocalendar()[1]) - (date.replace(day=1).isocalendar()[1])

        group['weekInMonth'] = group['date'].apply(week_in_month)
        group['weekInMonth'] = 'W' + group['weekInMonth'].astype(str)
        group = group.reset_index(drop=True)
        append_df.append(group)

    final_df = pd.concat(append_df, ignore_index=True)
    print(final_df)
    print(final_df.to_csv('week_range.csv'))


week_range()


def week_of_month(tgtdate):
    global startdate
    tgtdate = tgtdate.to_pydatetime()
    days_this_month = calendar.mdays[tgtdate.month]
    # print(days_this_month, range(1, days_this_month))
    for i in range(1, days_this_month):
        d = datetime(tgtdate.year, tgtdate.month, i)
        if d.day - d.weekday() > 0:
            startdate = d
            break
    return (tgtdate - startdate).days // 7 + 1


start_date = '2023-09-01'
end_date = '2023-09-30'

date_list = pd.date_range(start=start_date, end=end_date)
df = pd.DataFrame({'date': date_list})

df['date'] = pd.to_datetime(df['date'])

df['weekInMonth'] = 'W' + df['date'].apply(week_of_month).astype(str)
df.loc[df['weekInMonth'] == 'W0', 'weekInMonth'] = 'W1'
