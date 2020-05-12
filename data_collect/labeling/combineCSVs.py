import os
import sys
import yaml
import pytz
from datetime import datetime, timedelta
import pandas as pd
sys.path.append('../..')
from utils import list_files_in_directory, parse_timestamp_tz_aware, read_ELAN, update_ELAN_w_drift
from settings import settings


#========================================================================================================
ROOT_DIR = settings['ROOT_DIR']
# subj = settings['subj']
subj = '208'
startDate = settings['START_DATE']

ANNO_FOLDER = os.path.join(ROOT_DIR, 'ANNOTATION', subj, 'CHEWING')
#========================================================================================================

startDateTZ = datetime.combine(startDate[subj], datetime.min.time()).\
        astimezone(settings["TIMEZONE"])
print('start date: ', startDateTZ)

ELANAnnotDfConcat = []

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

    #========================================================================================================
    # 2. load ELAN annotation file if after startDate
    #========================================================================================================
    if startTime > startDateTZ:
        try:
            ELANAnnotDf = pd.read_csv(os.path.join(ANNO_FOLDER, episode+'.csv'))
            ELANAnnotDfConcat.append(ELANAnnotDf)
            print(episode)
        except:
            print(episode, ': file not exist.')

try:
    ELANAnnotDfConcat = pd.concat(ELANAnnotDfConcat)
    ELANAnnotDfConcat.to_csv(os.path.join(ANNO_FOLDER, 'chewing.csv'), index = None)
except:
    print('No file to concat.')
