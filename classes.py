# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 16:31:15 2022

@author: ndd2
"""

from math import exp, sqrt
from uuid import uuid1, UUID
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as st

import refs

class Entity:
    def __init__(self, id=None):
        if(id is None):
            self.id = UUID(uuid1().hex)
        else:
            self.id = UUID(id)
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, type(self)):
            return self.id == __o.id

        return False



class Item(Entity):
    def __init__(self, name, qty=1, isContainer=False):
        super().__init__()
        self.drblt: int = 100
        self.kgs: float = 0.0
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
        
        elif(act == 'roll'):
            mass = self.massCurCarrying()
            delay = 0.2/(self.cdims['precisão']+1)*mass - 0.000004*(self.cdims['precisão']**2)*(mass**2) + 1/(self.cdims['agilidade']**2+1) + 1.3
        
        elif(act == 'jump'):
            mass = self.massCurCarrying()
            delay = 0.02*mass - 0.000004*(self.cdims['precisão']**2)*(mass**2) + 0.1/(self.cdims['agilidade']+1) + 0.8
        
        elif(act == 'strike'):
            if(self.wpn is None):
                mass = 0.2
            else:
                mass = self.wpn.kgs
            delay = exp(-1*self.cdims['agilidade']/mass) + 0.1*mass/(self.cdims['ímpeto']+1) + 1/sqrt(self.cdims['agilidade']*self.cdims['ímpeto']+1)
        
        elif(act == 'interact'):
            print("Well, it's complicated. What are you interacting with?")
        
        elif(act == 'block'):
            pass

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
    def __init__(self, tm = (0, 0, 0)) -> None:
        self.d = tm[0]
        self.h = tm[1]
        self.m = tm[2]
        self.mins = self.d*1440 + self.h*60 + self.m

    def __add__(self, __o):
        if isinstance(__o, Time):
            __r =  (self.d + __o.d, self.h + __o.h, self.m + __o.m)
        elif isinstance(__o, tuple):
            __r = (self.d + __o[0], self.h + __o[1], self.m + __o[2])
        else:
            raise TypeError(f"unsupported operand types for +: {type(self)} and {type(__o)}")

        if __r[2] >= 60:
            __r = (__r[0], __r[1] + (__r[2]//60), __r[2] % 60)
        if __r[1] >= 24:
            __r = (__r[0] + (__r[1]//24), __r[1] % 24, __r[2])
            
        return Time(__r)

    def __repr__(self) -> str:
        return f"{self.d}, {self.h}:{self.m}"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, type(self)):
            return self.mins == __o.mins
        elif isinstance(__o, tuple):
            return self.time == __o
        return False


class Game:
    def __init__(self, save_path=None, players=None, game_time=(0,0,0)) -> None:
        self.save_path = save_path
        self.players = players
        self.time = Time(game_time)
        self.state = 1

    def advance(self, adv: tuple):
        old_time = self.time
        new_time = old_time + adv

        if new_time.d != old_time.d:
            # day change, update PDR, third hungerpt
            pass
        if new_time.h != old_time.h:
            # hour change, update hunger
            pass
        if new_time.m != old_time.m:
            # minute change, update bloodloss, stamina
            pass


class GUI:
    def __init__(self, game: Game) -> None:
        self.container = tk.Tk()
        self.game = game
        self.parser = Parser()
        self.undo = None

##### FRAMES IN THE MAIN WINDOW #####

        self.logs_frame = ttk.Labelframe(self.container, text="resposta", height=200, width=600)
        self.main_frame = tk.Frame(self.container)
        self.placedatetime_frame = tk.Frame(self.container)

##### END FRAMES IN THE MAIN WINDOW #####
#####
##### WIDGETS IN THE LOGS FRAME #####



##### END WIDGETS IN THE LOGS FRAME #####
#####
##### WIDGETS IN THE MAIN FRAME #####

        self.info_lframe = ttk.Labelframe(self.main_frame, text="info adicional")
        self.info = tk.Label(self.info_lframe, text="nada aqui", anchor="center")
        self.description_lframe = ttk.Labelframe(self.main_frame, text="descrição")
        self.description = st.ScrolledText(self.description_lframe, width=36, height=12)
        self.cmdbrowser = tk.Label(self.main_frame, text="Digite um comando", anchor="s")
        self.playerinfo_lframe = ttk.Labelframe(self.main_frame, text="jogadores")
        self.cmd_line = tk.Entry(self.main_frame)

##### END WIDGETS IN THE MAIN FRAME #####
#####
##### VARIABLES IN THE PLAYERINFO TABLE #####

        self.table_name = tk.Label(self.playerinfo_lframe, text="Nome", font=("Arial", 10))
        self.table_blood = tk.Label(self.playerinfo_lframe, text="Sangue", font=("Arial", 10))
        self.table_bloodloss = tk.Label(self.playerinfo_lframe, text="PDS", font=("Arial", 10))
        self.table_pneuma = tk.Label(self.playerinfo_lframe, text="Pneuma", font=("Arial", 10))
        self.table_pdr = tk.Label(self.playerinfo_lframe, text="PDR", font=("Arial", 10))
        self.table_hunger = tk.Label(self.playerinfo_lframe, text="Fome", font=("Arial", 10))
        self.table_stamina = tk.Label(self.playerinfo_lframe, text="Stm", font=("Arial", 10))
        self.table_tiredLvl = tk.Label(self.playerinfo_lframe, text="Cans", font=("Arial", 10))

        self.p1_name = tk.Label(self.playerinfo_lframe, text="joao")
        self.p1_blood = tk.Label(self.playerinfo_lframe, text="100")
        self.p1_bloodloss = tk.Label(self.playerinfo_lframe, text="0")
        self.p1_pneuma = tk.Label(self.playerinfo_lframe, text="100")
        self.p1_pdr = tk.Label(self.playerinfo_lframe, text="3")
        self.p1_hunger = tk.Label(self.playerinfo_lframe, text="0")
        self.p1_stamina = tk.Label(self.playerinfo_lframe, text="100")
        self.p1_tiredLvl = tk.Label(self.playerinfo_lframe, text="0")

        self.p2_name = tk.Label(self.playerinfo_lframe, text="joao")
        self.p2_blood = tk.Label(self.playerinfo_lframe, text="100")
        self.p2_bloodloss = tk.Label(self.playerinfo_lframe, text="0")
        self.p2_pneuma = tk.Label(self.playerinfo_lframe, text="100")
        self.p2_pdr = tk.Label(self.playerinfo_lframe, text="3")
        self.p2_hunger = tk.Label(self.playerinfo_lframe, text="0")
        self.p2_stamina = tk.Label(self.playerinfo_lframe, text="100")
        self.p2_tiredLvl = tk.Label(self.playerinfo_lframe, text="0")

        self.p3_name = tk.Label(self.playerinfo_lframe, text="joao")
        self.p3_blood = tk.Label(self.playerinfo_lframe, text="100")
        self.p3_bloodloss = tk.Label(self.playerinfo_lframe, text="0")
        self.p3_pneuma = tk.Label(self.playerinfo_lframe, text="100")
        self.p3_pdr = tk.Label(self.playerinfo_lframe, text="3")
        self.p3_hunger = tk.Label(self.playerinfo_lframe, text="0")
        self.p3_stamina = tk.Label(self.playerinfo_lframe, text="100")
        self.p3_tiredLvl = tk.Label(self.playerinfo_lframe, text="0")

        self.p4_name = tk.Label(self.playerinfo_lframe, text="joao")
        self.p4_blood = tk.Label(self.playerinfo_lframe, text="100")
        self.p4_bloodloss = tk.Label(self.playerinfo_lframe, text="0")
        self.p4_pneuma = tk.Label(self.playerinfo_lframe, text="100")
        self.p4_pdr = tk.Label(self.playerinfo_lframe, text="3")
        self.p4_hunger = tk.Label(self.playerinfo_lframe, text="0")
        self.p4_stamina = tk.Label(self.playerinfo_lframe, text="100")
        self.p4_tiredLvl = tk.Label(self.playerinfo_lframe, text="0")

        self.p5_name = tk.Label(self.playerinfo_lframe, text="joao")
        self.p5_blood = tk.Label(self.playerinfo_lframe, text="100")
        self.p5_bloodloss = tk.Label(self.playerinfo_lframe, text="0")
        self.p5_pneuma = tk.Label(self.playerinfo_lframe, text="100")
        self.p5_pdr = tk.Label(self.playerinfo_lframe, text="3")
        self.p5_hunger = tk.Label(self.playerinfo_lframe, text="0")
        self.p5_stamina = tk.Label(self.playerinfo_lframe, text="100")
        self.p5_tiredLvl = tk.Label(self.playerinfo_lframe, text="0")

        self.p6_name = tk.Label(self.playerinfo_lframe, text="joao")
        self.p6_blood = tk.Label(self.playerinfo_lframe, text="100")
        self.p6_bloodloss = tk.Label(self.playerinfo_lframe, text="0")
        self.p6_pneuma = tk.Label(self.playerinfo_lframe, text="100")
        self.p6_pdr = tk.Label(self.playerinfo_lframe, text="3")
        self.p6_hunger = tk.Label(self.playerinfo_lframe, text="0")
        self.p6_stamina = tk.Label(self.playerinfo_lframe, text="100")
        self.p6_tiredLvl = tk.Label(self.playerinfo_lframe, text="0")

##### END VARIABLES IN THE PLAYERINFO TABLE #####
#####
##### WIDGETS IN THE PLACEDATETIME FRAME #####

        self.place_lframe = ttk.Labelframe(self.placedatetime_frame, text="local")
        self.place = tk.Label(self.place_lframe, text="lugar nenhum mas pqp esse lixo é chatão", anchor="center")
        self.datetime_lframe = ttk.Labelframe(self.placedatetime_frame, text="data e horário")
        self.datetime = tk.Label(self.datetime_lframe, text="zero hora", anchor="center")

##### END WIDGETS IN THE PLACEDATETIME FRAME #####


    def dark_mode(self):
        ''' Return a dark style to the window'''
        
        self.style = ttk.Style(self.container)
        self.container.tk.call('source', './Azure/azure.tcl')
        self.container.tk.call("set_theme", "dark")



    def configure(self):
        self.container.title(refs.win_name)
        #self.container.geometry(str(refs.win_width) + "x" + str(refs.win_height))
        self.container.resizable(False, False)

        self.dark_mode()

        self.bind_keys()



    def begin(self):
        self.configure()
        self.draw_screen()

        self.container.mainloop()



    def _esc_callback(self, event):
        self.undo = self.cmd_line.get()
        self.cmd_line.delete(0, 'end')
        self.cmd_line.focus()



    def _undo_callback(self, event):
        if self.undo:
            self.cmd_line.insert(0, self.undo)

    def enter_callback(self, event):
        print("Enter detected")
        if self.valid_cmd and self.complete_cmd:
            cmd_words = []
            cmd_nums = []
            for char in self.cmd_line.get():
                if char.isdigit():
                    cmd_nums.append(char)
                else:
                    cmd_words.append(char)
            print(cmd_words)
            print(cmd_nums)
            

    def keypress_callback(self, event):
        if cmd := self.cmd_line.get():
            self.parser.parse(cmd)

        self.description.config(state=tk.NORMAL)
        self.description.delete("1.0", tk.END)

        self.description.insert("1.0", self.parser.description)



    def bind_keys(self):
        self.container.bind("<Key-Escape>", self._esc_callback)
        self.container.bind("<Control-z>", self._undo_callback)
        self.container.bind("<Key>", self.keypress_callback)
        self.container.bind("<KeyPress-Return>", self.enter_callback)



    def draw_screen(self): 
##### MAIN WINDOW FRAMES #####

        self.logs_frame.grid(row=0)
        self.main_frame.grid(row=1)
        self.placedatetime_frame.grid(row=2)

##### END MAIN WINDOW FRAMES #####
#####
##### LOGS FRAME WINDGETS #####



##### END LOGS FRAME WINDGETS #####
#####
##### MAIN FRAME WIDGETS #####

        self.cmd_line.grid(row=1, column=1)
        self.info_lframe.grid(row=0, rowspan=3, column=0)
        self.info.pack()
        self.description_lframe.grid(row=2, column=1)
        self.description.pack()
        self.description.insert("1.0", "Bem-vindo ao Antir, seu otário!")
        self.description.config(state=tk.DISABLED)
        self.cmdbrowser.grid(row=0, column=1)
        self.playerinfo_lframe.grid(row=0, rowspan=3, column=2)

        self.table_name.grid(row=0, column=0)
        self.table_blood.grid(row=0, column=1)
        self.table_bloodloss.grid(row=0, column=2)
        self.table_pneuma.grid(row=0, column=3)
        self.table_pdr.grid(row=0, column=4)
        self.table_hunger.grid(row=0, column=5)
        self.table_stamina.grid(row=0, column=6)
        self.table_tiredLvl.grid(row=0, column=7)

        self.p1_name.grid(row=1, column=0)
        self.p1_blood.grid(row=1, column=1)
        self.p1_bloodloss.grid(row=1, column=2)
        self.p1_pneuma.grid(row=1, column=3)
        self.p1_pdr.grid(row=1, column=4)
        self.p1_hunger.grid(row=1, column=5)
        self.p1_stamina.grid(row=1, column=6)
        self.p1_tiredLvl.grid(row=1, column=7)

        self.p2_name.grid(row=2, column=0)
        self.p2_blood.grid(row=2, column=1)
        self.p2_bloodloss.grid(row=2, column=2)
        self.p2_pneuma.grid(row=2, column=3)
        self.p2_pdr.grid(row=2, column=4)
        self.p2_hunger.grid(row=2, column=5)
        self.p2_stamina.grid(row=2, column=6)
        self.p2_tiredLvl.grid(row=2, column=7)

        self.p3_name.grid(row=3, column=0)
        self.p3_blood.grid(row=3, column=1)
        self.p3_bloodloss.grid(row=3, column=2)
        self.p3_pneuma.grid(row=3, column=3)
        self.p3_pdr.grid(row=3, column=4)
        self.p3_hunger.grid(row=3, column=5)
        self.p3_stamina.grid(row=3, column=6)
        self.p3_tiredLvl.grid(row=3, column=7)

        self.p4_name.grid(row=4, column=0)
        self.p4_blood.grid(row=4, column=1)
        self.p4_bloodloss.grid(row=4, column=2)
        self.p4_pneuma.grid(row=4, column=3)
        self.p4_pdr.grid(row=4, column=4)
        self.p4_hunger.grid(row=4, column=5)
        self.p4_stamina.grid(row=4, column=6)
        self.p4_tiredLvl.grid(row=4, column=7)

        self.p5_name.grid(row=5, column=0)
        self.p5_blood.grid(row=5, column=1)
        self.p5_bloodloss.grid(row=5, column=2)
        self.p5_pneuma.grid(row=5, column=3)
        self.p5_pdr.grid(row=5, column=4)
        self.p5_hunger.grid(row=5, column=5)
        self.p5_stamina.grid(row=5, column=6)
        self.p5_tiredLvl.grid(row=5, column=7)

        self.p6_name.grid(row=6, column=0)
        self.p6_blood.grid(row=6, column=1)
        self.p6_bloodloss.grid(row=6, column=2)
        self.p6_pneuma.grid(row=6, column=3)
        self.p6_pdr.grid(row=6, column=4)
        self.p6_hunger.grid(row=6, column=5)
        self.p6_stamina.grid(row=6, column=6)
        self.p6_tiredLvl.grid(row=6, column=7)

##### END MAIN FRAME WIDGETS #####
#####
##### PLACEDATETIME FRAME WIDGETS #####
        
        self.place_lframe.grid(column=0, row=0, columnspan=5)
        self.datetime_lframe.grid(column=5, row=0, columnspan=2)
        self.place.pack()
        self.datetime.pack()

##### END PLACEDATETIME FRAME WIDGETS #####

##### string parser pros comandos #####

class Parser:
    def __init__(self) -> None:
        self.description = ""
        self.ans = ""

    def parse(self, chars: str):
        cmd = chars.lower()
        depth = len(cmd)

        if cmd[0] == 't':
            self.description = "Menu de tempo"
        elif cmd[0] == 'p':
            self.description = "Menu de personagem"
        elif cmd[0] == 'k':
            self.description = "Menu de combate"
        elif cmd[0] == 'e':
            self.description = "Menu de cena"
        elif cmd[0] == 'l':
            self.description = "Menu de local"

        if depth == 1:
            return

        