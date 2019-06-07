#encoding: utf-8

import os

root = 'data'


files = []

def is_int(str):
    try:
        int(str)
        return 1
    except Exception:
        return 0

for parent,dirnames,filenames in os.walk(root):
    for i in dirnames:
        dir = parent + '\\' + i
        #print(dir)
        files.append([parent,dir])

files.reverse()

for ii in files:
    i = ii[1]

    if i.split('\\')[-1].__contains__('-') and is_int(i.split('\\')[-1][:2]):
        newName =  ii[0] + '\\' + i.split('\\')[-1][2:].split('-')[0]
        os.rename(ii[1],newName)
    elif i.split('\\')[-1].__contains__('-'):
        newName = ii[0] + '\\' + i.split('\\')[-1].split('-')[0]
        os.rename(ii[1], newName)
    elif is_int(i.split('\\')[-1][:2]):
        newName = ii[0] + '\\' + i.split('\\')[-1][2:]
        os.rename(ii[1], newName)

