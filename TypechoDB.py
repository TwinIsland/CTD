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


class WebDB:
    def __init__(self):
        if not exists('web.db'):
            print("init fail")
            raise FileNotFoundError("cannot find db, place the web.db under the same fold")
        self.conn = sqlite3.connect('web.db')
        self.c = self.conn.cursor()
        print(rec_msg("Start Web DB Instance"))

    def push(self, data: list[dict]):
        print(rec_msg("begin pushing {} data".format(str(len(data)))))
        type_counter, fail_counter, ok_counter = 0, 0, 0
        for item in data:
            try:
                item['publish'] = "Unknown" if item['publish'] == "NULL" or item['publish'] == "" else item['publish'].\
                    replace(" ", "_")
                item['author'] = "Unknown" if item['author'] == "NULL" or item['author'] == "" else item['author'].\
                    replace(" ", "_")
                item['content'] = item['content'].replace("'", "''")

                # insert content
                self.c.execute("INSERT INTO ctd_contents (title,created,modified,text,allowComment, allowPing) \
                                VALUES ('{t}',{time},{time},'{text}',1,1)".
                               format(t=item['title'],
                                      time=int(time.time()),
                                      text=item['publish'] + '|' + item["author"] + "|" + item['content'], ))

                cur_cid = self.c.lastrowid

                # update type->period information, formate: period_{period desc}
                type_period_info = list(self.c.execute("SELECT * FROM ctd_metas WHERE name='{}'".
                                                       format("period_" + item['publish'])))
                if len(type_period_info) == 0:
                    self.c.execute("INSERT INTO ctd_metas (name,slug,type,count,parent) \
                                                        VALUES ('{name}','{name}','category',1,0)".
                                   format(name="period_" + item["publish"]))
                    cur_mid_period = self.c.lastrowid
                else:
                    cur_mid_period = type_period_info[0][0]
                    self.c.execute("Update ctd_metas set count = {count} where mid = {mid}".
                                   format(count=type_period_info[0][5] + 1,
                                          mid=cur_mid_period))
                self.c.execute("INSERT INTO ctd_relationships (cid, mid) \
                                VALUES ({cid},{mid})".format(cid=cur_cid,
                                                             mid=cur_mid_period))

                # update type->author information
                type_author_info = list(self.c.execute("SELECT * FROM ctd_metas WHERE name='{}'".
                                                       format("author_" + item['author'])))
                if len(type_author_info) == 0:
                    self.c.execute("INSERT INTO ctd_metas (name,slug,type,count,parent) \
                                                        VALUES ('{name}','{name}','category',1,0)".
                                   format(name="author_" + item["author"]))
                    cur_mid_author = self.c.lastrowid
                else:
                    cur_mid_author = type_author_info[0][0]
                    self.c.execute("Update ctd_metas set count = {count} where mid = {mid}".
                                   format(count=type_author_info[0][5] + 1,
                                          mid=cur_mid_author))
                self.c.execute("INSERT INTO ctd_relationships (cid, mid) \
                                VALUES ({cid},{mid})".format(cid=cur_cid,
                                                             mid=cur_mid_author))

                # update type information
                type_info = list(self.c.execute("SELECT * FROM ctd_metas WHERE name='{}'".format(item['type'])))
                if len(type_info) == 0:
                    self.c.execute("INSERT INTO ctd_metas (name,slug,type,count,parent) \
                                    VALUES ('{name}','{name}','category',1,0)".
                                   format(name=item["type"]))
                    type_counter += 1
                    cur_mid_type = self.c.lastrowid
                else:
                    cur_mid_type = type_info[0][0]
                    self.c.execute("Update ctd_metas set count = {count} where mid = {mid}".
                                   format(count=type_info[0][5] + 1,
                                          mid=cur_mid_type))

                self.c.execute("INSERT INTO ctd_relationships (cid, mid) \
                                VALUES ({cid},{mid})".format(cid=cur_cid,
                                                             mid=cur_mid_type))

            except Exception as e:
                fail_counter += 1
                print("fail to push: {} -- {}".format(item["title"], str(e)[:50] + '\n'))
                continue

            ok_counter += 1

        print(ok_msg("pushing {} books and {} types, {} fail".
                     format(str(ok_counter), str(type_counter), str(fail_counter))))

    def commit(self):
        self.conn.commit()
        print(ok_msg("commit ok"))

    def connect(self):
        self.conn = sqlite3.connect('ctd.db')
        self.c = self.conn.cursor()
        print(rec_msg("reconnect CTD database"))

    def close(self):
        self.conn.close()
        print(ok_msg("database closed"))

    def rollback(self):
        self.conn.rollback()

    def length(self):
        self.c.execute("SELECT max(rowid) from ctd_contents")
        return self.c.fetchone()[0]
