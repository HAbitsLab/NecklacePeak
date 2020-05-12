# INSTRUCTION: copy this script into the video folder, then run it.

import os
import subprocess


def list_files_in_directory(mypath):
    return [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]


def get_duration(file):
    try:
        """Get the duration of a video using ffprobe."""
        cmd = 'ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(file)
        output = subprocess.check_output(
            cmd,
            shell=True, # Let this run in the shell
            stderr=subprocess.STDOUT
        )
        return float(output)
    except:
        return 0

    # return round(float(output))  # ugly, but rounds your seconds up or down


def main():
    path = "./"
    files = [f for f in list_files_in_directory(path) if f.endswith('.MP4') or f.endswith('.AVI')]
    print(files)
    ttl = 0

    for file in files:
        print(file)
        t = get_duration(file)
        print(t)
        ttl += t

    print('Seconds:', ttl)
    print('Hours:', ttl/60/60)


if __name__ == '__main__':
    main()
