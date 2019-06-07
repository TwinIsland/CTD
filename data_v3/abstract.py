#encoding:utf-8

import json

with open('sj.json','r', encoding='utf-8',errors='ignore') as f:
    data = f.read()


datas = json.loads(data)



#{'title': '关雎', 'chapter': '国风', 'section': '周南', 'content': ['关关雎鸠，在河之洲']}

for data in datas:
    with open('data/' + data['title']+'.txt','w', encoding='gbk',errors='ignore') as f:
        for i in data['content']:
            f.write(i + '\n')