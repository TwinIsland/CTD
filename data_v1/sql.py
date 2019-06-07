#encoding:utf-8

import sqlite3  


c = sqlite3.connect('ctd.db')

con = c.cursor()

def create_Table():
    con.execute('''create table ctb(name char not null,
                                    author char,
                                    age char,
                                    link char
                                    )''')

    c.commit()

def insertValue(name,author,age ,link):
    if author == '' and age == '':
        con.execute('''insert into ctb(name, link) values(?,?)''',[name,link])
    if author != '' and age == '':
        con.execute('''insert into ctb(name, author, link) values(?,?,?)''', [name, author,link])
    if author == '' and age != '':
        con.execute('''insert into ctb(name,age,link) values(?,?,?)''', [name, age,link])
    elif author != '' and age != '':
        con.execute('''insert into ctb(name,author,age,link) values(?,?,?,?)''', [name, author, age, link])


def commit():
    c.commit()


def show(num):
    data = con.execute('''select * from ctb''')

    if num == 0:
        for i in data:
            print(i)
            print('------------')
    else:
        for i in data:
            if num <0:
                break
            num += 1
            print(i)
            print('------------')

def get_item(name):
    data = list(con.execute('''select * from ctb where name is ?''',[name]))
    return data


def get_content_from_file(file):
    return open(file,'r',encoding='gb18030',errors='ignore').read()
