# Usage
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

## Database

![Snipaste_2022-06-15_20-30-33](pic/Snipaste_2022-06-15_20-30-33.png)

## TypechoDB
DB API that support native Typecho Sqlite database

**To get a better using experience, please set:**

contents: `cid`, `title`, `slug`

metas: `mid`, `name`, `slug`

users: `uid`, `name`

as *UNIQUE*, you may find `webdb_sample.db` useful