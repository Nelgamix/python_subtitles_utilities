# Python subtitles utility
Python program used to manipulate subtitle files (shifting, renaming...).

Useful for series.

## Usage
You should have python 3.5 installed, and have it in the PATH.

Then, just download this repository and extract it somewhere.

Then, launch the command line utility (or a bash) and launch the program with "python main.py"

You must add some args to specify what you want to do with it.

The first arg to add is the mode. "move" let you shift subtitles, and "rename" automatically finds
subtitles and renames them to the same name as the clip in the same folder.

Make sure to edit the config.ini file which contains the settings about the environment you are using.

### Move command
The move command let you shift subtitle in various ways, from a simple global shift of all the subtitles,
to a selective shift (shift before, shift between, shift after). But you can also sort the list, and split them.
The sorting just takes every time of the beginning and sort the subtitles according to that.
The splitting is more specific but may be useful: it take a subtitle written onto two lines (ore more),
and split into several. For example, if you have a subtitle on two line from 0 to 5 secs, the split will
simply translate that into one subtitle with the first line and will last from 0 to 2.5 secs,
and a second one with the second line from 2.5 to 5 secs.

To use the move command, you have to specify at least one file after the command, then the interactive mode will let
you choose what you need to do.

### Rename command
This command runs a simple algorithm which will attempt to find subtitles in a folder and rename them with the same
name as the movies also present on this folder. However, this is actually the reverse thing: the algorithm find a clip,
finds the season and episode number, and attempts to find its subtitle file based on the pattern provided by the user.

To use the rename command, you can (not mandatory) specify a folder. If you don't, the current directory will be used.

### Clean command
This will just clean all the files having the extension `.srt~`. Used to clean the mess made with the automatic backup
when you're done.

## Examples
```
python move_subtitles.py move subtitle.srt # Runs the move on this file
python move_subtitles.py move subtest.srt subtest2.srt # Runs the move on those two files
python move_subtitles.py rename # Will run the rename in the actual folder
python move_subtitles.py rename ../../Documents/Movies/Movie1 # Runs the rename in the Movie1 directory
python clean # clean the current directory of all .srt~ files
```

If you have set correctly the python association and the path, you can do this:
```
move_subtitles.py [mode] [arg]
```

