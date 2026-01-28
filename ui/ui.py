# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 16:31:15 2022

@author: ndd2
"""

from math import exp, sqrt
from classes.game import Game


from tkinter import Tk, Frame, Label, Entry, Text, Button, DISABLED, NORMAL, END
from tkinter.messagebox import askokcancel
from tkinter.ttk import Style, Labelframe, Treeview, Scrollbar, Notebook
import tkinter.ttk as ttk
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText

from db.models import Item_Mold

from sqlalchemy import select

window_name = "Antir Pre Alpha"

class Parser:
    def __init__(self, g: Game) -> None:
        self.ans = ''

        self.command_is_recognized: bool = False
        self.command_is_complete: bool = False

        """
        {'callable': ,
                                'handle': '',
                                'arg_types_list': []}
        """

        self.time_dict = {'m': {'callable':g.cmd_advance_minutes,
                                'handle':'Avançar Minutos',
                                'arg_types_list':['int']}}
        self.env_dict = {}
        self.player_dict = {'h': {'callable': g.cmd_hunger,
                                'handle': 'Esfoemar',
                                'arg_types_list': ['int']},
                            'b': {'callable': g.cmd_blood,
                                'handle': 'Dessangrar',
                                'arg_types_list': ['int']},
                            'p': {'callable': g.cmd_pdr,
                                'handle': 'Murchar',
                                'arg_types_list': ['int']},
                            's': {'callable': g.cmd_stamina,
                                'handle': 'Fatigar',
                                'arg_types_list': ['int']},
                            'sle': {'callable': g.cmd_sleep,
                                'handle': 'Botar pra dormir',
                                'arg_types_list': []}}
        self.location_dict = {'g': {'callable': g.cmd_move_scene_to,
                                'handle': 'Mover',
                                'arg_types_list': ['str']}}

        self.base_dict = {'t': {'func_dict': self.time_dict,
                                'target_type': 'Tempo'},
                        'p': {'func_dict': self.player_dict,
                              'target_type': 'Player'},
                        'e': {'func_dict': self.env_dict,
                              'target_type': 'Ambiente'},
                        'l': {'func_dict': self.location_dict,
                              'target_type': 'Local'}}
        
    def parse(self, chars: str):
        if not chars:
            self.ans = ""
            return None # no input

        self.tokens = list(filter(None, chars.split(' ')))

        cmd_key = self.tokens[0]

        if cmd_key[0] not in self.base_dict:
            self.ans = f"Primeiro char errado. Opções:\n{' '.join(self.base_dict.keys())}"
            return None # wrong first character
        
        if len(cmd_key) < 2:
            self.ans = f"Comandos de {self.base_dict[cmd_key[0]]['target_type']}:\n{' '.join(self.base_dict[cmd_key[0]]['func_dict'].keys())}"
            return None # command keyword incomplete
        
        try:
            func_dict = self.base_dict[cmd_key[0]]['func_dict'][cmd_key[1:]]
        except KeyError:
            self.ans = f"Comando errado. Opções de {self.base_dict[cmd_key[0]]['target_type']}:\n{' '.join(self.base_dict[cmd_key[0]]['func_dict'].keys())}"
            return None # wrong second character

        if len(self.tokens) < 2:
            return None

        cmd_target_list = self.read_target(self.base_dict[cmd_key[0]]['target_type'], self.tokens[1])
        args_list = []

        if self.base_dict[cmd_key[0]]['target_type'] == 'Tempo':
            if len(self.tokens) < len(func_dict['arg_types_list']) + 1:
                self.ans = f"Argumentos de {func_dict['handle']}: {' '.join(func_dict['arg_types_list'])}"
                return None
            
            for idx, token in enumerate(self.tokens[1:]):
                args_list.append(getattr(self,
                                         f"read_arg_{func_dict['arg_types_list'][idx]}")(token))
        else:
            if len(self.tokens) < len(func_dict['arg_types_list']) + 2:
                self.ans = f"Argumentos de {func_dict['handle']}: alvos {' '.join(func_dict['arg_types_list'])}"
                return None
            
            for idx, token in enumerate(self.tokens[2:]):
                args_list.append(getattr(self, f"read_arg_{func_dict['arg_types_list'][idx]}")(token))

        if len(func_dict['arg_types_list']) == len(args_list):
            self.ans = "Comando Completo."
        
        return [self.base_dict[cmd_key[0]]['target_type'], func_dict['callable'], cmd_target_list, args_list]

    def read_target(self, cmd_target_type, token):
        cmd_target_list = []
        if cmd_target_type == "Player":
            if token == '*':
                [cmd_target_list.append(x) for x in range(6)]
            else:
                for char in token:
                    if char in ['0', '1', '2', '3', '4', '5']:
                        cmd_target_list.append(int(char))
                    else:
                        raise(TypeError)
        elif cmd_target_type == "Item":
            raise ValueError("Not implemented")
        elif cmd_target_type == "Tempo":
            pass # Time has no target
        return cmd_target_list
                    
    def read_arg_player(self, token):
        pass

    def read_arg_time(self, token):
        pass

    def read_arg_int(self, token):
        return int(token)

    def read_arg_item(self, token):
        pass

    def read_arg_str(self, token):
        pass


###################################################################
# Abaixo estão classes de widgets customizados
###################################################################

class ItemMoldTable():
    """use a ttk.TreeView as a multicolumn ListBox"""
    def __init__(self, frame, items):
        self.tree = None
        self.col_names = ['ID', 'Nome', 'Tipo', 'Tags']
        self._setup_widgets(frame)
        self._build_tree(items)

    def _setup_widgets(self, container):
        s = """\
