import os
import pprint

class data:
    def __init__(self):
        self.data = []

    def load_data(self,fold_array):

        files = []
        for root in fold_array:
            # print(root)
            for parent, dirnames, filenames in os.walk(root):
                for ii in filenames:
                    files.append(parent + '\\' + ii)

                for i in dirnames:
                    dir = parent + '\\' + i
                    # print(dir)
                    files.append([parent, dir])

        temp = []
        for i in files:
            # print(str(type(i)))
            if str(type(i)) == '<class \'list\'>':
                # print(i)
                for ii in i:
                    temp.append(ii)
                    continue
            else:
                temp.append(i)
        self.data = temp

    def show_data(self):
        pprint.pprint(self.data)

    def eliminate_file_type(self,eliminated_type_array):
        for file in self.data:
            removed = 0
            for type in eliminated_type_array:
                if file.split('\\')[-1] == type:
                    removed = 1
                    break
            if removed:
                self.data.remove(file)

    def eliminate_letter(self,blackList):
        for file in self.data:
            removed = 0
            for ban in blackList:
                if file.__contain__(ban):
                    removed = 1
                    break
            if removed:
                self.data.remove(file)

    def reduce_letter(self,reduced_list):
        temp = []
        for file in self.data:
            parent = file[0:file.rfind('\\', 1) + 1]
            bookName = file.split('\\')[-1]

            for reducedItem in reduced_list:
                bookName = bookName.replace(reducedItem,'')

            temp.append(parent + '\\' + bookName)
