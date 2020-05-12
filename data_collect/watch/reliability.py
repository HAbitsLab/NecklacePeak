import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, time, date
from shutil import copyfile, rmtree, move
from calc_reliability import calc_reliability
from score_reliability import score_reliability
from utils import create_folder


def list_files_in_directory(mypath):
    return [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]


def list_subfolder_path_in_directory(mypath):
    return [os.path.join(mypath, o) for o in os.listdir(mypath) if os.path.isdir(os.path.join(mypath,o))]



TIME_COL = 'time'

SUBJ = '203'
DEVICE = 'WRIST'
# SENSOR = 'ACCELEROMETER'
SENSOR = 'GYROSCOPE'
timestampCol = 2
RAW_PATH = '../../Data/wild/CLEAN/'

unit = 'second'
sensorFreq = 20

# read start time and end time for a meal
dataPath = os.path.join(RAW_PATH, SUBJ, DEVICE, SENSOR)
reliPath = os.path.join(RAW_PATH, SUBJ, DEVICE, SENSOR+'_reliability')
create_folder(reliPath)

print(dataPath)
print(os.path.exists(dataPath))
files = list_files_in_directory(dataPath)

for file in files:
    file_path = os.path.join(dataPath, file)
    df = pd.read_csv(file_path)

    if len(df):
        timeArr = df.iloc[:,timestampCol-1].values
        countDf = calc_reliability(timeArr, sensorFreq, unit, plot=0)        
        countDf.to_csv(os.path.join(reliPath, file), index=False)
        score_reliability(countDf, sensorFreq, unit)


