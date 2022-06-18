import time
from os.path import exists
import sqlite3


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


class CosDB:
    def __init__(self, db_name: str):
        self.db_name = db_name
        if not exists(db_name):
            print("init fail")
            raise FileNotFoundError("cannot find db, place the {} under the same fold".format(db_name))
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        print(rec_msg("Start {} Instance".format(db_name)))
        self.init_status = True

    '''
    data = [
    {
        "title": "book title",
        "author": "book author",   # Set as "NULL" if no info
        "type": "book type",
        "publish": "when publish"  # Set as "NULL" if no info,
        "dir": "file address"
    }
    ]
    '''

    def merge_text(self, data: list[dict]):
        if not self.init_status:
            raise ConnectionError("fail to initialized")
        print(rec_msg("begin pushing {} data".format(str(len(data)))))
        type_counter, fail_counter, ok_counter = 0, 0, 0
        for item in data:
            try:
                item['publish'] = "Unknown" if item['publish'] == "NULL" or item['publish'] == "" else item['publish']. \
                    replace(" ", "_")
                item['author'] = "Unknown" if item['author'] == "NULL" or item['author'] == "" else item['author']. \
                    replace(" ", "_")

                if not exists(item["dir"]):
                    raise FileNotFoundError("cannot find book: " + item["title"])

                # insert content
                self.c.execute("UPDATE ctd_contents SET text='{text}' WHERE title='{title}'".
                               format(title=item['title'],
                                      text=item['publish'] + '|' + item["author"]))

            except Exception as e:
                fail_counter += 1
                print("fail to update: {} -- {}".format(item["title"], str(e)[:50] + '\n'))
                continue

            ok_counter += 1

        print(ok_msg("update {} books and {} types, {} fail".
                     format(str(ok_counter), str(type_counter), str(fail_counter))))

    def commit(self):
        if not self.init_status:
            raise ConnectionError("fail to initialized")
        self.conn.commit()
        print(ok_msg("commit ok"))

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()
        print(rec_msg("reconnect {}".format(self.db_name)))
        self.init_status = True

    def close(self):
        if not self.init_status:
            raise ConnectionError("fail to initialized")
        self.conn.close()
        print(ok_msg("database closed"))

    def rollback(self):
        if not self.init_status:
            raise ConnectionError("fail to initialized")
        self.conn.rollback()

    def length(self):
        if not self.init_status:
            raise ConnectionError("fail to initialized")
        self.c.execute("SELECT max(rowid) from ctd_contents")
        return self.c.fetchone()[0]
