import sqlite3 as sql

connection = sql.connect('items.db')

cursor = connection.cursor()

name = 'Avental de Mineiro de Cron'
params = 'weight=2.0'
tags = 'cl-co-un'

with connection:
    cursor.execute("INSERT INTO items VALUES (:name, :desc, :tags, :state, :notes)", 
                   {'name':name,
                    'params':params,
                    'tags':tags})