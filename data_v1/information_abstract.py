#encoding:utf-8

import os
import pickle

root = 'data'

files = []
data = []


for parent,dirnames,filenames in os.walk(root):
    if dirnames == []:
        for i in filenames:
            print(parent + '\\' + i)
            files.append([i,parent])


                # [file name,file addr not include file name]


#print(files)

#files = [i for i in files if i != []][0]
#print(files[:10])

for i in files:
    file = i[0]
    i[1] = i[1] + '\\' + i[0]

    try:
        try:

            if file.__contains__('〖 〗'):
                print('name: ' + file.split('〖')[0])
                data.append({'name':file.split('〖')[0],'age':'','author':'','addr':i[1]})
                continue


            # split by 〖
            if file.__contains__('〖'):
                file = file.split('.')[0].split('〖')
                print('name: ' + file[0])

                if file[1][0] == ' ':
                    print('age: '  + file[1].split(' ')[1])
                    print('author: ' + file[1].split(' ')[2][:-1])
                    data.append({'name':file[0],'age':file[1].split(' ')[1],'author':file[1].split(' ')[2][:-1],'addr':i[1]})
                    print('--------------------')
                    continue
                else:
                    print('age: ' + file[1].split(' ')[0])
                    print('author: ' + file[1].split(' ')[1][:-1])
                    data.append({'name':file[0],'age':file[1].split(' ')[0],'author':file[1].split(' ')[1][:-1],'addr':i[1]})
                    print('--------------------')
                    continue

        except Exception as e:

            print('name: ' + file[0])
            print('author: ' + file[1][:-1])
            data.append({'name':file[0],'age':'','author':file[1][:-1],'addr':i[1]})
            # print('name: ' + i[0].split('.')[0])
            print('--------------------')

        # only contain name
        if not file.__contains__('-'):
            print('name: ' + file.split('.')[0])
            data.append({'name':file.split('.')[0],'age':'','author':'','addr':i[1]})
            print('--------------------')
            continue


        # name--.txt
        if file.__contains__('--'):
            print('name: ' + file.split('.')[0][:-2])
            data.append({'name':file.split('.')[0][:-2],'age':'','author':'','addr':i[1]})
            print('-------------------')
            continue

        file = file.split('.')[0]

        file = file.split('-')

        name = file[0]
        age = file[1]
        author = file[2]

        print('name: ' + name + '\n' +
              'age: ' + age + '\n' +
              'author: ' + author)
        data.append({'name':name,'age':age,'author':author,'addr':i[1]})
        print('--------------------')

    # name = all
    except Exception as e:
        print('name: ' + file[0])
        data.append({'name':file[0],'age':'','author':'','addr':i[1]})
        print('--------------------')


print(data)
print(len(data))

with open('result_array.pkl','wb') as f:
    pickle.dump(data,f)

