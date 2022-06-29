```python
# wtf is the encoding
try:
    c = a.decode("gbk")
except Exception :
    try:
        c = a.decode("utf-16")
    except Exception as e:
        try:
            c = a.decode("utf-8")
        except Exception as e:
            try:
                c = a.decode("mbcs")
            except Exception as e:
                try:
                    c = a.decode("cp1252")
                except Exception as e:
                    print(i[-1].split("-")[0])
                    continue
```