click on header to sort by that column
to change width of column drag boundary
        """

        msg = ttk.Label(container, wraplength="4i", justify="left", anchor="n",
            padding=(10, 2, 10, 6), text=s)

        # create a treeview with dual scrollbars
        self.tree = Treeview(container, columns=self.col_names, show="headings")
        vsb = Scrollbar(container, orient="vertical",
            command=self.tree.yview)
        hsb = Scrollbar(container, orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        
        msg.grid(sticky='e')
        self.tree.grid(row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='e w')

        # container.grid_columnconfigure(0, weight=1)
        # container.grid_rowconfigure(0, weight=1)

    def _build_tree(self, items):
        for col in self.col_names:
            self.tree.heading(col, text=col,
                command=lambda: self.sortby(self.tree, col, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                width=Font().measure(col.title()))

        for item in items:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = Font().measure(val)
                if self.tree.column(self.col_names[ix],width=None)<col_w:
                    self.tree.column(self.col_names[ix], width=col_w)


    def sortby(self, tree, col, descending):
        """sort tree contents when a column header is clicked on"""
        # grab values to sort
        data = [(tree.set(child, col), child) \
            for child in tree.get_children('')]
        # if the data to be sorted is numeric change to float
        #data =  change_numeric(data)
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        # switch the heading so it will sort in the opposite direction
        tree.heading(col, command=lambda a=col:
                     self.sortby(tree, a, int(not descending)))

class Playertable:
    pass

class ItemTable:
    pass

###################################################################
# Abaixo estão classes que definem janelas da interface
###################################################################

class WINDOW_BASE:
    def __init__(self) -> None:
        self.container = Tk()
        self.quit = False
        self.style = Style(self.container)
        self.container.tk.call('source', './Azure/azure.tcl')
        self.container.tk.call("set_theme", "dark")

        self.container.title(window_name)
        self.container.resizable(False, False)
        self.container.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self, event):
        self.quit = True
        self.container.destroy()


class MAIN_PAGE(WINDOW_BASE):
    def __init__(self, game_instance: Game, session) -> None:
        super().__init__()
        self.container.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.game = game_instance
        self.parser = Parser(self.game)
        self.db_session = session

        self.cmd_trigger: bool = False
        self.player_ids = [p.id for p in self.game.players]

        self.container.bind("<KeyPress-Return>", self.enter_callback)
        self.container.bind("<Key-Escape>", self.esc_callback)

        # For navigating through player pages
        self.container.bind("<Control-p>", self.bind_player_menu)
        self.player_select = 0

##### TAB INITIALIZATIONS #####

        self.tabs = Notebook(self.container)
        self.tabs.enable_traversal()

        self.items_frame = Frame(self.tabs)
        self.main_frame = Frame(self.tabs)

        self.tabs.add(self.main_frame, text='Home')
        self.tabs.add(self.items_frame, text='Itens')

##### WIDGETS IN THE ITEMS TAB #####

        self.new_item_name_entry = Entry(self.items_frame)
        self.new_item_type_entry = Entry(self.items_frame)
        self.new_item_tags_entry = Entry(self.items_frame)
        self.new_item_descrip_entry = Entry(self.items_frame)
        self.new_item_name_label = Label(self.items_frame, text="Nome do item")
        self.new_item_type_label = Label(self.items_frame, text="Tipo")
        self.new_item_tags_label = Label(self.items_frame, text="Tags")
        self.new_item_descrip_label = Label(self.items_frame, text="Descrição")
        self.add_new_item_button = Button(self.items_frame, text="Item\nNovo",
                                          command=self.add_item)
        
        self.table_frame = Frame(self.items_frame)
        mold_list = [x[0].as_tuple() for x in self.db_session.execute(select(Item_Mold)).all()]
        self.item_table = ItemMoldTable(self.table_frame, mold_list)

##### WIDGETS IN THE MAIN FRAME #####

        self.placedatetime_frame = Frame(self.main_frame)

        self.place = Label(self.placedatetime_frame,
                           text="lugar nenhum mas pqp esse lixo é chatão", anchor="center")
        self.datetime = Label(self.placedatetime_frame, text="zera hora", anchor="center")
        
        self.description_lframe = Labelframe(self.main_frame, text="descrição")
        
        self.description = Text(self.description_lframe, width=36, height=5)
        self.cmdbrowser_label = Label(self.description_lframe,
                                      text="Digite um comando", anchor="center")
        self.cmd_line = Entry(self.description_lframe)

        self.playerinfo_lframe = Labelframe(self.main_frame, text="jogadores")

        self.table_name_label = Label(self.playerinfo_lframe, text="Nome", font=("Arial", 10))
        self.table_blood_label = Label(self.playerinfo_lframe, text="Sangue", font=("Arial", 10))
        self.table_pneuma_label = Label(self.playerinfo_lframe, text="Pneuma", font=("Arial", 10))
        self.table_hunger_label = Label(self.playerinfo_lframe, text="Fome", font=("Arial", 10))
        self.table_stamina_label = Label(self.playerinfo_lframe, text="Stm", font=("Arial", 10))
        self.table_columns = ['name', 'blood', 'pneuma', 'hunger', 'stamina']
        for player in self.game.players:
            for col in self.table_columns:
                setattr(self, f'p{player.id}{col}', Label(self.playerinfo_lframe))

    def draw_screen(self): 
        self.tabs.grid(row=0)

######### Home tab

        self.description_lframe.grid(row=0, column=0)
        self.playerinfo_lframe.grid(row=0, rowspan=2, column=1)
        self.placedatetime_frame.grid(row=1, column=0)

        # description_lframe

        self.cmdbrowser_label.grid(row=0, column=0)
        self.cmd_line.grid(row=1, column=0)
        self.description.grid(row=2, column=0)
        self.description.insert("1.0", "Bem-vindo ao Antir, seu otário!")
        self.description.config(state=DISABLED)

        # playerinfo_lframe

        self.table_name_label.grid(row=0, column=0)
        self.table_blood_label.grid(row=0, column=1)
        self.table_pneuma_label.grid(row=0, column=2)
        self.table_hunger_label.grid(row=0, column=3)
        self.table_stamina_label.grid(row=0, column=4)

        for player_id in self.player_ids:
            for col_no, col in enumerate(self.table_columns):
                getattr(self, f'p{player_id}{col}').grid(row=player_id+1, column=col_no)
        
        # placedatetime_lframe

        self.place.grid(row=0, column=0)
        self.datetime.grid(row=0, column=1)

######### Items tab

        self.table_frame.grid(sticky='nsew', columnspan=5)

        self.new_item_name_label.grid(row=2, column=0)
        self.new_item_type_label.grid(row=2, column=1)
        self.new_item_tags_label.grid(row=2, column=2)
        self.new_item_descrip_label.grid(row=2, column=3)
        self.add_new_item_button.grid(row=2, column=4, rowspan=2)

        self.new_item_name_entry.grid(row=3, column=0)
        self.new_item_type_entry.grid(row=3, column=1)
        self.new_item_tags_entry.grid(row=3, column=2)
        self.new_item_descrip_entry.grid(row=3, column=3)



    def on_closing(self):
        if askokcancel("Quit", "Are you sure you want to quit?"):
            self.container.destroy()
            self.quit = True

    def enter_callback(self, event):
        res = self.parser.parse(self.cmd_line.get())
        self.cmd_line.delete(0, 'end')
        if res != None:
            self.game.execute(*res)

    def add_item(self):
        exit
        self.new_item_name_entry
        self.new_item_type_entry
        self.new_item_tags_entry
        self.new_item_descrip_entry

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

    def configure(self, context:Game):
        self.datetime.config(text=str(context.time))

    def begin(self, game):
        self.configure(game)
        self.draw_screen()

    def read_input(self):
        if cmd:=self.cmd_line.get():
            self.parser.parse(cmd)
            self.reply(self.parser.ans)

    def reply(self, text):
        self.description.configure(state=NORMAL)
        self.description.delete(0.0, END)
        self.description.insert(END, text + '\n')
        self.description.configure(state=DISABLED)

    def update_widgets(self, g: Game):
        self.datetime.config(text=str(g.time))

        for p in g.players:
            getattr(self, f'p{p.id}name').config(text=str(getattr(p, "name")))
            for col in self.table_columns[1:]:
                getattr(self, f'p{p.id}{col}').config(text=str(getattr(p, 'state_' + col)))
    
        self.place.config(text=g.location)

        self.container.update_idletasks()
        self.container.update()





class PLAYER_PAGE(WINDOW_BASE):
    def __init__(self) -> None:
        super().__init__()

        self.player_ids = []
