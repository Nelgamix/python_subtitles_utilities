import re
from Time import *
import math


# Holds a single subtitle.
# Contains a number, a begin time, an end time, and lines of text.
class Subtitle:
    def __init__(self, number=0, begin='', end='', text=None):
        self.number = number
        self.begin = begin
        self.end = end
        if text is None:
            self.text = []
        else:
            self.text = text

    # Used to validate the content of the subtitle.
    # Mandatory because it generates times.
    # Also generate the mt, which is used to describe the position of the
    # subtitle among others.
    # @return valid True if validate is successful, False otherwise
    def validate(self):
        if self.number == 0 or self.begin == '' or self.end == '' or self.text is None: return False
        zbegin = re.split('\W+', self.begin)
        zend = re.split('\W+', self.end)
        self.time_begin = Time(int(zbegin[0]), int(zbegin[1]), int(zbegin[2]), int(zbegin[3]))
        self.time_end = Time(int(zend[0]), int(zend[1]), int(zend[2]), int(zend[3]))
        self.set_mt()
        del self.begin
        del self.end
        return True

    # Prints the entire subtitle at cout as if it was written in a .srt file
    # @return none
    def show(self):
        print(str(self.number))
        print(self.time_begin.get_formatted() + ' --> ' + self.time_end.get_formatted())
        for line in self.text:
            print(line, end='')
        print('')

    # Generate the mt based on the beginning time of the subtitle
    # @return none
    def set_mt(self):
        self.mt = self.time_begin.generate_mt()

    # Write the subtitle on the file provided
    # @param file The file to be written to
    # @return none
    def write(self, file):
        file.write(str(self.number) + "\n")
        file.write(self.time_begin.get_formatted() + ' --> ' + self.time_end.get_formatted() + "\n")
        for line in self.text:
            file.write(line)
        file.write("\n")

    # Shift the subtitle by shift Time
    # @param shift The time to shift the subtitle
    def shift(self, shift):
        self.time_begin.shift(shift)
        self.time_end.shift(shift)
        self.set_mt()

    # Know if the subtitle begins after time Time
    # @param time The time to be compared to
    # @return boolean True if the subtitle begins after the time provided, False otherwise
    def begins_after(self, time):
        return self.time_begin.is_after(time)

    # Know if the subtitle begins before time Time
    # @param time The time to be compared to
    # @return boolean True if the subtitle begins before the time provided, False otherwise
    def begins_before(self, time):
        return self.time_begin.is_before(time)


# Holds all the subtitles.
# Can be used to manipulate the subtitles, and/or access them.
class Subtitles:
    def __init__(self):
        self.subs = []

    def add_sub(self, sub):
        assert isinstance(sub, Subtitle), "ADD_SUB: SUB MUST BE A SUBTITLE"
        self.subs.append(sub)

    def show_all(self):
        for sub in self.subs:
            sub.show()

    def split_all(self):
        new_sub_list = []
        for sub in self.subs:
            if len(sub.text) > 1:
                time_b = sub.time_begin.generate_mt()  # mt of the beginning
                time_e = sub.time_end.generate_mt()  # mt of the end
                diff = time_e - time_b  # Difference between the two above
                diff_t = math.floor(diff / len(sub.text))  # Time that one sub must last
                for text in sub.text:
                    begin = create_time(time_b)
                    end = create_time(time_b + diff_t)
                    nsub = Subtitle(1, begin.get_formatted(), end.get_formatted(), (text,))
                    nsub.validate()
                    new_sub_list.append(nsub)
                    time_b += diff_t
            else:
                new_sub_list.append(sub)
        self.subs = new_sub_list

    def sort(self):
        self.subs.sort(key=lambda x: x.mt, reverse=False)
        i = 1
        for sub in self.subs:
            sub.number = i
            i += 1

    def write_all(self, file):
        for sub in self.subs:
            sub.write(file)

    def remove_negative(self):
        new_list = []
        for sub in self.subs:
            if sub.mt > 0:
                new_list.append(sub)
        self.subs = new_list

    # Shift all the subtitles by the Time provided in 'shift' variable
    # @param shift The time to add
    # @return none
    def shift(self, shift):
        assert isinstance(shift, Time), 'SHIFT MUST BE A TIME'
        for sub in self.subs:
            sub.shift(shift)

    # Shift the subtitles by the Time provided in 'shift' variable
    # Only subtitles beginning after the 'position' Time will be shifted
    # @param position The time from which the subtitles will be affected
    # @param shift The time to add
    # @return none
    def shift_after(self, position, shift):
        assert isinstance(shift, Time), 'SHIFT MUST BE A TIME'
        assert isinstance(position, Time), 'POSITION MUST BE A TIME'
        for sub in self.subs:
            if sub.begins_after(position):
                sub.shift(shift)

    # Shift all the subtitles by the Time provided in 'shift' variable
    # Only subtitles beginning before the 'position' Time will be shifted
    # @param position The time before which the subtitles will be affected
    # @param shift The time to add
    # @return none
    def shift_before(self, position, shift):
        assert isinstance(shift, Time), 'SHIFT MUST BE A TIME'
        assert isinstance(position, Time), 'POSITION MUST BE A TIME'
        for sub in self.subs:
            if sub.begins_before(position):
                sub.shift(shift)

    # Shift all the subtitles by the Time provided in 'shift' variable
    # Only subtitles beginning after the 'position_after' Time and
    # beginning before the 'position_before' Time will be affected
    # @param position_after The time from which the subtitles will be affected
    # @param position_before The time before which the subtitles will be affected
    # @param shift The time to add
    # @return none
    def shift_between(self, position_after, position_before, shift):
        assert isinstance(shift, Time), 'SHIFT MUST BE A TIME'
        assert isinstance(position_after, Time), 'POSITION MUST BE A TIME'
        assert isinstance(position_before, Time), 'POSITION MUST BE A TIME'
        for sub in self.subs:
            if sub.begins_before(position_before) and sub.begins_after(position_after):
                sub.shift(shift)
