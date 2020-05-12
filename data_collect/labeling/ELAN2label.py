#========================================================================================================
# 
# After obtaining the offset, update annotation file from original ELAN label
# 
#========================================================================================================

import os
import sys
import yaml
import pandas as pd
from datetime import datetime, timedelta
from dateutil import parser
sys.path.append('../..')
from utils import list_files_in_directory, parse_timestamp_tz_aware, read_ELAN, update_ELAN_w_drift
from settings import settings


#========================================================================================================
ROOT_DIR = settings['ROOT_DIR']
subj = str(sys.argv[1])
# subj = settings['subj']
startDate = settings['START_DATE']

VIDEO_FOLDER = os.path.join(ROOT_DIR, 'RAW', subj, 'VIDEO')
ANNO_FOLDER = os.path.join(ROOT_DIR, 'ANNOTATION', subj, 'CHEWING')
#========================================================================================================
startDateTZ = datetime.combine(startDate[subj], datetime.min.time()).\
        astimezone(settings["TIMEZONE"])
print('start date: ', startDateTZ)


#========================================================================================================
# 1. load the absolute time
#========================================================================================================
setting_path = os.path.join(ANNO_FOLDER, 'sync.yaml')

with open(setting_path) as f:
    SETTINGS = yaml.load(f)

ELANAnnotDfConcat = []

for episode in SETTINGS:
    print(episode)

    # get start time and end time
    syncRelative = SETTINGS[episode]['sync_relative']
    syncAbsolute = SETTINGS[episode]['sync_absolute']
    videoLeadTime = SETTINGS[episode]['video_lead_time']

    syncAbsolute = parse_timestamp_tz_aware(syncAbsolute)

    if len(syncRelative) == 12:
        t = datetime.strptime(syncRelative,"%H:%M:%S.%f")
    elif len(syncRelative) == 8:
        t = datetime.strptime(syncRelative,"%H:%M:%S")

    startTime = syncAbsolute - timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)\
                             + timedelta(seconds=videoLeadTime/1000)
    endTime = startTime + timedelta(minutes=20)


    #========================================================================================================
    # 2. load ELAN annotation file if after startDate
    #========================================================================================================
    if startTime > startDateTZ:
        ELANAnnotDf = read_ELAN(os.path.join(VIDEO_FOLDER, episode+'.txt'))
        ELANAnnotDf = ELANAnnotDf.sort_values('start')
        ELANAnnotDf = update_ELAN_w_drift(ELANAnnotDf, startTime)
        ELANAnnotDf.to_csv(os.path.join(ANNO_FOLDER, episode+'.csv'), index = None)
        ELANAnnotDfConcat.append(ELANAnnotDf)

try:
    ELANAnnotDfConcat = pd.concat(ELANAnnotDfConcat)
    ELANAnnotDfConcat.to_csv(os.path.join(ANNO_FOLDER, 'chewing.csv'), index = None)
except:
    print('No file to concat.')
