import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
    "INSERT INTO users (username, password, admin) VALUES (?, ?, ?)",
    ('admin', 'password', '1')
)


cur.execute(
    "INSERT INTO posts (title, header, content, admin) VALUES (?, ?, ?, ?)",
    (
        'Hello World!',
        'My first post on my new blog',
        '# Hello World! <br> This is my very first blog post. Havent got much to say yet but look forward to posting more!',
        '0'
    )
)

cur.execute(
    "INSERT INTO posts (title, header, content, admin) VALUES (?, ?, ?, ?)",
    (
        'Struggle for content',
        'Im a bit stuck with what to type',
        '# Struggle for content <br> I cant think of anything to type here yet maybe I will talk about my hobbies in the future.',
        '0'
    )
)

cur.execute(
    "INSERT INTO posts (title, header, content, admin) VALUES (?, ?, ?, ?)",
    (
        'Private Post',
        'Hello, Friend...',
        'My Secret is ^FLAG^ $FLAG$',
        '1'
    )
)


connection.commit()
connection.close()