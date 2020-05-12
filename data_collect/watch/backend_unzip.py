import os
import zipfile


def list_files_in_directory(mypath):
    return [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]


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


ZIP_FOLDER = '/Volumes/Seagate/Periodic/RAW/203-2/WRIST/0113/'
UNZIP_FOLDER = '/Volumes/Seagate/Periodic/RAW/203-2/WRIST/0113_unzip/'


files = list_files_in_directory(ZIP_FOLDER)

for f in files:
    print(f)
    if f.endswith('.zip'):
        create_folder(UNZIP_FOLDER+f[:-4]+'/')
        with zipfile.ZipFile(ZIP_FOLDER+f, 'r') as zip_ref:
            zip_ref.extractall(UNZIP_FOLDER+f[:-4]+'/')