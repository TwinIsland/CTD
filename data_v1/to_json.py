import json

import pickle
r =  open('result_array.pkl','rb')
r = pickle.load(r)
print(r)


with open('data.json','w') as f:
    json.dump(r,f)