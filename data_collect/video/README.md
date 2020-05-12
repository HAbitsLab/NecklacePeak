# Necklace

Requirement: 

* Install ffmpeg: `https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg`
* The videos are in .AVI format, which is always true for HAbitslab wearable camera v1 videos.

## Split video into subvideos
Use a batch paradigm to split multiple videos into subvideos with same length.

### Instruction:

1. copy `ffmpeg-split-batch.py` to the folder containing videos (with no videos in any subfolder).
2. run python script `ffmpeg-split-batch.py`, then you will see generated subvideos in the same directory.


## Count videos length

### Instruction:

1. copy `ffprobe_len.py` into the video folder (with no videos in any subfolder).
2. Then run it, you will see the total length in second