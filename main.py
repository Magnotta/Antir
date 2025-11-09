# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 15:53:14 2022

@author: Usuario
"""

from classes.game import Game
from gui.gui import MAIN_PAGE
from player.player import Player

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from db.models import Base

def main():
    engine = create_engine('sqlite:///db/antir_db.db')
    Base.metadata.create_all(engine)
    session = Session(engine, future=True)

    try:
        session.begin()
        # session.add(teste)
        session.flush()
        session.commit()
    except IntegrityError:
        session.rollback()

    test_players = [Player('joao'), Player('jose'), Player('seucu'), Player('miguel'), Player('sandino'), Player('castro')]
    game_instance = Game(players=test_players)
    display = MAIN_PAGE(game_instance, session)
    
    display.begin(game_instance)

    while not display.quit:
        display.read_input()

        if display.cmd_trigger:
            display.cmd_trigger = False
            game_instance.execute(display.parser.exec)

        display.update_widgets(game_instance)


if __name__ == "__main__":
    main()
