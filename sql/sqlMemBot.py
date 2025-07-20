import sqlite3

from random import random




conn = sqlite3.connect('MemBot.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS phrases(
id INTEGER PRIMARY KEY AUTOINCREMENT,
phrase TEXT)
''')

cursor.execute('''CREATE TABLE IF NOT EXISTS DND_hyesoss_ebalai_lumidorchik_vihodi(
id INTEGER PRIMARY KEY AUTOINCREMENT,
phrase TEXT)
''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Player_points(
id INTEGER PRIMARY KEY AUTOINCREMENT,
tg_id TEXT,
tg_name TEXT,
point INTEGER)
''')

def append_phrases(phrs):
    cursor.execute('INSERT INTO phrases(phrase) VALUES(?)',[phrs])
    conn.commit()

def append_phrases(phrs):
    cursor.execute('INSERT INTO DND_hyesoss_ebalai_lumidorchik_vihodi(phrase) VALUES(?)',[phrs])
    conn.commit()

def random_phrases():
    cursor.execute('SELECT * FROM phrases ORDER BY RANDOM() LIMIT 10')
    return [phras[1] for phras  in cursor.fetchall()]


def increase_points(tg_id,points):
    cursor.execute(f'UPDATE Player_points SET point = point + {points} WHERE tg_id = {tg_id}')
    conn.commit()



def append_player(tg_id,tg_name):
    info = cursor.execute('SELECT * FROM Player_points WHERE tg_id=?', (tg_id, ))
    if info.fetchone() is None: 
        cursor.execute('INSERT INTO Player_points(tg_id,tg_name,point) VALUES(?,?,?)',[tg_id,tg_name,0])
        conn.commit()
