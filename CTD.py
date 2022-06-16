import sqlite3
from os.path import exists
import eventRec


class CTD:
    if not exists('ctd.db'):
        print('database no found')
        exit()
    conn = sqlite3.connect('ctd.db')
    c = conn.cursor()
    print(eventRec.rec_msg("Start CTD DB Instance"))

    def push(self, data: list[dict]):
        print(eventRec.rec_msg("begin pushing {} data".format(str(len(data)))))
        type_counter, fail_counter, counter = 0, 0, 0
        for item in data:
            item['publish'] = "'" + item['publish'] + "'" if item['publish'] != "NULL" else item['publish']
            item['author'] = "'" + item['author'] + "'" if item['author'] != "NULL" else item['author']
            try:
                self.c.execute("INSERT INTO Data (TITLE,PUBLISH,AUTHOR,CONTENT) \
                                VALUES ('{t}',{p},{a},'{c}')".format(t=item['title'],
                                                                     p=item['publish'],  # set as "NULL" if no info
                                                                     a=item['author'],   # set as "NULL" if no info
                                                                     c=item['content']))
                type_info = list(self.c.execute("SELECT * FROM Type WHERE DESC='{}';".format(item['type'])))
                if len(type_info) == 0:
                    self.c.execute("INSERT INTO Type (Desc) \
                                    VALUES ('{desc}')".format(desc=item['type']))
                    type_counter += 1
                type_info = list(self.c.execute("SELECT * FROM Type WHERE DESC='{}';".format(item['type'])))
                self.c.execute("INSERT INTO Relation (CID, TID) \
                                VALUES ({cid},{tid})".format(cid=self.c.lastrowid,
                                                             tid=type_info[0][0]))
                counter += 1
            except Exception as e:
                fail_counter += 1
                print("fail to push: {} -- {}".format(item["title"], str(e) + '\n'))
        print(eventRec.ok_msg("successful pushing {} books and {} types, fail {}".
                              format(str(counter), str(type_counter), str(fail_counter))))

    def commit(self):
        self.conn.commit()
        print(eventRec.ok_msg("committed"))

    def close(self):
        self.conn.close()
        print(eventRec.ok_msg("database closed"))
