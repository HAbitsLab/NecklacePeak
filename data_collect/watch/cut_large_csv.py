from dateutil import parser
import pandas as pd



def datetime_to_unixtime(dt):
    '''
    Convert Python datetime object (timezone aware)
    to epoch unix time in millisecond
    '''
    return int(1000 * dt.timestamp())


def datetime_str_to_unixtime(string):
    return datetime_to_unixtime(parse_timestamp_tz_aware(string))


def parse_timestamp_tz_aware(string):
    return parser.parse(string)

start = datetime_str_to_unixtime('01/11/2019 14:00:00-0600')
end = datetime_str_to_unixtime('01/11/2019 23:59:59-0600')

print(start)
print(end)

filePath = '/Volumes/Seagate/Periodic/RAW/203-2/WRIST/0111_data_acc/acc.csv'
df = pd.read_csv(filePath)
df = df[~df['Time'].isin(['Time'])]
df['Time'] = pd.to_numeric(df['Time'], errors='ignore')
df = df.sort_values(by=['Time'])
print(len(df))
print(df)
df = df[(df['Time'] > start) & (df['Time'] < end)]
print(len(df))
