from classes.time import Time

class Event():
    def __init__(self, due_time: Time, func):
        self.due_time = due_time
        self.func = func

class Recurring_Event(Event):
    def __init__(self, due_time: Time, func, recurrences):
        super().__init__(due_time, func)

class Lasting_Event(Event):
    def __init__(self, due_time: Time, func, duration):
        super().__init__(due_time, func)



class Event_Engine():
    def __init__(self, g):
        self.g = g

        self.events:list[Event] = []
        self.hourly_events:list[Recurring_Event] = []
        self.daily_events:list[Recurring_Event] = []

    def update(self):
        if self.g.time.hour_change():
            pass

        if self.g.time.day_change():
            self.events.append(Event(Time((self.g.time.d,8,0)), self.day_hunger))
            self.events.append(Event(Time((self.g.time.d,12,0)), self.day_hunger))
            self.events.append(Event(Time((self.g.time.d,18,0)), self.day_hunger))
            self.events.append(Event(Time((self.g.time.d,23,59)), self.night_hunger))
            # PDR

        for e in self.events:
            if e.due_time == self.g.time:
                e.func()

        for e in self.hourly_events:
            pass

        for e in self.daily_events:
            pass

    def day_hunger(self):
        self.g.hunger_all()

    def night_hunger(self):
        for p in self.g.players:
            if not p.asleep():
                p.addHunger(1)

