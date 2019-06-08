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
info = '《四库全书》全称《钦定四库全书》，是清代乾隆时期编修的大型丛书。在清高宗乾隆帝的主持下，由纪昀等360多位高官、学者编撰，3800多人抄写，耗时十三年编成。'


cid_begin = 50662 + 1
count = 0
for id in range(cid_begin,cid_begin+len(data)):
    title = data[count].split('\\')[-1][:-4]
    url = api + data[count].split('\\')[-2] + '/' + data[count].split('\\')[-1]
    print(title)
    print(url)
    count += 1
    library.addMethod([id,title,'纪昀',age,info,url],'download')


library.save_change()