# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 15:53:14 2022

@author: Usuario
"""

from classes.game import Game
from classes.gui import GUI
from classes.parser import Parser
from classes.solver import Solver

def main():
    game_instance = Game()
    display = GUI()
    parser = Parser()
    solver = Solver(game_instance)
    
    display.begin(game_instance)

    while not display.quit:
        parser.parse(display.command)

        display.reply(parser)

        if display.runCommand:
            display.runCommand = False
            solver.run_command(parser.command, game_instance)

        display.update_widgets(game_instance)


if __name__ == "__main__":
    main()
