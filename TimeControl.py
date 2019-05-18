from datetime import datetime


class TimeControl:
    
    def __init__(self, timeslots):
        self.timeslots = timeslots
    
    def check_time(self, time):
        for timeslot in self.timeslots:
            if (time > timeslot[0]) and (time < timeslot[1]):
                print(time, "ist im Zeitintervall")
                return True
        print(time, "ist nicht im Zeitintervall")
        return False


if __name__ == '__main__':
    #Zeitslots
    DAY0_START = datetime(year=2019, month=1, day=1, hour=0, minute=0)
    DAY0_END = datetime(year=2019, month=6, day=6, hour=3, minute=0)
    DAY1_START = datetime(year=2019, month=6, day=6, hour=9, minute=0)
    DAY1_END = datetime(year=2019, month=6, day=6, hour=21, minute=0)
    DAY2_START = datetime(year=2019, month=6, day=7, hour=9, minute=0)
    DAY2_END = datetime(year=2019, month=6, day=7, hour=21, minute=0)
    DAY3_START = datetime(year=2019, month=6, day=8, hour=9, minute=0)
    DAY3_END = datetime(year=2019, month=6, day=8, hour=21, minute=0)
    DAY4_START = datetime(year=2019, month=6, day=9, hour=9, minute=0)
    DAY4_END = datetime(year=2019, month=6, day=9, hour=21, minute=0)
    DAY5_START = datetime(year=2019, month=6, day=10, hour=9, minute=0)
    DAY5_END = datetime(year=2019, month=6, day=10, hour=21, minute=0)
    
    TIMESLOTS = [(DAY0_START, DAY0_END),
                 (DAY1_START, DAY1_END),
                 (DAY2_START, DAY2_END),
                 (DAY3_START, DAY3_END),
                 (DAY4_START, DAY4_END)]
    
    time1 = datetime(2019, 4, 29, 17, 30)
    time2 = datetime(2019, 4, 29, 19, 30)
    time3 = datetime(2019, 4, 21, 17, 30)
    time4 = datetime.now()
    
    timecontrol = TimeControl(TIMESLOTS)
    
    timecontrol.check_time(time1)
    timecontrol.check_time(time2)
    timecontrol.check_time(time3)
    timecontrol.check_time(time4)
