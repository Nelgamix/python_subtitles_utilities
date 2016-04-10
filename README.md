# python_subtitles_utilities
Python program used to manipulate subtitle files (shifting, renaming...)

## Usage
You should have python 3.5 installed, and have it in the PATH.

Then, just download this repository and extract it somewhere.

Then, launch the command line utility (or a bash) and launch the program with "python main.py"

You must add some args to specify what you want to do with it.

The first arg to add is the mode. "move" let you shift subtitles, and "rename" automatically finds
subtitles and renames them to the same name as the clip in the same folder.

## Exemples
```
python main.py move subtitle.srt
python main.py rename ../../Documents/Movies/Movie1
```

...
