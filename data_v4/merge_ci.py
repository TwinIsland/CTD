#encoding:utf-8

import sqlite3
import pprint
import library
import json
import fastclean

container = fastclean.data()
container.load_data(['data'])
#container.show_data()
container.eliminate_file_type(['db'])
jsons = container.data
json_content = []
datas = []
age = '花间集'

for i in jsons:
    with open(i,'r',encoding='utf-8') as f:
        json_content.append(json.loads(f.read()))

for data in json_content:
    for item in data:
        title = item['title']
        content = item['paragraphs']
        author = item['author']
        datas.append({'title':title,'author':author,'content':''.join(content),'age':age})

library = library.library()

conn = sqlite3.connect('data/ci.db')
c = conn.cursor()

cid_begin = 29070+1

tag = 'poem'
age = '宋词'

db_data = c.execute('''select * from ci''')

for data in db_data:
    title = data[1] + '-' + data[2]
    author = data[2]

    datas.append({'title':title,'author':author,'age':age,'content':data[3]})

#print(len(datas))
count = 0
for id in range(cid_begin,cid_begin+len(datas)):
    re = [id,datas[count]['title'],datas[count]['author'],datas[count]['age'],datas[count]['content']]
    library.addMethod(re,'poem')
    count += 1
    print('finished: ' + str(count))

print('done!')
library.save_change()

# added 21592 new item !

