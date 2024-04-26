# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 15:53:14 2022

@author: Usuario
"""

from classes.game import Game
from gui.gui import MAIN_PAGE
from classes.solver import Solver
from player.player import Player
from classes.logger import Logger

def main():
    test_players = [Player('joao'), Player('jose'), Player('seucu'), Player('miguel'), Player('sandino'), Player('castro')]
    game_instance = Game(players=test_players)
    display = MAIN_PAGE(game_instance)
    logger = Logger()
    
    game_instance.start()
    display.begin(game_instance)

    while not display.quit:
        display.read_input()

        if display.cmd_trigger:
            display.cmd_trigger = False
            game_instance.execute(display.parser.parsed)
            logger.log(game_instance)

        display.update_widgets(game_instance)


if __name__ == "__main__":
    main()
