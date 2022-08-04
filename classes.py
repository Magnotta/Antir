# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 16:31:15 2022

@author: ndd2
"""

from math import exp, sqrt
from uuid import uuid1, UUID
import tkinter as tk
import tkinter.ttk as ttk
import refs

class Entity:
    def __init__(self, id=None):
        if(id is None):
            self.id = UUID(uuid1().hex)
        else:
            self.id = UUID(id)



class Item(Entity):
    def __init__(self, name, qty=1, isContainer=False):
        super().__init__()
        self.drblt: int = 100
        self.kgs: int = 0
        self.name: str = name
        self.qty: int = qty
        self.isContainer = isContainer
        self.storedItems = []
        
    def storeItem(self, item):
        if(not self.isContainer):
            print('Non container items cannot store other items!')
            return
        
        if(item.isContainer):
            print('Cannot store container item inside another container!')
            return
        
        self.storedItems.append(item)



class Cover(Item):
    def __init__(self):
        super().__init__()
        self.mat: str = None



class Weapon(Item):
    def __init__(self):
        super().__init__()
        self.mat: str = None
        self.mode: str = 'blunt'



class BodyPart:
    def __init__(self):
        self.health = 100
        self.cover: Cover = None
        self.status: str = 'normal'



class Player(Entity):
    def __init__(self, name, id=None):
        super().__init__(id=id)
        self.name: str = name
        self.pneuma: int = 100
        self.pdr: int = 0
        self.blood: int = 100
        self.bloodLoss: int = 0
        self.stamina: int = 100
        self.tiredLvl: int = 0
        self.hungerPts: int = 0
        self.cdims = {'ímpeto':0,'agilidade':0,'precisão':0,'defesa':0}
        self.cdimsTot: int = 6
        self.cdimsRsvd = {'ímpeto':0,'agilidade':0,'precisão':0,'defesa':0}
        self.wpn: Weapon = None
        self.invtry = []
        self.sleeping: bool = False

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.id == other.id

        return False
         
    def setCdim(self, cdimName, cdimVal):
        if(cdimVal < self.cdimsRsvd[cdimName]):
            print(f'Failed to assign value {cdimVal} to {cdimName}: smaller than reserved. Min allowed is {self.cdimsRsvd[cdimName]}.')
            return
        
        sum = cdimVal
        for k,v in self.cdims.items():
            if(k != cdimName):
                sum += v
        
        if(sum > self.cdimsTot):
            excess = sum - self.cdimsTot
            print(f'Failed to assign value {cdimVal} to {cdimName}: total cdims overshoot. Max allowed is {cdimVal - excess}.')
            return
        
        self.cdims[cdimName] = cdimVal
        
    def loadFromFile(self):
        pass
    
    def massCurCarrying(self):
        mass = 0.0
        for item in self.invtry:
            if(item.isContainer):
                for subItem in item.storedItems:
                    mass += subItem.kgs
            mass += item.kgs
        return mass
     
    def calcActDelay(self, act):
        delay = 0.0
        if(act == 'step'):
            mass = self.massCurCarrying()
            delay = mass*0.02 - 0.00004*self.cdims['precisão']*(mass**2) + 0.1/(self.cdims['agilidade']+1) + 0.3
            return delay
        
        elif(act == 'roll'):
            mass = self.massCurCarrying()
            delay = 0.2/(self.cdims['precisão']+1)*mass - 0.000004*(self.cdims['precisão']**2)*(mass**2) + 1/(self.cdims['agilidade']**2+1) + 1.3
            return delay
        
        elif(act == 'jump'):
            mass = self.massCurCarrying()
            delay = 0.02*mass - 0.000004*(self.cdims['precisão']**2)*(mass**2) + 0.1/(self.cdims['agilidade']+1) + 0.8
            return delay
        
        elif(act == 'strike'):
            if(self.wpn is None):
                mass = 0.2
            else:
                mass = self.wpn.kgs
            delay = exp(-1*self.cdims['agilidade']/mass) + 0.1*mass/(self.cdims['ímpeto']+1) + 1/sqrt(self.cdims['agilidade']*self.cdims['ímpeto']+1)
            return delay
        
        elif(act == 'interact'):
            print("Well, it's complicated. What are you interacting with?")
            return delay
        
        elif(act == 'block'):
            return delay
        
        else:
            print(f'Action {act} not recognized.')
            return delay
        
    def calcDmg(self, enemy, tgt):
        pass
    
    def wearItem(self, item):
        pass
    
    def takeBloodHit(self, dmg, tgt):
        self.blood -= dmg
    
    def eatFood(self, food):
        pass
    
    def printState(self):
        ret = ''
        ret += 'blood ' + str(self.blood) + '\n'
        ret += 'bloodLoss ' + str(self.bloodLoss) + '\n'
        ret += 'pneuma ' + str(self.pneuma) + '\n'
        ret += 'pdr ' + str(self.pdr) + '\n'
        ret += 'stamina ' + str(self.stamina) + '\n'
        ret += 'tiredLvl ' + str(self.tiredLvl) + '\n'
        ret += 'hungerPts ' + str(self.hungerPts) + '\n'
        return ret

    def addHunger(self):
        self.hungerPts += 1
    
    def goToSleep(self):
        self.sleeping = True
        self.pdr += 3
        self.pdr -= self.hungerPts

    def wakeUp(self):
        self.sleeping = False
        self.pneuma += self.pdr



class Time:
    def __init__(self, tm:int=0):
        self.tm = tm
        self._update()

    def _update(self):
        self.min = self.tm % 60
        self.h = self.tm // 60 % 24
        self.d = self.tm // 1440 % 30
        self.mon = self.tm // 43200 % 12
        self.y = self.tm // 518400

    def advance_min(self, m):
        self.tm += m
        self._update()

    def get_ftimestr(self) -> str:
        wkDay = ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado']
        return f'{wkDay[self.d%7]} {self.d}/{self.mon}/{self.y} {self.h}:{self.min}'

class Game:
    def __init__(self, save_path=None, players=None, game_time=0) -> None:
        self.save_path = save_path
        self.players = players
        self.time = Time(game_time)
        self.state = 1

    def adv_hours(self, h):
        self.time.advance(h*60)

    def hunger(self):
        if self.time.h == 12:
            for player in self.players:
                player.addHunger()
        elif self.time.h == 18:
            for player in self.players:
                player.addHunger()
        elif self.time.h == 0:
            for player in self.players:
                player.addHunger()


class GUI:
    def __init__(self, game: Game) -> None:
        self.root = tk.Tk()
        self.root.title(refs.win_name)
        self.root.resizable(False, False)

        self.game = game


    def dark_mode(self):
        ''' Return a dark style to the window'''
        
        self.style = ttk.Style(self.root)
        self.root.tk.call('source', './Azure/azure.tcl')
        self.root.tk.call("set_theme", "dark")

    def begin(self):
        self.root.mainloop()

    def _t_callback(self, event):
        self.label.config(text="Advance time.")

    def _q_callback(self, event):
        self.label.config(text="Q clicked")

    def _esc_callback(self, event):
        self.entry.delete(0, 'end')

    def bind_keys(self):
        self.root.bind("<Key-t>", self._t_callback)
        self.root.bind("<Key-Escape>", self._esc_callback)

    def draw_screen(self):
        self.root.geometry(str(refs.org_width) + "x" + str(refs.org_height))
        self.label = tk.Label(self.root, text="0")
        self.label.pack(padx=10, pady=10)

        self.entry = tk.Entry(self.root)
        self.entry.bind("<Key-q>", self._q_callback)
        self.entry.pack()

    