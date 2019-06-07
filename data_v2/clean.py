#encoding:utf-8
import os
import library

resource_dict = ['E:\GFEC - Global Free Education Center\我的掌上书库\古典文学',
                 'E:\GFEC - Global Free Education Center\我的掌上书库\历史书籍',
                 'E:\GFEC - Global Free Education Center\我的掌上书库\诸子百家']



files = []
for root in resource_dict:
    #print(root)
    for parent, dirnames, filenames in os.walk(root):
        for ii in filenames:
            files.append(parent + '\\' + ii)

        for i in dirnames:
            dir = parent + '\\' + i
            # print(dir)
            files.append([parent, dir])

#print(len(files))

temp = []
for i in files:
    #print(str(type(i)))
    if str(type(i)) == '<class \'list\'>':
        #print(i)
        for ii in i:
            temp.append(ii)
            continue
    else:
        temp.append(i)


removed = 0

files = temp


print('====================\n')


print(len(files))
print(files)

print('====================\n')

def isInt(word):
    try:
        int(word)
    except Exception:
        return 0
    return 1

result = []
for i in files:
    parent = i[0:i.rfind('\\', 1) + 1]
    book = i.split('\\')[-1]
    book = book.replace(' ','')
    book = book.split('_')[0]

    if book.__contains__('mydoc'):
        book = i.split('\\')[-2] + book[-6:]

    if isInt(book[:1]):
        book = i.split('\\')[-2] + book

    if not book.__contains__('txt') and not book.__contains__('TXT'):
        continue
    blackList = ['论坛','讲义','资料','绝窍','ebook','李涵辰','[原创]','INDEX','index']
    ban = 0
    for banWord in blackList:
        if book.__contains__(banWord):
            ban = 1
    if ban:
        continue

    if book[1] == '.':
        book = i.split('\\')[-2] + '-' + book

    book = book.replace('TXT','txt')
    book = book.replace('黄金书屋---','')
    addr = parent + '/' + book
    print(parent + '/' + book)
    result.append(addr)

files = result

print(len(files))

print('==================')


api = 'https://ctd-1257758577.cos.ap-guangzhou.myqcloud.com/data/201966/'
# example: 'E:\GFEC - Global Free Education Center\我的掌上书库\古典文学\易学书籍\象数\周易卦象\\周易卦象-离.txt'

library = library.library()

cid = 28007

for i in range(cid,cid+len(files)):
    book = files[i-cid]
    bookURL = api + book.split('我的掌上书库\\')[1].replace('\\','/').replace('//','/')
    bookName = book.split('/')[-1][:-4]
    print(bookName)
    print(bookURL)
    library.addBook([i,bookName,'unknown','unknown',bookURL])

library.save_change()