import TypechoDB


test = [
    {"title": "你好世界",
     "author": "作者",
     "content": "你好世界hello world",
     "type": "测试1",
     "publish": "现代"},
    {"title": "你好芝加哥",
     "author": "作者2",
     "content": "你好芝加哥hello chicago",
     "type": "测试1",
     "publish": "NULL"},
    {"title": "你好香槟",
     "author": "NULL",
     "content": "你好香槟hello chicago",
     "type": "测试2",
     "publish": "唐朝"},
    {"title": "你好世界",
     "author": "NULL",
     "content": "你好香槟hello chicago",
     "type": "测试2",
     "publish": "唐朝"},
]

ctd_db = TypechoDB.WebDB()
ctd_db.push(test)
ctd_db.close()
