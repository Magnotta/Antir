# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 15:53:14 2022

@author: Usuario
"""
from msilib.schema import File
import gameroutines as gr


def main():
    while(True):
        opt = input("1 - New Game\n2 - Load Game\n3 - Quit\n")
        match opt:
            case '1':
                savePath, players = gr.newGameRoutine()
                eng = gr.startEngine(players, 0)

            case '2':
                savePath, players, gameTime = gr.loadGameRoutine()
                if(savePath is None):
                    continue
                eng = gr.startEngine(players, gameTime)

            case '3':
                break

            case _:
                print("Not a valid option.")

if __name__ == "__main__":
    main()