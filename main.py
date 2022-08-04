# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 15:53:14 2022

@author: Usuario
"""

from classes import *


def main():
    game = Game()
    gui = GUI(game)

    gui.dark_mode()

    gui.bind_keys()

    gui.draw_screen()

    gui.begin()


if __name__ == "__main__":
    main()