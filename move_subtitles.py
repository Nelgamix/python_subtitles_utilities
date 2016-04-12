from Subtitle import Subtitle, Subtitles
import sys, os, glob, re, configparser, shutil
from Time import Time

# TODO: CUT PARTS

subs = Subtitles()  # Contains all the subtitles

settings = {
    'general': {
        'files': []
    },
    'move': {
        'write_out': True  # More or less useless..
    }
}
config = configparser.ConfigParser()
rp = os.path.dirname(os.path.realpath(__file__))


def get_settings():
    config_file = 'config.ini'
    assert os.path.exists(rp + "/" + config_file) and os.path.isfile(rp + "/" + config_file), "CONFIG FILE DOESN'T EXIST."

    config.read(rp + '/' + config_file)


def clean():
    print("Cleaning directory...")
    for fod in glob.glob('*.srt~'):
        os.remove(fod)
        print('Removed ' + fod)


def move(instructions):
    for f in settings['general']['files']:
        file = open(f, 'r')  # Open the file on read mode

        sub = Subtitle()
        line_c = 1

        for line in file:  # For each line in the file
            if line != "\n":  # If this is not a blank line
                if line_c == 1:  # If this is the first line of a subtitle
                    try:  # First line throws an exception
                        sub.number = int(line)  # First line throws an exception, others don't
                    except ValueError:
                        sub.number = 1  # The first line is 1
                elif line_c == 2:  # If this is the second line of a subtitle
                    times = line.split(' --> ')  # Split the line into 2 times (begin and end)
                    sub.begin = times[0]  # Assign begin time to begin variable
                    sub.end = times[1]  # Assign begin end to end variable
                else:  # Else we append the text
                    sub.text.append(line)
                line_c += 1  # And we increment the line counter
            else:  # Else we have a subtitle ready
                if sub.validate():
                    subs.add_sub(sub)  # We append the subtitle to the list
                sub = Subtitle()  # We create a new one
                line_c = 1  # We reset the line counter

        if sub.validate():
            subs.add_sub(sub)
        del sub
        del line_c
        file.close()

        for inst in instructions:
            if inst[0] == "shift":
                subs.shift(inst[1])
            elif inst[0] == "shift before":
                subs.shift_before(inst[1], inst[2])
            elif inst[0] == "shift between":
                subs.shift_between(inst[1], inst[2], inst[3])
            elif inst[0] == "shift after":
                subs.shift_after(inst[1], inst[2])
            elif inst[0] == "sort":
                subs.sort()
            elif inst[0] == "split":
                subs.split_all()
            # ...

        # USER INSTRUCTION TO MANIPULATE THE SUBS BEFORE WRITING OUT ON A FILE
        # shift(Time(0, 0, 2, 0))
        # subs.shift_after(Time(1), Time(0, 10))
        # subs.split_all()
        # subs.sort()
        # END OF USER INSTRUCTIONS

        # subs.show_all()

        if config['DEFAULT'].getboolean('REMOVE_NEGATIVE_SUBTITLES'):
            subs.remove_negative()

        if config['DEFAULT'].getboolean('AUTOMATIC_SORT'):
            subs.sort()

        if config['DEFAULT'].getboolean('FILE_BACKUP'):  # CHANGE THIS PLEASE
            shutil.copyfile(f, f + "~")

        if config['DEFAULT'].getboolean('FILE_REPLACE'):
            with open(f, 'w') as fil:
                subs.write_all(fil)
        else:
            with open(f.split('.')[0] + '_corrected.' + f.split('.')[-1], 'w') as fil:
                subs.write_all(fil)


