#encoding:utf-8
import fastclean
import library
import pprint

api = 'https://ctd-1257758577.cos.ap-guangzhou.myqcloud.com/data/%E5%9B%9B%E5%BA%93/'

addr = 'E:\GFEC - Global Free Education Center\CTCdata - Chinese Traditional Classical Database\Data\藏\四库'

library = library.library()
container = fastclean.data()

container.load_data([addr])

container.eliminate_fold()
data = container.data[4:]
pprint.pprint(data)
print(len(data))

age = '清代'
author = 'unknown'


cid_begin = 50662 + 1
count = 0
for id in range(cid_begin,cid_begin+len(data)):
    title = data[count].split('\\')[-1][:-4]
    url = api + data[count].split('\\')[-2] + '/' + data[count].split('\\')[-1]
    print(title)
    print(url)
    count += 1
    library.addMethod([id,title,'unknown',age,url],'book')


library.save_change()