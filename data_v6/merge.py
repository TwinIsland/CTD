import library
import fastclean

file = 'E:\GFEC - Global Free Education Center\医\\000-神农本草经.txt'
addr = 'E:\GFEC - Global Free Education Center\医\\'
api = 'https://ctd-1257758577.cos.ap-guangzhou.myqcloud.com/data/%E5%8C%BB/'

containe = fastclean.data()
containe.load_data([addr])
containe.eliminate_type_not_have(['txt'])

'''
data = []
for i in containe.data:
    title = i.split('\\')[-1].split('-')[1][:-4]
    if title == '格致余论':
        break
    else:
        data.append(i)
'''

library = library.library()

id = 54069 + 1

for i in containe.data:
    author = 'unknown'
    age = 'unknown'
    addr = api + i.split('\\')[-1]
    title = i.split('\\')[-1].split('-')[1][:-4]
    library.addMethod([id,title,author,age,addr],'book')
    id += 1

library.save_change()