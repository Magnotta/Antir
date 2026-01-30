from __future__ import annotations

class Time:
    def __init__(self, tm:int=0) -> None:
        self.tick = tm
        self.d = tm//1440
        self.h = tm%1440//60
        self.m = tm%60
        self.day_change = False
        self.hour_change = False



    def __add__(self, other):
        if isinstance(other, Time):
            __r =  Time(self.tick + other.tick)
        elif isinstance(other, int):
            __r = Time(self.tick + other)
        else:
            raise TypeError(f"unsupported operand types for +: {type(self)} and {type(other)}")
            
        __r._day_change(self)
        __r._hour_change(self)
        return __r
    

    
    def __str__(self) -> str:
        if self.h < 10:
            if self.m < 10:
                return f"Dia {self.d}   0{self.h}:0{self.m}"
            else:
                return f"Dia {self.d}   0{self.h}:{self.m}"
        else:
            if self.m < 10:
                return f"Dia {self.d}   {self.h}:0{self.m}"
            else:
                return f"Dia {self.d}   {self.h}:{self.m}"



    def __eq__(self, other: object) -> bool:
        if isinstance(other, Time):
            return self.tick == other.tick
        elif isinstance(other, int):
            return self.tick == other
        else:          
            return False


    
    def __lt__(self, other: object):
        if isinstance(other, Time):
            return self.tick < other.tick
        elif isinstance(other, int):
            return self.tick < other
        else:          
            return False
    

    
    def __gt__(self, other: Time):
        if isinstance(other, Time):
            return self.tick > other.tick
        elif isinstance(other, int):
            return self.tick > other
        else:          
            return False
    


    def ticks_until(self, stop: Time):
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
    
    
    
    def _hour_change(self, other:Time):
        if self.h != other.h:
            self.hour_change = True
    
    
    
    def _day_change(self, other:Time):
        if self.d != other.d:
            self.day_change = True
