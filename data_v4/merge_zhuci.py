#encoding:utf-8

import sqlite3
import pprint
import library
import json

library = library.library()

jsons = ['南唐二主词.json']
json_content = []
datas = []
age = '南唐二主词'

for i in jsons:
    with open(i,'r',encoding='utf-8') as f:
        json_content.append(json.loads(f.read()))

for data in json_content:
    for item in data:
        title = item['title']
        content = item['paragraphs']
        author = item['author']
        datas.append({'title':title,'author':author,'content':''.join(content),'age':age})

cid_begin = 50617+1

count = 0
for id in range(cid_begin,cid_begin+len(datas)):
    re = [id,datas[count]['title'],datas[count]['author'],datas[count]['age'],datas[count]['content']]
    library.addMethod(re,'poem')
    count += 1
    print('finished: ' + str(count))

print('done!')
#library.save_change()

library.save_change()