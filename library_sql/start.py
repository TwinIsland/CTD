import library
import sqlite3

library = library.library()

conn = sqlite3.connect('ctd.db')
c = conn.cursor()

books = c.execute('''SELECT * FROM ctb''')

id = 0

for book in books:
    id += 1
    book = list(book)
    for element in range(len(book)):
        if book[element] == None:
            book[element] = 'unknown'
    print(book)

    library.addBook([id,book[0],book[1],book[2],book[3]])
library.save_change()

