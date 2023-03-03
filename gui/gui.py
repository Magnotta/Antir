# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 16:31:15 2022

@author: ndd2
"""

from math import exp, sqrt
from classes.game import Game
from .cmd_parser import Parser


import tkinter as tk
import tkinter.messagebox as messageBox
import tkinter.ttk as ttk
import tkinter.scrolledtext as st

import refs


class GUI:
    def __init__(self, game_instance: Game) -> None:
        self.container = tk.Tk()
        self.parser = Parser(game_instance)
        self.undo = None
        self.quit = False
        self.cmd_trigger: bool = False
        self.player_ids = [p.id for p in game_instance.players]
        

##### FRAMES IN THE MAIN WINDOW #####

        self.logs_frame = ttk.Labelframe(self.container, text="resposta", height=200, width=600)
        self.main_frame = tk.Frame(self.container)
        self.placedatetime_frame = tk.Frame(self.container)

##### WIDGETS IN THE LOGS FRAME #####



##### WIDGETS IN THE MAIN FRAME #####

        self.info_lframe = ttk.Labelframe(self.main_frame, text="info adicional")
        self.info = tk.Label(self.info_lframe, text="nada aqui", anchor="center")
        self.description_lframe = ttk.Labelframe(self.main_frame, text="descrição")
        self.description = st.ScrolledText(self.description_lframe, width=36, height=12)
        self.cmdbrowser = tk.Label(self.main_frame, text="Digite um comando", anchor="s")
        self.playerinfo_lframe = ttk.Labelframe(self.main_frame, text="jogadores")
        self.cmd_line = tk.Entry(self.main_frame)

##### VARIABLES IN THE PLAYERINFO TABLE #####

        self.table_name = tk.Label(self.playerinfo_lframe, text="Nome", font=("Arial", 10))
        self.table_blood = tk.Label(self.playerinfo_lframe, text="Sangue", font=("Arial", 10))
        self.table_pneuma = tk.Label(self.playerinfo_lframe, text="Pneuma", font=("Arial", 10))
        self.table_hunger = tk.Label(self.playerinfo_lframe, text="Fome", font=("Arial", 10))
        self.table_stamina = tk.Label(self.playerinfo_lframe, text="Stm", font=("Arial", 10))

        self.table_columns = ['name', 'blood', 'pneuma', 'hunger', 'stamina']
        for player in game_instance.players:
            for col in self.table_columns:
                setattr(self, f'p{player.id}{col}', tk.Label(self.playerinfo_lframe))
            
##### WIDGETS IN THE PLACEDATETIME FRAME #####

        self.place_lframe = ttk.Labelframe(self.placedatetime_frame, text="local")
        self.place = tk.Label(self.place_lframe, text="lugar nenhum mas pqp esse lixo é chatão", anchor="center")
        self.datetime_lframe = ttk.Labelframe(self.placedatetime_frame, text="data e horário")
        self.datetime = tk.Label(self.datetime_lframe, text="zero hora", anchor="center")

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

        for p in g.players:
            for col in self.table_columns:
                getattr(self, f'p{p.id}{col}').config(text=str(getattr(p, col)))
    
        self.place.config(text=g.location)

        self.container.update_idletasks()
        self.container.update()



    def read_input(self):
        if cmd:=self.cmd_line.get():
            self.parser.parse(cmd)



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
        if self.parser.command_is_complete:
            self.cmd_trigger = True
            self.cmd_line.delete(0, 'end')



    def bind_keys(self):
        self.container.bind("<Key-Escape>", self._esc_callback)
        self.container.bind("<Control-z>", self._undo_callback)
        self.container.bind("<KeyPress-Return>", self.enter_callback)



    def draw_screen(self): 
        self.logs_frame.grid(row=0)
        self.main_frame.grid(row=1)
        self.placedatetime_frame.grid(row=2)

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
        self.table_pneuma.grid(row=0, column=2)
        self.table_hunger.grid(row=0, column=3)
        self.table_stamina.grid(row=0, column=4)

        for player_id in self.player_ids:
            for col_no, col in enumerate(self.table_columns):
                getattr(self, f'p{player_id}{col}').grid(row=player_id+1, column=col_no)
        
        self.place_lframe.grid(column=0, row=0, columnspan=5)
        self.datetime_lframe.grid(column=5, row=0, columnspan=2)
        self.place.pack()
        self.datetime.pack()
