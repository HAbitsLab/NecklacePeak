import os
import re
import sys
import json
import time
import yaml
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import pylab
from datetime import datetime, timedelta, time, date
from shutil import copyfile
sys.path.append('../..')
from utils import create_folder, \
					datetime_to_unixtime, \
					parse_timestamp_tz_naive, \
					list_files_in_directory, \
					truncate_df_index_dt,\
					truncate_df_index_str,\
					parse_timestamp_tz_aware
from settings import settings
sys.path.append('../necklace')
from read_data import read_data


# ==================================================================================
SUBJ = '218'
ROOT_DIR = settings['ROOT_DIR']
TEMP_UP_FOLDER = os.path.join(ROOT_DIR, 'pallas/wild')
ANNO_FOLDER = os.path.join(ROOT_DIR, 'ANNOTATION', SUBJ, 'CHEWING')
DATA_FOLDER = os.path.join(ROOT_DIR, 'CLEAN', SUBJ, 'NECKLACE')
# ==================================================================================


#========================================================================================================
# 1. load the absolute time
#========================================================================================================
setting_path = os.path.join(ANNO_FOLDER, 'sync.yaml')

with open(setting_path) as f:
    SETTINGS = yaml.load(f)

print(SETTINGS)

for episode in SETTINGS:
	print("episode: ", episode)
	# get start time and end time
	sync_relative = SETTINGS[episode]['sync_relative']
	sync_absolute = SETTINGS[episode]['sync_absolute']
	video_lead_time = SETTINGS[episode]['video_lead_time']
	print("video_lead_time: ", video_lead_time)
	sync_absolute = parse_timestamp_tz_aware(sync_absolute)
	t = datetime.strptime(sync_relative,"%H:%M:%S")
	startTime = sync_absolute - timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)\
							 + timedelta(seconds=video_lead_time/1000)
	endTime = startTime + timedelta(minutes=20)
	startTimeExt = startTime - timedelta(minutes = 10)
	endTimeExt = endTime + timedelta(minutes = 10)

	epiDf = read_data(DATA_FOLDER, datetime_to_unixtime(startTimeExt), datetime_to_unixtime(endTimeExt))
	epiDf['ELAN_time'] = epiDf['Time'] - datetime_to_unixtime(startTime)
	# print(startTime)
	# epiDf[['accx','accy','accz']].plot()
	# plt.show()
	epiDf.to_csv(os.path.join(ANNO_FOLDER, 'P'+SUBJ+'_SYNC_'+episode+'.csv'), index = None)



