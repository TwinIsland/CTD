import sqlite3
from os.path import exists
import eventRec

if exists('ctd.db'):
    print("database already exist!")
    exit()

conn = sqlite3.connect('ctd.db')

c = conn.cursor()
c.execute('''CREATE TABLE Data
       (CID INTEGER PRIMARY KEY    AUTOINCREMENT,
       TITLE           CHAR(50)    NOT NULL UNIQUE,
       PUBLISH         CHAR(10),
       AUTHOR          CHAR(10),
       CONTENT         TEXT        NOT NULL);''')

c.execute('''CREATE TABLE Relation
       (CID           INT    NOT NULL,
        TID           INT    NOT NULL);''')

c.execute('''CREATE TABLE Type
       (TID  INTEGER PRIMARY KEY  AUTOINCREMENT,
        Desc          TEXT    NOT NULL UNIQUE);''')

conn.commit()
conn.close()
print(eventRec.ok_msg("Complete construct database"))
