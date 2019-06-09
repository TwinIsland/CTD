#encoding:utf-8
import library
import fastclean

api = 'E:\GFEC - Global Free Education Center\CTCdata - Chinese Traditional Classical Database\Data\话'
url = 'https://ctd-1257758577.cos.ap-guangzhou.myqcloud.com/data/%E8%AF%9D/'
cid = 54766 + 1
count = 0

library = library.library()
container = fastclean.data()

container.load_data([api])
data = container.data

for i in data:
    title = i.split('\\')[-1].split('-')[0]
    age = i.split('\\')[-1].split('-')[1]
    author = i.split('\\')[-1].split('-')[2].split('.')[0]
    link = url + i.split('\\')[-1].split('\\')[-1]

    re = [cid,title,author,age,link]
    print(re)
    library.addMethod(re,'book')
    cid += 1

library.save_change()

