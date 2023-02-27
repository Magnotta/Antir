from __future__ import annotations

class Time:
    def __init__(self, tm = (0, 0, 0)) -> None:
        self.d = tm[0]
        self.h = tm[1]
        self.m = tm[2]
        self.mins = self.d*1440 + self.h*60 + self.m

    def __add__(self, other):
        if isinstance(other, Time):
            __r =  (self.d + other.d, self.h + other.h, self.m + other.m)
        elif isinstance(other, tuple):
            __r = (self.d + other[0], self.h + other[1], self.m + other[2])
        else:
            raise TypeError(f"unsupported operand types for +: {type(self)} and {type(other)}")

        if __r[2] >= 60:
            __r = (__r[0], __r[1] + (__r[2]//60), __r[2] % 60)
        if __r[1] >= 24:
            __r = (__r[0] + (__r[1]//24), __r[1] % 24, __r[2])
            
        return Time(__r)

    def __repr__(self) -> str:
        return f"{self.d}, {self.h}:{self.m}"
    
    def __str__(self) -> str:
        return f"{self.d}, {self.h}:{self.m}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.mins == other.mins
        elif isinstance(other, tuple):
            return self.time == other
        return False
    
    def __lt__(self, other: Time):
        return self.mins < other.mins
    
    def __gt__(self, other: Time):
        return self.mins > other.mins

    def minutes_until(self, stop: Time):
        list_minutes = []
        copy = Time((self.d,self.h,self.m))
        while copy < stop:
            list_minutes.append(copy)
            copy += (0,0,1)
        return list_minutes
    
    def hours_until(self, stop: Time):
        list_hours = []
        copy = Time((self.d,self.h,self.m))
        while copy < stop:
            list_hours.append(copy)
            copy += (0,1,0)
        return list_hours
    
    @classmethod
    def from_int_mins(cls, total_mins: int):
        days = total_mins // 1440
        total_mins %= 1440
        hours = total_mins // 60
        total_mins %= 60
        mins = total_mins

        return (days,hours,mins)