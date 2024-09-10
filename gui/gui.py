# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 16:31:15 2022

@author: ndd2
"""

from math import exp, sqrt
from classes.game import Game, Parser


import tkinter as tk
import tkinter.messagebox as messageBox
import tkinter.ttk as ttk
import tkinter.scrolledtext as st
import sqlite3 as sql

window_name = "Antir Pre Alpha"

class GUI_BASE:
    def __init__(self) -> None:
        self.container = tk.Tk()
        self.quit = False
        self.style = ttk.Style(self.container)
        self.container.tk.call('source', './Azure/azure.tcl')
        self.container.tk.call("set_theme", "dark")

        self.container.title(window_name)
        self.container.resizable(False, False)
        self.container.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self, event):
        self.quit = True
        self.container.destroy()



class MAIN_PAGE(GUI_BASE):
    def __init__(self, game_instance: Game) -> None:
        super().__init__()
        self.container.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.game = game_instance

        self.cmd_trigger: bool = False
        self.player_ids = [p.id for p in game_instance.players]

        self.container.bind("<KeyPress-Return>", self.enter_callback)
        self.container.bind("<Key-Escape>", self.esc_callback)

        # For navigating through player pages
        self.container.bind("<Control-p>", self.bind_player_menu)
        self.player_select = 0

        # For opening item page
        self.container.bind("<Control-i>", ITEM_PAGE)

##### FRAMES IN THE MAIN WINDOW #####

        self.logs_frame = ttk.Labelframe(self.container, text="resposta", height=200, width=600)
        self.main_frame = tk.Frame(self.container)
        self.placedatetime_frame = tk.Frame(self.container)

##### WIDGETS IN THE LOGS FRAME #####

        self.reply_box = st.ScrolledText(self.logs_frame, width=110, height=15)

##### WIDGETS IN THE MAIN FRAME #####

        self.info_lframe = ttk.Labelframe(self.main_frame, text="info adicional")
        self.info = tk.Label(self.info_lframe, text="nada aqui", anchor="center")
        self.description_lframe = ttk.Labelframe(self.main_frame, text="descrição")
        self.description = st.ScrolledText(self.description_lframe, width=36, height=12)
        self.cmdbrowser_label = tk.Label(self.main_frame, text="Digite um comando", anchor="center")
        self.playerinfo_lframe = ttk.Labelframe(self.main_frame, text="jogadores")
        self.cmd_line = tk.Entry(self.main_frame)

##### VARIABLES IN THE PLAYERINFO TABLE #####

        self.table_name_label = tk.Label(self.playerinfo_lframe, text="Nome", font=("Arial", 10))
        self.table_blood_label = tk.Label(self.playerinfo_lframe, text="Sangue", font=("Arial", 10))
        self.table_pneuma_label = tk.Label(self.playerinfo_lframe, text="Pneuma", font=("Arial", 10))
        self.table_hunger_label = tk.Label(self.playerinfo_lframe, text="Fome", font=("Arial", 10))
        self.table_stamina_label = tk.Label(self.playerinfo_lframe, text="Stm", font=("Arial", 10))

        self.table_columns = ['name', 'blood', 'pneuma', 'hunger', 'stamina']
        for player in game_instance.players:
            for col in self.table_columns:
                setattr(self, f'p{player.id}{col}', tk.Label(self.playerinfo_lframe))
            
##### WIDGETS IN THE PLACEDATETIME FRAME #####

        self.place_lframe = ttk.Labelframe(self.placedatetime_frame, text="local")
        self.place = tk.Label(self.place_lframe, text="lugar nenhum mas pqp esse lixo é chatão", anchor="center")
        self.datetime_lframe = ttk.Labelframe(self.placedatetime_frame, text="data e horário")
        self.datetime = tk.Label(self.datetime_lframe, text="zera hora", anchor="center")

    def on_closing(self):
        if messageBox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.container.destroy()
            self.quit = True

    def enter_callback(self, event):
        res = self.game.parser.parse(self.cmd_line.get())
        self.cmd_line.delete(0, 'end')
        if res != None:
            self.game.execute(*res)

    def esc_callback(self, event):
        self.undo = self.cmd_line.get()
        self.cmd_line.delete(0, 'end')
        self.cmd_line.focus()

    def bind_player_menu(self, event):
        self.reply("Ctrl-P apertado. Aguardando jogador...")
        self.container.bind("<KeyPress>", self.unbind_player_menu)

    def unbind_player_menu(self, event):
        self.container.unbind("<KeyPress>")

        try:
            self.player_select = int(event.char)
            if(self.player_select > 5 or self.player_select < 1):
                raise ValueError
        except ValueError:
            self.reply("Comando cancelado. Por favor, digite um número de 1 a 5.")
        else:
            self.reply(f"Abrindo tela do jogador {self.player_select}")

    def draw_screen(self): 
        self.logs_frame.grid(row=0)
        self.main_frame.grid(row=1)
        self.placedatetime_frame.grid(row=2)

        self.reply_box.pack()
        self.reply_box.configure(state=tk.DISABLED)

        self.cmd_line.grid(row=1, column=1)
        self.info_lframe.grid(row=0, rowspan=3, column=0)
        self.info.pack()
        self.description_lframe.grid(row=2, column=1)
        self.description.pack()
        self.description.insert("1.0", "Bem-vindo ao Antir, seu otário!")
        self.description.config(state=tk.DISABLED)
        self.cmdbrowser_label.grid(row=0, column=1)
        self.playerinfo_lframe.grid(row=0, rowspan=3, column=2)

        self.table_name_label.grid(row=0, column=0)
        self.table_blood_label.grid(row=0, column=1)
        self.table_pneuma_label.grid(row=0, column=2)
        self.table_hunger_label.grid(row=0, column=3)
        self.table_stamina_label.grid(row=0, column=4)

        for player_id in self.player_ids:
            for col_no, col in enumerate(self.table_columns):
                getattr(self, f'p{player_id}{col}').grid(row=player_id+1, column=col_no)
        
        self.place_lframe.grid(column=0, row=0, columnspan=5)
        self.datetime_lframe.grid(column=5, row=0, columnspan=2)
        self.place.pack()
        self.datetime.pack()

    def configure(self, context:Game):
        self.datetime.config(text=str(context.time))

    def begin(self, game):
        self.configure(game)
        self.draw_screen()

    def read_input(self):
        if cmd:=self.cmd_line.get():
            self.game.parser.parse(cmd)
            self.reply(self.game.parser.ans)

    def reply(self, text):
        self.description.configure(state=tk.NORMAL)
        self.description.delete(0.0, tk.END)
        self.description.insert(tk.END, text + '\n')
        self.description.configure(state=tk.DISABLED)

    def update_widgets(self, g: Game):
        self.datetime.config(text=str(g.time))

        for p in g.players:
            for col in self.table_columns:
                getattr(self, f'p{p.id}{col}').config(text=str(getattr(p, col)))
    
        self.place.config(text=g.location)

        self.container.update_idletasks()
        self.container.update()





class PLAYER_PAGE(GUI_BASE):
    def __init__(self) -> None:
        super().__init__()

        self.player_ids = []

class ITEM_PAGE(tk.Toplevel):
    def __init__(self, event) -> None:
        super().__init__()

        self.new_item_frame = ttk.Labelframe(self, text="Item Novo")
        self.item_search_frame = ttk.Labelframe(self, text="Buscar Item")

        self.new_item_name_entry = tk.Entry(self.new_item_frame)
        self.new_item_name_label = tk.Label(self.new_item_frame, text="Nome do item")
        self.new_item_params_entry = tk.Entry(self.new_item_frame)
        self.new_item_params_label = tk.Label(self.new_item_frame, text="Parâmetros")
        self.new_item_tags_entry = tk.Entry(self.new_item_frame)
        self.new_item_tags_label = tk.Label(self.new_item_frame, text="Tags")
        self.add_new_item_button = tk.Button(self.new_item_frame, text="Adicionar", command=self.add_item)

        self.bind("<Key-Escape>", self.close)

        self.new_item_frame.pack()
        self.item_search_frame.pack()

        self.new_item_name_label.grid(row=0, column=0)
        self.new_item_params_label.grid(row=0, column=1)
        self.new_item_tags_label.grid(row=0, column=2)

        self.new_item_name_entry.grid(row=1, column=0)
        self.new_item_params_entry.grid(row=1, column=1)
        self.new_item_tags_entry.grid(row=1, column=2)

        self.new_item_name_entry.focus()

        self.grab_set()

    def add_item(self):
        pass

    def close(self, event):
        self.destroy()