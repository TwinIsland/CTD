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
        self.mid_last = None
        self.uid_last = None
        self.cid_last = None
        if not exists('web.db'):
            print("init fail")
            raise FileNotFoundError("cannot find db, place the web.db under the same fold")
        self.conn = sqlite3.connect('web.db')
        self.c = self.conn.cursor()
        self.update_last_pointer()
        print(rec_msg("Start Web DB Instance"))

    def update_last_pointer(self):
        content_last = list(self.c.execute("SELECT * FROM ctd_contents ORDER BY cid DESC LIMIT 1"))
        author_last = list(self.c.execute("SELECT * FROM ctd_users ORDER BY uid DESC LIMIT 1"))
        meta_last = list(self.c.execute("SELECT * FROM ctd_metas ORDER BY mid DESC LIMIT 1"))
        self.cid_last = int(content_last[0][0])
        self.uid_last = int(author_last[0][0])
        self.mid_last = int(meta_last[0][0])

    def push(self, data: list[dict]):
        print(rec_msg("begin pushing {} data".format(str(len(data)))))
        type_counter, fail_counter, ok_counter = 0, 0, 0
        for item in data:
            is_uid_update, is_mid_update, is_period_type_update = False, False, False
            try:
                item['publish'] = "unknown" if item['publish'] == "NULL" else item['publish']
                item['author'] = "unknown" if item['author'] != "NULL" else item['author']
                author_info = list(self.c.execute("SELECT * FROM ctd_users WHERE screenName='{author}';"
                                                  .format(author=item['author'])))
                if len(author_info) == 0:
                    self.c.execute("INSERT INTO ctd_users (uid,screenName) \
                                    VALUES ({uid},'{sn}')".
                                   format(uid=self.uid_last + 1,
                                          sn=item["author"]))

                    author_id = self.uid_last + 1
                    is_uid_update = True
                else:
                    author_id = author_info[0][0]

                self.c.execute("INSERT INTO ctd_contents (cid,title,created,modified,text,authorId,type,status,"
                               "allowComment, allowPing) \
                                VALUES ({c},'{t}',{time},{time},'{text}',{au},'page','publish',1,1)".
                               format(c=self.cid_last + 1,
                                      t=item['title'],
                                      time=int(time.time()),
                                      text=item['publish'] + '|' + item['content'],
                                      au=author_id))

                type_period_info = list(self.c.execute("SELECT * FROM ctd_metas WHERE name='{}'".
                                                       format("period_" + item['publish'])))
                if len(type_period_info) == 0:
                    self.c.execute("INSERT INTO ctd_metas (mid,name,slug,type,count,parent) \
                                                        VALUES ({mid},'{name}','{name}','category',1,0)".
                                   format(mid=self.mid_last + 1,
                                          name="period_" + item["publish"]))
                    type_period_mid = self.mid_last + 1
                    is_period_type_update = True
                else:
                    type_period_mid = type_period_info[0][0]
                    self.c.execute("Update ctd_metas set count = {count} where mid = {mid}".
                                   format(count=type_period_info[0][5] + 1,
                                          mid=type_period_info[0][0]))
                self.c.execute("INSERT INTO ctd_relationships (cid, mid) \
                                VALUES ({cid},{mid})".format(cid=self.cid_last + 1,
                                                             mid=type_period_mid))

                type_info = list(self.c.execute("SELECT * FROM ctd_metas WHERE name='{}'".format(item['type'])))
                if len(type_info) == 0:
                    self.c.execute("INSERT INTO ctd_metas (mid,name,slug,type,count,parent) \
                                    VALUES ({mid},'{name}','{name}','category',1,0)".
                                   format(mid=self.mid_last + 1 + int(is_period_type_update),
                                          name=item["type"]))
                    type_counter += 1
                    type_mid = self.mid_last + 1 + int(is_period_type_update)
                    is_mid_update = True
                else:
                    type_mid = type_info[0][0]
                    self.c.execute("Update ctd_metas set count = {count} where mid = {mid}".
                                   format(count=type_info[0][5] + 1,
                                          mid=type_mid))

                self.c.execute("INSERT INTO ctd_relationships (cid, mid) \
                                VALUES ({cid},{mid})".format(cid=self.cid_last + 1,
                                                             mid=type_mid))

            except Exception as e:
                self.conn.rollback()
                fail_counter += 1
                print("fail to push: {} -- {}".format(item["title"], str(e)[:50] + '\n'))
                continue

            self.uid_last += int(is_uid_update)
            self.mid_last += int(is_mid_update) + int(is_period_type_update)
            self.cid_last += 1
            ok_counter += 1
            self.conn.commit()

        print(ok_msg("successful pushing {} books and {} types, {} fail".
                     format(str(ok_counter), str(type_counter), str(fail_counter))))

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
