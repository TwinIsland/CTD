from qcloud_cos import CosS3Client
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
    def __init__(self, db_name: str, cos_client: CosS3Client, bucket: str):
        self.cos_client = cos_client
        self.db_name = db_name
        self.bucket = bucket
        if not exists(db_name):
            print("init fail")
            raise FileNotFoundError("cannot find db, place the {} under the same fold".format(db_name))
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        print(rec_msg("Start {} Instance".format(db_name)))
        self.init_status = True

    def __upload__(self, origin, to):
        with open(origin, 'rb') as fp:
            self.cos_client.put_object(
                Bucket=self.bucket,
                Body=fp,
                Key='ctd/{}'.format(to),
                StorageClass='STANDARD',
                EnableMD5=False
            )

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

    def push(self, data: list[dict]):
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
                self.c.execute("INSERT INTO ctd_contents (title,created,modified,text,allowComment, allowPing) \
                                   VALUES ('{t}',{time},{time},'{text}',1,1)".
                               format(t=item['title'],
                                      time=int(time.time()),
                                      text=item['publish'] + '|' + item["author"]))

                cur_cid = self.c.lastrowid

                # upload to COS
                self.__upload__(item["dir"], str(cur_cid) + ".txt")

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
                self.conn.rollback()
                fail_counter += 1
                print("fail to push: {} -- {}".format(item["title"], str(e)[:50] + '\n'))
                continue

            self.conn.commit()
            ok_counter += 1

        print(ok_msg("pushing {} books and {} types, {} fail".
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
