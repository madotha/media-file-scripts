# media-file-scripts

A collection of scripts I made for personal use, mostly generated with ChatGPT.
These should assist in finding specific sets of files and directories in a file structure.
They are mostly used on Mac, therefore the required dependencies can be retrieved through `pip` and `homebrew`.

## funxd-finder

Used to find directories containing 'funxd.mkv' files.  
Usage:

```
python funxd-finder.py -v -d /path/to/starting-directory

-v : verbose mode
-d : define starting directory
```

## tmdb-finder

Used to find directories which do not have a `{tmdb-123456}` extension.  
Usage:

```
python tmdb-finder.py -v -d /path/to/starting-directory

-v : verbose mode
-d : define starting directory
-s : series mode, ignores Season and Specials directories
```

## video-codec-analyser

Used mainly to find files, which are not HEVC encoded. In verbose mode, HEVC files will be green and all other red.
Output can be found in corresponding `errors` and `not_hevc` folders.  
Usage:

```
python video-codec-analyser.py -v -d /path/to/starting-directory

-v : verbose mode
-d : define starting directory
```

## videofile-infos

Get simple info about codec, bitrate and resolution of a video file.  
Usage:

```
python videofile-infos.py filename.mkv
```