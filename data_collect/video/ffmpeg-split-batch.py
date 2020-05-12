#!/usr/bin/env python

import csv
import subprocess
import math
import json
import os
import sys
import shlex
from optparse import OptionParser


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


def list_files_in_directory(mypath):
    return [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]



def split_by_manifest(filename, manifest, vcodec="copy", acodec="copy",
                      extra="", **kwargs):
    """ Split video into segments based on the given manifest file.

    Arguments:
        filename (str)      - Location of the video.
        manifest (str)      - Location of the manifest file.
        vcodec (str)        - Controls the video codec for the ffmpeg video
                            output.
        acodec (str)        - Controls the audio codec for the ffmpeg video
                            output.
        extra (str)         - Extra options for ffmpeg.
    """
    if not os.path.exists(manifest):
        print ("File does not exist")
        raise SystemExit

    with open(manifest) as manifest_file:
        manifest_type = manifest.split(".")[-1]
        if manifest_type == "json":
            config = json.load(manifest_file)
        elif manifest_type == "csv":
            config = csv.DictReader(manifest_file)
        else:
            print ("Format not supported. File must be a csv or json file")
            raise SystemExit

        split_cmd = ["ffmpeg", "-i", filename, "-vcodec", vcodec,
                     "-acodec", acodec, "-y"] + shlex.split(extra)
        try:
            fileext = filename.split(".")[-1]
        except IndexError as e:
            raise IndexError("No . in filename. Error: " + str(e))
        for video_config in config:
            split_str = ""
            split_args = []
            try:
                split_start = video_config["start_time"]
                split_length = video_config.get("end_time", None)
                if not split_length:
                    split_length = video_config["length"]
                filebase = video_config["rename_to"]
                if fileext in filebase:
                    filebase = ".".join(filebase.split(".")[:-1])

                split_args += ["-ss", str(split_start), "-t",
                    str(split_length), filebase + "." + fileext]
                print ("########################################################")
                print ("About to run: "+" ".join(split_cmd+split_args))
                print ("########################################################")
                subprocess.check_output(split_cmd+split_args)
            except KeyError as e:
                print ("############# Incorrect format ##############")
                if manifest_type == "json":
                    print ("The format of each json array should be:")
                    print ("{start_time: <int>, length: <int>, rename_to: <string>}")
                elif manifest_type == "csv":
                    print ("start_time,length,rename_to should be the first line ")
                    print ("in the csv file.")
                print ("#############################################")
                print (e)
                raise SystemExit

def get_video_length(filename):

    output = subprocess.check_output(("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename)).strip()
    video_length = int(float(output))
    print ("Video length in seconds: "+str(video_length))

    return video_length

def ceildiv(a, b):
    return int(math.ceil(a / float(b)))

def split_by_seconds(filename, split_length, vcodec="copy", acodec="copy",
                     extra="", video_length=None, **kwargs):
    if split_length and split_length <= 0:
        print ("Split length can't be 0")
        raise SystemExit

    if not video_length:
        video_length = get_video_length(filename)
    split_count = ceildiv(video_length, split_length)
    if(split_count == 1):
        print ("Video length is less then the target split length.")
        raise SystemExit

    split_cmd = ["ffmpeg", "-i", filename, "-vcodec", vcodec, "-acodec", acodec] + shlex.split(extra)
    try:
        filebase = ".".join(filename.split(".")[:-1])
        fileext = filename.split(".")[-1]
        time_base = ".".join(filename.split("_")[-1])
        date_base = ".".join(filename.split("_")[0:-1])
        time_h = ".".join(time_base.split(".")[0]) + ".".join(time_base.split(".")[1])
        time_m = ".".join(time_base.split(".")[4]) + ".".join(time_base.split(".")[5])
        time_s = str(".".join(time_base.split(".")[8]) + ".".join(time_base.split(".")[9]))
        print('+++++++++++++++++++++++++')
        print(time_h)
        print(time_m)
        print(time_s)
        print('+++++++++++++++++++++++++')
        num_of_ite = 0
        # time_m = int(time_m) + 5 * num_of_ite
        # if (time_m > 60 ):
        #     time_h = int(time_h) + 1
        #     time_m = time_m - 60
        #     time_m = "0" + str(time_m)
        # time_h = str(time_h)
        # time_detail = time_h + "." + time_m+ "." +time_s 

    except IndexError as e:
        raise IndexError("No . in filename. Error: " + str(e))
    for n in range(0, split_count):
        split_args = []
        if n == 0:
            split_start = 0
        else:
            split_start = split_length * n

        if (int(time_m) > 60 ):
            time_h = int(time_h) + 1
            time_m = int(time_m) - 60
            time_m = str("0" + str(time_m))
        if (len(str(time_m)) < 2):
            time_m = str("0" + str(time_m))
        time_h = str(time_h)
        time_m = str(time_m)
        time_detail = time_h + "." + time_m+ "." +time_s 

        split_args += ["-ss", str(split_start), "-t", str(split_length),
                       "split" + date_base + "_" + time_detail + "." + fileext]
        print ("About to run: "+" ".join(split_cmd+split_args))
        time_m = str(int(time_m) + 5)
        subprocess.check_output(split_cmd+split_args)
        

def split_single_video(file):

    #######################
    options = {}
    options['filename'] = file

    # THIS IS HARD-CODED FOR 5 MINUTES VIDEO SPLIT
    options['split_length'] = 300    
    #######################
    
    def bailout():
        parser.print_help()
        raise SystemExit

    if not options['filename']:
        bailout()

    video_length = None
    if not options['split_length']:
        video_length = get_video_length(options['filename'])
        file_size = os.stat(options['filename']).st_size
        split_filesize = None
        if options['split_filesize']:
            split_filesize = int(options['split_filesize'] * options['filesize_factor'])
        if split_filesize and options['chunk_strategy'] == 'even':
            options['split_chunks'] = ceildiv(file_size, split_filesize)
        if options['split_chunks']:
            options['split_length'] = ceildiv(video_length, options['split_chunks'])
        if not options['split_length'] and split_filesize:
            options['split_length'] = int(split_filesize / float(file_size) * video_length)
    if not options['split_length']:
        bailout()
    split_by_seconds(filename = options['filename'], split_length = options['split_length'], video_length=video_length)

def main():
    path = "./"
    files = [f for f in list_files_in_directory(path) if f.endswith('.mov') or f.endswith('.AVI')]
    print(files)

    for file in files:
        split_single_video(file)


if __name__ == '__main__':
    main()
