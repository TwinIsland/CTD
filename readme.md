# Usage

## CTD

The standard CTD database, used for building own project from zero

```python
import CTD

# New a instance
ctd_db = CTD.CTD()

# data structure
data = [
    {
    "title": "book title",
     "author": "book author",    # Set as "NULL" if no info
     "content": "content of the book",
     "type": "book type",
     "publish": "when publish"   # Set as "NULL" if no info
    }  
]

# push data to database
ctd_db.push(data)

# get length
print(ctd_db.length())

# save and close
ctd_db.commit()
ctd_db.close()

# reconnect
ctd_db.connect()
```

### CTD data structure

![Snipaste_2022-06-15_20-30-33](pic/Snipaste_2022-06-15_20-30-33.png)

> TYPO: `Table_3` should be `Type`

## TypechoDB

DB API that support native Typecho Sqlite database

**To get a better using experience, please set:**

contents: `cid`, `title`, `slug`

metas: `mid`, `name`, `slug`

users: `uid`, `name`

as *UNIQUE*, and all primary key with auto increasing property. 

For this form of database, due to the characteristic of Typecho, the web may crack as the volume excess certain amount. This problem can be solved by using OSS (Object Storage), which will be introduced later.

Its usage is nearly the same as CTD 

## TencentCosDB

Typecho Database API with Tencent Cos OSS. I also distribute this plan on my own CTD website.

```python
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

dat = TencentCOS.CosDB(db_name="web.db",
                       cos_client=client,
                       bucket="")

data = [
    {
     "title": "book title",
     "author": "book author",    # Set as "NULL" if no info
     "content": "content of the book",
     "type": "book type",
     "dir": "file address"  
    }  
]

dat.push(data)
```

This DB share the same methods with other two, feel free to use.

More configuration information please refer Tencent API document.

## Theme

Redesign and revise based on default theme of Typecho, compatible with `TencentCosDB`

