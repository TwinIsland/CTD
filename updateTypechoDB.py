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

                # update content

                content_info = list(self.c.execute("SELECT * FROM ctd_contents WHERE title='{}'".
                                                       format(item["title"])))

                if len(content_info) != 0:
                    self.c.execute("UPDATE ctd_contents SET text='{text}' WHERE title='{title}'".
                                   format(title=item['title'],
                                          text=item['publish'] + '|' + item["author"]))
                else:
                    continue

                cur_cid = content_info[0][0]

                # update type->period information, formate: period_{period desc}
                type_period_info = list(self.c.execute("SELECT * FROM ctd_metas WHERE name='{}'".
                                                       format("period_" + item['publish'])))
                if len(type_period_info) == 0:
                    self.c.execute("INSERT INTO ctd_metas (name,slug,type,count,parent) \
                                                           VALUES ('{name}','{name}','category',1,0)".
                                   format(name="period_" + item["publish"]))

                    cur_mid_last = self.c.lastrowid

                    self.c.execute("INSERT INTO ctd_relationships (cid, mid) \
                                       VALUES ({cid},{mid})".format(cid=cur_cid,
                                                                    mid=cur_mid_last))
                else:
                    if len(list(self.c.execute("SELECT * FROM ctd_relationships WHERE cid={cid} AND mid={mid}".
                                   format(cid=cur_cid,
                                          mid=type_period_info[0][0])))) == 0:
                        self.c.execute("INSERT INTO ctd_relationships (cid, mid) \
                                           VALUES ({cid},{mid})".format(cid=cur_cid,
                                                                        mid=type_period_info[0][0]))

                # update type->author information
                type_author_info = list(self.c.execute("SELECT * FROM ctd_metas WHERE name='{}'".
                                                       format("author_" + item['author'])))
                if len(type_author_info) == 0:
                    self.c.execute("INSERT INTO ctd_metas (name,slug,type,count,parent) \
                                                           VALUES ('{name}','{name}','category',1,0)".
                                   format(name="author_" + item["author"]))

                    cur_mid_author = self.c.lastrowid

                    self.c.execute("INSERT INTO ctd_relationships (cid, mid) \
                                       VALUES ({cid},{mid})".format(cid=cur_cid,
                                                                    mid=cur_mid_author))
                else:
                    if len(list(self.c.execute("SELECT * FROM ctd_relationships WHERE cid={cid} AND mid={mid}".
                                                       format(cid=cur_cid,
                                                              mid=type_author_info[0][0])))) == 0:
                        self.c.execute("INSERT INTO ctd_relationships (cid, mid) \
                                           VALUES ({cid},{mid})".format(cid=cur_cid,
                                                                        mid=type_author_info[0][0]))

                # update type information
                type_info = list(self.c.execute("SELECT * FROM ctd_metas WHERE name='{}'".format(item['type'])))
                if len(type_info) == 0:
                    self.c.execute("INSERT INTO ctd_metas (name,slug,type,count,parent) \
                                                           VALUES ('{name}','{name}','category',1,0)".
                                   format(name=item["type"]))

                    cur_mid_type = self.c.lastrowid

                    self.c.execute("INSERT INTO ctd_relationships (cid, mid) \
                                       VALUES ({cid},{mid})".format(cid=cur_cid,
                                                                    mid=cur_mid_type))
                else:
                    if len(list(self.c.execute("SELECT * FROM ctd_relationships WHERE cid={cid} AND mid={mid}".
                                                       format(cid=cur_cid,
                                                              mid=type_info[0][0])))) == 0:
                        self.c.execute("INSERT INTO ctd_relationships (cid, mid) \
                                           VALUES ({cid},{mid})".format(cid=cur_cid,
                                                                        mid=type_info[0][0]))

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
