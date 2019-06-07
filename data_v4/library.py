import sqlite3
import time

class library:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()


    def addMethod(self,information,tag):
        #
        # depend on web/post.php
        #
        # tag: book | poem
        #
        # book_information: [id,book_name,book_author,book_age,book_link]
        # poem_information: [id,poem_name,poem_author,poem_age,poem_content]
        #
        def get_time_stamp():
            return int(time.time())

        content = '[' + tag + ',' + information[2] + ',' + information[3] + ']' + information[4]
        total_information = [information[0],information[1],str(information[0])
                             ,get_time_stamp(),get_time_stamp(),content,1,'post','publish'
                             ,0,1,1,1,0]

        self.c.execute('''INSERT INTO ctd_contents(cid,title,slug
                          ,created,modified,text,authorId,
                          type,status,commentsNum,allowComment,
                          allowPing,allowFeed,parent)VALUES(?,?,?
                          ,?,?,?,?,?,?,?,?,?,?,?)''',total_information)



    def cleanDataBase(self):
        self.c.execute('''DELETE FROM ctd_contents''')

    def save_change(self):
        self.conn.commit()

