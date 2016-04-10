from Subtitle import Subtitle, Subtitles
import sys, os, glob, re


subs = Subtitles() # Contains all the subtitles

settings = {
    'general': {
        'files': []
    },
    'move': {
        'write_out': False
    },
    'rename': {
        'pattern': { # 0 for Season, 1 for episode
            'subtitle': '0x11', # Format XxXX
            'clip': '00x11' # Format SXXEXX
        },
        'extension': {
            'subtitle': 'srt',
            'clip': 'mkv'
        }
    }
}


def move():
    for f in settings['general']['files']:
        file = open(f, 'r') # Open the file on read mode

        sub = Subtitle()
        line_c = 1

        for line in file: # For each line in the file
            if line != "\n": # If this is not a blank line
                if line_c == 1: # If this is the first line of a subtitle
                    try: # First line throws an exception
                        sub.number = int(line) # First line throws an exception, others don't
                    except:
                        sub.number = 1 # The first line is 1
                elif line_c == 2: # If this is the second line of a subtitle
                    times = line.split(' --> ') # Split the line into 2 times (begin and end)
                    sub.begin = times[0] # Assign begin time to begin variable
                    sub.end = times[1] # Assign begin end to end variable
                else: # Else we append the text
                    sub.text.append(line)
                line_c += 1 # And we increment the line counter
            else: # Else we have a subtitle ready
                if sub.validate(): subs.add_sub(sub) # We append the subtitle to the list
                sub = Subtitle() # We create a new one
                line_c = 1 # We reset the line counter

        if sub.validate(): subs.add_sub(sub)
        del sub
        del line_c
        file.close()

        # USER INSTRUCTION TO MANIPULATE THE SUBS BEFORE WRITING OUT ON A FILE
        #shift(Time(0, 0, 2, 0))
        #subs.shift_after(Time(1), Time(0, 10))
        #subs.split_all()
        #subs.sort()
        # END OF USER INSTRUCTIONS

        #subs.show_all()

        if settings['move']['write_out']:
            with open(f.split('.')[0] + '_test.' + \
                    f.split('.')[-1], 'w') as fil:
                subs.write_all(fil)


def rename():
    if len(settings['general']['files']) > 0:
        dira = settings['general']['files'][0]
        if dira[-1] != '/' or dira != '\\':
            dira += "/"
    else:
        dira = ''

    pe = re.sub('\d', '[0-9]', settings['rename']['pattern']['clip'])
    pat = '*' + pe + "*." + \
            settings['rename']['extension']['clip']
    #print(pat)
    for f in glob.glob(dira + pat):
        f = f.replace('\\', '/')
        print(" * Searching subtitles file for {} ...".format(f))
        for m in re.findall(pe, str(f)[str(f).rfind('/'):]):
            #print(m)
            season = ''
            episode = ''
            ind = 0
            inds = []

            # SEASON FINDING
            while True: # Find index in the pattern
                ind = settings['rename']['pattern']['clip'].find('0', ind)
                if ind != -1:
                    inds.append(ind)
                else:
                    break
                ind += 1
            for i in inds: # find season
                season += m[i]
            season = int(season)
            #print(season)

            ind = 0
            inds.clear()

            # EPISODE FINDING
            while True: # Find index in the pattern
                ind = settings['rename']['pattern']['clip'].find('1', ind)
                if ind != -1:
                    inds.append(ind)
                else:
                    break
                ind += 1
            for i in inds: # find season
                episode += m[i]
            episode = int(episode)
            #print(episode)

            # SUBTITLE CORRESPONDING
            aa = settings['rename']['pattern']['subtitle']
            ab = aa.count('0') # Counting the occurences of 0 in the pattern
            ac = aa.index('0') # Finding the first index of 0 in the pattern
            ad = aa[0:ac] + str(season).zfill(ab) + aa[ac+ab:] # Replacing the season
            ae = aa.count('1') # Counting the occurences of 1 in the pattern
            af = aa.index('1') # Finding the first index of 1 in the pattern
            ag = ad[0:af] + str(episode).zfill(ae) + ad[af+ae:] # Replacing the episode
            #print(ag)

            found = False
            for subf in glob.glob(dira + '*' + ag + "*." + settings['rename']['extension']['subtitle']):
                print(" ** Subtitles file: " + subf)
                os.rename(subf, f[0:f.rfind('.')] + ".srt")
                found = True
            if not found:
                print(" *xxxxx* Couldn't find the subtitles attached to {}.".format(f))


def check_files():
    for f in settings['general']['files']:
        assert os.path.exists(f), "FILE/DIR {} DOES'T EXISTS. PLEASE CHECK SPELLING.".format(f)


def correct_filename():
    for fi in range(len(settings['general']['files'])):
        if os.path.exists(settings['general']['files'][fi]) \
        and os.path.isdir(settings['general']['files'][fi]):
            pass
        else:
            try:
                settings['general']['files'][fi].index('.')
            except ValueError:
                settings['general']['files'][fi] += '.srt'


def main():
    assert len(sys.argv) >= 2, "YOU MUST SPECIFY A MODE"
    for i in range(len(sys.argv)):
        if i >= 2: settings['general']['files'].append(sys.argv[i])

    correct_filename()
    check_files()

    if sys.argv[1] == "move":
        move()
    elif sys.argv[1] == "rename":
        rename()


if __name__ == "__main__":
    main()
