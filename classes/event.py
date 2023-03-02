from classes.time import Time

class Event():
    def __init__(self, _due_time: Time, action:str='') -> None:
        self.due_time = _due_time
        self.action = ''


daily_events = {'hunger_1st_point': Event(Time((0,12,0)), action='ph*1'),
                'hunger_2nd_point': Event(Time((0,18,0)), action='ph*1'),
                'hunger_3rd_point': Event(Time((0,23,59)), action='ph*1'),}