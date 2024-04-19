import sqlite3 as sql

connection = sql.connect('items.db')

cursor = connection.cursor()

with connection:
    cursor.execute("""CREATE TABLE IF NOT EXISTS items(
        name VARCHAR(120) NOT NULL,
        params VARCHAR(300),
        tags VARCHAR(20) NOT NULL);"""
    )

with connection:
    cursor.execute("INSERT INTO items VALUES (:name, :desc, :tags, :state, :notes)", 
                   {'name':'Avental de Mineiro de Cron',
                    'params':'average_weight=2.0;weight_range=0.15',
                    'tags':'cl-co-un'})

cursor.execute("""SELECT * FROM items WHERE name=:name""", 
               {'name':'Avental de Mineiro'})
print(cursor.fetchone())