def interactive_mode():
    instructions = []
    uinput = "A"
    while uinput != "":
        uinput = input("What operation do you want to do? [shift/shift before/shift after/split/sort/list/ok]: ")
        if uinput == "shift":
            time = ask_time("to shift")
            instructions.append(['shift', time])
        elif uinput == "shift before":
            time1 = ask_time("before which to shift")
            time2 = ask_time("to shift")
            instructions.append(['shift before', time1, time2])
        elif uinput == "shift between":
            time1 = ask_time("after which to shift")
            time2 = ask_time("before which to shift")
            time3 = ask_time("to shift")
            instructions.append(['shift between', time1, time2, time3])
        elif uinput == "shift after":
            time1 = ask_time("after which to shift")
            time2 = ask_time("to shift")
            instructions.append(['shift after', time1, time2])
        elif uinput == "split":
            instructions.append(['split'])
        elif uinput == "sort":
            instructions.append(['sort'])
        elif uinput == "list":
            for inst in instructions:
                print(inst[0])
        elif uinput == "ok":
            move(instructions)
            break
        elif uinput == "debug":
            for inst in instructions:
                print(inst[0])
        elif uinput == "":
            pass
        else:
            print("We didn't catch what you want to do. Retry or enter a blank line to quit.")


def user_input(description = ""):
    if description == "":
        phrase = "Please enter a number: "
    else:
        phrase = "How many {}?: ".format(description)

    while True:
        try:
            uinput = input(phrase)
            if uinput != "":
                uinput = int(uinput)
            else:
                return 0
            return uinput
        except ValueError:
            print("This is not a correct time. Please retry.")


def ask_time(reason):
    print("Please enter a time " + reason + ".")

    hours = user_input("hours")
    minutes = user_input("minutes")
    seconds = user_input("seconds")
    milliseconds = user_input("milliseconds")

    return Time(hours, minutes, seconds, milliseconds)


def rename():
    if len(settings['general']['files']) > 0:
        dira = settings['general']['files'][0]
        if dira[-1] != '/' or dira != '\\':
            dira += "/"
    else:
        dira = ''

    pe = re.sub('\d', '[0-9]', config['DEFAULT']['CLIP_PATTERN'])
    pat = '*' + pe + "*." + \
          config['DEFAULT']['CLIP_EXTENSION'].lower()
    # print(pat)
    for f in glob.glob(dira + pat):
        f = f.replace('\\', '/')
        print(" * Searching subtitles file for {} ...".format(f))
        for m in re.findall(pe, str(f)[str(f).rfind('/'):]):
            # print(m)
            season = ''
            episode = ''
            ind = 0
            inds = []

            # SEASON FINDING
            while True:  # Find index in the pattern
                ind = config['DEFAULT']['CLIP_PATTERN'].find('0', ind)
                if ind != -1:
                    inds.append(ind)
                else:
                    break
                ind += 1
            for i in inds:  # find season
                season += m[i]
            season = int(season)
            # print(season)

            ind = 0
            inds.clear()

            # EPISODE FINDING
            while True:  # Find index in the pattern
                ind = config['DEFAULT']['CLIP_PATTERN'].find('1', ind)
                if ind != -1:
                    inds.append(ind)
                else:
                    break
                ind += 1
            for i in inds:  # find season
                episode += m[i]
            episode = int(episode)
            # print(episode)

            # SUBTITLE CORRESPONDING
            aa = config['DEFAULT']['SUBTITLE_PATTERN']
            ab = aa.count('0')  # Counting the occurrences of 0 in the pattern
            ac = aa.index('0')  # Finding the first index of 0 in the pattern
            ad = aa[0:ac] + str(season).zfill(ab) + aa[ac + ab:]  # Replacing the season
            ae = aa.count('1')  # Counting the occurrences of 1 in the pattern
            af = aa.index('1')  # Finding the first index of 1 in the pattern
            ag = ad[0:af] + str(episode).zfill(ae) + ad[af + ae:]  # Replacing the episode
            # print(ag)

            found = False
            for subf in glob.glob(dira + '*' + ag + "*." + config['DEFAULT']['SUBTITLE_EXTENSION'].lower()):
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
        if i >= 2:
            settings['general']['files'].append(sys.argv[i])

    correct_filename()
    check_files()

    if sys.argv[1] == "move":
        interactive_mode()
    elif sys.argv[1] == "rename":
        rename()
    elif sys.argv[1] == "clean":
        clean()


if __name__ == "__main__":
    get_settings()
    main()
