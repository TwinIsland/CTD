#encoding:utf-8

# https://ctd-1257758577.cos.ap-guangzhou.myqcloud.com/data/

import library
import json

with open('sj.json','r', encoding='utf-8',errors='ignore') as f:
    data = f.read()


datas = json.loads(data)
api = 'https://ctd-1257758577.cos.ap-guangzhou.myqcloud.com/data/诗经/'
library = library.library()

id = 28765

for i in range(id,id+len(datas)):
    re = [i,'诗经：' + datas[i-id]['title'],'诗经',datas[i-id]['section'],api+datas[i-id]['title'] + '.txt']
    print(re)
    library.addBook(re)
library.save_change()