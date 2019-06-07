import sql
import pickle
import pprint



content = open('result_array.pkl','rb')
data = pickle.load(content)

#sql.create_Table()

def analyze_link(i):
    str = 'https://ctd-1257758577.cos.ap-guangzhou.myqcloud.com/' + i['addr']
    str = str.replace('\\','/')
    return str


for i in data:
    try:

        sql.insertValue(i['name'],i['author'],i['age'],analyze_link(i))
    except Exception as e:
        print(str(e))
        print(i)
        input('error......')


sql.commit()