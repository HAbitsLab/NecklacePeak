import os
import sys
import pandas as pd
from datetime import timedelta
from datetime import datetime
from pytz import timezone
from settings import settings
from utils import create_folder, list_files_in_directory, datetime_to_filename


#========================================================================================================

# SUBJ = 'P203'

# RAW_DIR = '../Data/203/inwild_unzip/data_acc/'

# create_folder('../Data/203/inwild/CLEAN/WRIST/ACC/')

# IN_DIR = '../Data/203/inwild/CLEAN/WRIST/ACC/'

RAW_DIR = '../Data/203/inwild_unzip/data_gyr/'

create_folder('../Data/203/inwild/CLEAN/WRIST/GYR/')

IN_DIR = '../Data/203/inwild/CLEAN/WRIST/GYR/'

file = os.path.join(RAW_DIR, list_files_in_directory(RAW_DIR)[0])

starttimestamp = 1546581600000

#========================================================================================================
# CLEAN Module
#========================================================================================================
localtz = settings['TIMEZONE']

df = pd.read_csv(file)

print('len', len(df), '\n')
df = df[~df['Time'].isin(['Time'])]
print('Remove redundant headers...\n')
print('len', len(df), '\n')

df = df.dropna()
df['Time'] = pd.to_numeric(df['Time'], errors='ignore')
print(df.columns)
df = df.sort_values('Time')
df = df[df['Time'] > starttimestamp]

df['date'] = pd.to_datetime(df['Time'],unit='ms')
df = df.set_index(['date'])
df.index = df.index.tz_localize('UTC').tz_convert(settings['TIMEZONE'])

# dt: day: start day, hour: 0 
dt = datetime(year=df.index[0].year, month=df.index[0].month, \
                day=df.index[0].day, hour=0, minute=0, second=0)
dt = localtz.localize(dt)


#========================================================================================================
# split each hour into separate file under day folder
#========================================================================================================
# todo: fix the issue that the second day is not iterated

for day in range((df.index[-1].day - df.index[0].day) + 1):
    create_folder(IN_DIR)

    for hour in range(24):
        startHour = dt+timedelta(days=day, hours=hour)
        endHour = dt+timedelta(days=day, hours=hour+1)
        dfHr = df[(df.index>=startHour) & (df.index<endHour)]

        # if 'Unnamed: 13' in dfHr.columns:
        #     dfHr = dfHr.drop(columns=['Unnamed: 13'])

        # dfHr = dfHr.rename(columns={'power': 'energy'})
        # dfHr = dfHr[['Time','proximity','ambient','leanForward','qW','qX','qY','qZ','aX','aY','aZ','cal','energy']]

        if len(dfHr):
            file = datetime_to_filename(startHour)
            dfHr.to_csv(os.path.join(IN_DIR, file))