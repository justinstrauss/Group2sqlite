import csv, sqlite3

#run populate.py only if blogs.db is not present
conn = sqlite3.connect("blogs.db")
c = conn.cursor()

c.execute("CREATE TABLE blogs (title TEXT, name TEXT, entry TEXT, id INTEGER UNIQUE)")

base = 'INSERT INTO blogs VALUES("%(title)s","%(name)s", "%(entry)s",%(id)s)'
for a in csv.DictReader(open("blogposts.csv")):
    i = base%a
    print i
    c.execute(i)

conn.commit()

c.execute("CREATE TABLE comments (name TEXT, comment TEXT, id INTEGER)")

base = 'INSERT INTO comments VALUES("%(name)s","%(comment)s",%(id)s)'
for a in csv.DictReader(open("comments.csv")):
    i = base%a
    print i
    c.execute(i)

conn.commit()
