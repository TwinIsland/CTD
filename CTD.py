import sqlite3
from os.path import exists
import time


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def fail_msg(msg, sId="ADMIN"):
    c = "[X] sId: " + str(sId) + " --- " + msg + "    " + get_time() + "\n"
    file = open("EVENT.TXT", 'a+')
    file.write(c)
    file.close()
    return c


def ok_msg(msg, sId="ADMIN"):
    c = "[V] sId: " + str(sId) + " --- " + msg + "    " + get_time() + "\n"
    file = open("EVENT.TXT", 'a+')
    file.write(c)
    file.close()
    return c


def rec_msg(msg, sId="ADMIN"):
    c = "[-] sId: " + str(sId) + " --- " + msg + "    " + get_time() + "\n"
    file = open("EVENT.TXT", 'a+')
    file.write(c)
    file.close()
    return c


class CTD:
    def __init__(self):
        if not exists('ctd.db'):
            self.__new_database__()
        self.conn = sqlite3.connect('ctd.db')
        self.c = self.conn.cursor()
        print(rec_msg("Start CTD DB Instance"))

    def __new_database__(self):
        if exists('ctd.db'):
            print("database already exist!")
            return
        self.conn = sqlite3.connect('ctd.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE Data
               (CID INTEGER PRIMARY KEY    AUTOINCREMENT,
               TITLE           CHAR(50)    NOT NULL UNIQUE,
               PUBLISH         CHAR(10),
               AUTHOR          CHAR(10),
               CONTENT         TEXT        NOT NULL);''')

        self.c.execute('''CREATE TABLE Relation
               (CID           INT    NOT NULL,
                TID           INT    NOT NULL);''')

        self.c.execute('''CREATE TABLE Type
               (TID  INTEGER PRIMARY KEY  AUTOINCREMENT,
                Desc          TEXT    NOT NULL UNIQUE);''')

        self.conn.commit()
        self.conn.close()
        print(ok_msg("Complete construct database"))

    def push(self, data: list[dict]):
        print(rec_msg("begin pushing {} data".format(str(len(data)))))
        type_counter, fail_counter, ok_counter = 0, 0, 0
        for item in data:
            item['publish'] = "'" + item['publish'] + "'" if item['publish'] != "NULL" else item['publish']
            item['author'] = "'" + item['author'] + "'" if item['author'] != "NULL" else item['author']
            try:
                self.c.execute("INSERT INTO Data (TITLE,PUBLISH,AUTHOR,CONTENT) \
                                VALUES ('{t}',{p},{a},'{c}')".format(t=item['title'],
                                                                     p=item['publish'],  # set as "NULL" if no info
                                                                     a=item['author'],  # set as "NULL" if no info
                                                                     c=item['content']))
                cur_cid = self.c.lastrowid
                type_info = list(self.c.execute("SELECT * FROM Type WHERE DESC='{}';".format(item['type'])))
                if len(type_info) == 0:
                    self.c.execute("INSERT INTO Type (Desc) \
                                    VALUES ('{desc}')".format(desc=item['type']))
                    type_counter += 1
                type_info = list(self.c.execute("SELECT * FROM Type WHERE DESC='{}';".format(item['type'])))
                self.c.execute("INSERT INTO Relation (CID, TID) \
                                VALUES ({cid},{tid})".format(cid=cur_cid,
                                                             tid=type_info[0][0]))
                ok_counter += 1
            except Exception as e:
                fail_counter += 1
                print("fail to push: {} -- {}".format(item["title"], str(e)[:50] + '\n'))
        print(ok_msg("successful pushing {} books and {} types, {} fail".
                     format(str(ok_counter), str(type_counter), str(fail_counter))))

    def commit(self):
        self.conn.commit()
        print(ok_msg("committed"))

    def connect(self):
        self.conn = sqlite3.connect('ctd.db')
        self.c = self.conn.cursor()
        print(rec_msg("reconnect CTD database"))

    def close(self):
        self.conn.close()
        print(ok_msg("database closed"))

    def length(self):
        self.c.execute("SELECT max(rowid) from Data")
        return self.c.fetchone()[0]


