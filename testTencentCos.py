from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
import TencentCOS
import os

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
secret_id = ''
secret_key = ''
region = ''
token = None
scheme = 'https'

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)


data = []
paths = os.walk(r'./')

for path, dir_lst, file_lst in paths:
    for file_name in file_lst:
        if "txt" not in file_name:
            continue
        data.append(os.path.join(path, file_name))

data = [i.split("\\") for i in data]

data_n = []
for i in data:
    if len(i[-1].split("-")) == 3:
        data_n.append(i)
db = []

for i in data_n:
    db = []
    for i in data_n:
        ad = '//'.join(i)
        c = ''
        db.append({
            "title": i[-1].split(".")[0],
            "author": "NULL",
            "type": i[-2].split("-")[0][2:],
            "publish": "NULL",
            "dir": ad
        })
print(db[1])


dat = TencentCOS.CosDB(db_name="web.db",
                       cos_client=client,
                       bucket="")

dat.push(db)
