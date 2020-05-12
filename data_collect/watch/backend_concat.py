import os
import os.path
import pandas as pd


def create_folder(f, deleteExisting=False):
    '''
    Create the folder

    Parameters:
            f: folder path. Could be nested path (so nested folders will be created)

            deleteExising: if True then the existing folder will be deleted.

    '''
    if os.path.exists(f):
        if deleteExisting:
            shutil.rmtree(f)
    else:
        os.makedirs(f)


apaths = []
gpaths = []
for dirpath, dirnames, filenames in os.walk("/Volumes/Seagate/Periodic/RAW/203-2/WRIST/0113_unzip/"):
    for filename in [f for f in filenames if f.endswith(".csv")]:
        print(filename)
        if 'Gyroscope' in filename:
            gpaths.append(os.path.join(dirpath, filename))
        if 'Accelerometer' in filename:
            apaths.append(os.path.join(dirpath, filename))

create_folder("/Volumes/Seagate/Periodic/RAW/203-2/WRIST/0113_data_acc/")
create_folder("/Volumes/Seagate/Periodic/RAW/203-2/WRIST/0113_data_gyr/")

dfs = []
for i in gpaths:
	dfs.append(pd.read_csv(i))

# pd.concat(dfs).sort_values(by=['Time']).to_csv("../Data/203/inwild_unzip/0113_data_gyr/gyr.csv", index=None)
pd.concat(dfs).to_csv("/Volumes/Seagate/Periodic/RAW/203-2/WRIST/0113_data_gyr/gyr.csv", index=None)

dfs = []
for i in apaths:
	dfs.append(pd.read_csv(i))

# pd.concat(dfs).sort_values(by=['Time']).to_csv("../Data/203/inwild_unzip/0113_data_acc/acc.csv", index=None)
pd.concat(dfs).to_csv("/Volumes/Seagate/Periodic/RAW/203-2/WRIST/0113_data_acc/acc.csv", index=None)

