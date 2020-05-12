import os
import sys
import json
from beyourself.core.util import *
from beyourself.cleanup.video import cut_video, convert
from beyourself.data import get_necklace_timestr, get_necklace
from beyourself.data.label import read_ELAN, write_SYNC
from shutil import copytree, copyfile
from beyourself import settings
import pystache
sys.path.append('../necklace/')
from read_data import read_data
sys.path.append('../..')
from settings import settings
from utils import create_folder

# todo: call separate 1. AVI to mp4. 2 convert 2 elan rela time

# def zScoreNormalize(df, columns):
#     data = df.copy()
#     for c in columns:
#         data[c] = (data[c] - data[c].mean())/data[c].std(ddof = 0)
#     return data


#========================================================================================================
ROOT_DIR = settings['ROOT_DIR']
subj = str(sys.argv[1])
# subj = settings['subj']
configFile = 'partition_0113.json'

ANNO_FOLDER = os.path.join(ROOT_DIR, 'ANNOTATION', subj)
VIDEO_FOLDER = os.path.join(ROOT_DIR, 'RAW', subj, 'VIDEO')
DATA_FOLDER = os.path.join(ROOT_DIR, 'CLEAN', subj, 'NECKLACE')

partition = os.path.join(ANNO_FOLDER, configFile)
visualize_folder = os.path.join(ANNO_FOLDER, 'visualize')
newpartition = os.path.join(ANNO_FOLDER, 'partition_processed.json')
#========================================================================================================


create_folder(visualize_folder)

with open(partition) as f:
    meals = json.load(f)

    for m in meals:
        matching = meals[m]["LED"]

        relative_start = timedelta_from_str(meals[m]['relative_start'])
        relative_end = timedelta_from_str(meals[m]['relative_end'])

        absolute_start = sync_relative_time(relative_start, matching)
        absolute_end = sync_relative_time(relative_end, matching)

        meals[m]['start'] = datetime_to_str(absolute_start)
        meals[m]['end'] = datetime_to_str(absolute_end)

        outfolder = os.path.join(visualize_folder, m)
        maybe_create_folder(outfolder)


        # get Necklace Data
        print(meals[m]['start'])
        print(meals[m]['end'])


        start = human_to_epoch(meals[m]['start'])
        end = human_to_epoch(meals[m]['end'])
        # df = get_necklace('200', start - 60000, end + 60000, 0.01)
        interval = [start, end]
        print(interval)
        df = read_data(DATA_FOLDER, interval, 0.1)

        if not df is None:
            # todo: clear 'energy'

            # df['energy'] = df['aX'].pow(2) + df['aY'].pow(2) + df['aZ'].pow(2)
            df['Elan_time'] = df['Time'] - df['Time'].iloc[0]

            # df = zScoreNormalize(df, ['proximity','leanForward','energy','ambient'])

            df.to_csv(os.path.join(outfolder, 'necklace.csv'),index=None)

        else:
            raise ValueError("NO NECKLACE DATA")
            continue


        # cut video and convert to mp4
        video_mov = os.path.join(outfolder, 'video.mov')
        video_mp4 = os.path.join(outfolder, 'video.mp4')

        cut_video(os.path.join(VIDEO_FOLDER, meals[m]['raw_video']),\
                    meals[m]['relative_start'], meals[m]['relative_end'],\
                    video_mov) 

        convert(video_mov, video_mp4)


        # raw_label_folder = os.path.join(settings.RAW_FOLDER, 'LABEL/P103/')

        # # get Label
        # label = read_ELAN(os.path.join(raw_label_folder, meals[m]['raw_label']))
        # label = label[(label['start'] > relative_start)&\
        #                     (label['start'] < relative_end)]
        # label = label.reset_index()


        # label['start'] = sync_relative_time(label['start'], matching)
        # label['end'] = sync_relative_time(label['end'], matching)


        # write_SYNC(label, os.path.join(outfolder, 'label.json'))


        # copy SYNC
        if not os.path.isdir(os.path.join(outfolder, 'lib')):
            copytree('SYNC/lib', os.path.join(outfolder, 'lib'))
        if not os.path.isfile(os.path.join(outfolder, 'index.html')):
            copyfile('SYNC/index.html', os.path.join(outfolder, 'index.html'))

        renderer = pystache.Renderer()
        syncjs = renderer.render_path('SYNC/sync.js.template', 
            {'startTime': meals[m]['start']})

        overwrite = True
        if os.path.isfile(os.path.join(outfolder, 'sync.js')):
            overwrite = input("Do you want to overwrite sync.js?")

        if overwrite:
            print("Overwriting")
            with open(os.path.join(outfolder, 'sync.js'),'w') as f:
                f.write(syncjs)


        if not os.path.isfile(os.path.join(outfolder, 'labelchewing.json')):
            samplelabel = {meals[m]['start']: 'c'}

            with open(os.path.join(outfolder, 'labelchewing.json'),'w') as f:
                json.dump(samplelabel, f, indent=4)

        if not os.path.isfile(os.path.join(outfolder, 'labelbites.json')):
            samplelabel = {meals[m]['start']: 'c'}

            with open(os.path.join(outfolder, 'labelbites.json'),'w') as f:
                json.dump(samplelabel, f, indent=4)

with open(newpartition, 'w') as f:
    json.dump(meals, f, sort_keys=True, indent=4)
