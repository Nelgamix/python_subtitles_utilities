import math


def create_time(mt):
    if mt > 60 * 60 * 1000:
        hours = math.floor(mt / (60 * 60 * 1000))
        mt %= (60 * 60 * 1000)
    else:
        hours = 0

    if mt > 60 * 1000:
        minutes = math.floor(mt / (60 * 1000))
        mt %= (60 * 1000)
    else:
        minutes = 0

    if mt > 1000:
        seconds = math.floor(mt / 1000)
        mt %= 1000
    else:
        seconds = 0

    milliseconds = mt
    return Time(hours, minutes, seconds, milliseconds)


def create_mt(time):
    return time.hours * 60 * 60 * 1000 + time.minutes * 60 * 1000 + time.seconds * 1000 + time.milliseconds


class Time:
    def __init__(self, hours=0, minutes=0, seconds=0, milliseconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.milliseconds = milliseconds
        self.generate_mt()

    def get_formatted(self):
        return str(self.hours).zfill(2) + ':' + str(self.minutes).zfill(2) + ':' + \
               str(self.seconds).zfill(2) + ',' + str(self.milliseconds).zfill(3)

    def shift(self, shift):
        mtt = self.mt
        mts = shift.mt
        mtr = mtt + mts
        self.set_time_from_mt(mtr)

    def generate_mt(self, time = None):
        if time is not None:
            mt = time.milliseconds
            mt += time.seconds * 1000
            mt += time.minutes * 60 * 1000
            mt += time.hours * 60 * 60 * 1000
        else:
            mt = self.milliseconds
            mt += self.seconds * 1000
            mt += self.minutes * 60 * 1000
            mt += self.hours * 60 * 60 * 1000
            self.mt = mt
        return mt

    def set_time_from_mt(self, mt):
        if mt > 60 * 60 * 1000:
            self.hours = math.floor(mt / (60 * 60 * 1000))
            mt %= (60 * 60 * 1000)
        else:
            self.hours = 0

        if mt > 60 * 1000:
            self.minutes = math.floor(mt / (60 * 1000))
            mt %= (60 * 1000)
        else:
            self.minutes = 0

        if mt > 1000:
            self.seconds = math.floor(mt / 1000)
            mt %= 1000
        else:
            self.seconds = 0

        self.milliseconds = mt

    # def verify(self):
    #     if self.milliseconds < 0:
    #         self.seconds += math.ceil(self.milliseconds / 1000)
    #         self.milliseconds = math.fabs(self.milliseconds % 1000)
    #     if self.seconds < 0:
    #         self.minutes += math.ceil(self.seconds / 60)
    #         self.seconds = math.fabs(self.seconds % 60)
    #     if self.minutes < 0:
    #         self.hours += math.ceil(self.minutes / 60)
    #         self.minutes = math.fabs(self.minutes / 60)
    #
    #     if self.milliseconds >= 1000:
    #         self.seconds += math.floor(self.milliseconds / 1000)
    #         self.milliseconds %= 1000
    #     if self.seconds >= 60:
    #         self.minutes += math.floor(self.seconds / 60)
    #         self.seconds %= 60
    #     if self.minutes >= 60:
    #         self.hours += math.floor(self.minutes / 60)
    #         self.minutes %= 60
    #
    #     self.milliseconds = int(self.milliseconds)
    #     self.seconds = int(self.seconds)
    #     self.minutes = int(self.minutes)
    #     self.hours = int(self.hours)

    def is_before(self, time):
        if self.hours < time.hours:
            return True
        elif self.hours > time.hours:
            return False

        if self.minutes < time.minutes:
            return True
        elif self.minutes > time.minutes:
            return False

        if self.seconds < time.seconds:
            return True
        elif self.seconds > time.seconds:
            return False

        if self.milliseconds < time.milliseconds:
            return True
        elif self.milliseconds > time.milliseconds:
            return False
        else:
            return False

    def is_after(self, time):
        if self.hours > time.hours:
            return True
        elif self.hours < time.hours:
            return False

        if self.minutes > time.minutes:
            return True
        elif self.minutes < time.minutes:
            return False

        if self.seconds > time.seconds:
            return True
        elif self.seconds < time.seconds:
            return False

        if self.milliseconds > time.milliseconds:
            return True
        elif self.milliseconds < time.milliseconds:
            return False
        else:
            return False
