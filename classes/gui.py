# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 16:31:15 2022

@author: ndd2
"""

from math import exp, sqrt
from .game import Game
from .parser import Parser

import tkinter as tk
import tkinter.messagebox as messageBox
import tkinter.ttk as ttk
import tkinter.scrolledtext as st

import refs


class GUI:
    def __init__(self) -> None:
        self.container = tk.Tk()
        self.undo = None
        self.quit = False
        self.command = ''
        self.runCommand = False

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



    def configure(self, context: Game):
        self.container.title(refs.win_name)
        #self.container.geometry(str(refs.win_width) + "x" + str(refs.win_height))
        self.container.resizable(False, False)

        self.container.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.dark_mode()

        self.bind_keys()

        self.datetime.config(text=str(context.time))




    def on_closing(self):
        if messageBox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.container.destroy()
        self.quit = True



    def begin(self, game):
        self.configure(game)
        self.draw_screen()

    

    def update_widgets(self, g: Game):
        self.datetime.config(text=str(g.time))

        self.container.update_idletasks()
        self.container.update()



    def reply(self, ans):
        self.description.config(state=tk.NORMAL)
        self.description.delete("1.0", tk.END)

        self.description.insert("1.0", ans.description)



    def _esc_callback(self, event):
        self.undo = self.cmd_line.get()
        self.cmd_line.delete(0, 'end')
        self.cmd_line.focus()



    def _undo_callback(self, event):
        if self.undo:
            self.cmd_line.insert(0, self.undo)



    def enter_callback(self, event):
        self.runCommand = True

            

    def keypress_callback(self, event):
        self.command = self.cmd_line.get()



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