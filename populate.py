import csv, sqlite3

def setup():
    #run populate.py only if blogs.db is not present
    conn = sqlite3.connect("blogs.db")
    c = conn.cursor()

    c.execute("CREATE TABLE blogs (title TEXT, name TEXT, entry TEXT, id INTEGER UNIQUE, time TEXT)")
    
    conn.commit()

    c.execute("CREATE TABLE comments (name TEXT, comment TEXT, id INTEGER)")
    
    base = '''INSERT INTO blogs VALUES("%(title)s","%(name)s","%(entry)s",%(id)s,"%(time)s")'''
    for a in csv.DictReader(open("blogposts.csv")):
        i = base%a
        print i
        c.execute(i)
        
    base = '''INSERT INTO comments VALUES("%(name)s","%(comment)s",%(id)s)'''
    for a in csv.DictReader(open("comments.csv")):
        i = base%a
        print i
        c.execute(i)
    
    conn.commit()
    

def insert_post(title, name, entry, _id, time):
    conn = sqlite3.connect("blogs.db")
    c = conn.cursor()

    base = '''INSERT INTO blogs VALUES("%s","%s","%s",%s,"%s")'''
    c.execute(base % (title.replace('"',"'"),name.replace('"',"'"),entry.replace('"',"'"),_id,time))
    conn.commit()    
    

def insert_comment(name, comment, _id):
    conn = sqlite3.connect("blogs.db")
    c = conn.cursor()

    base = '''INSERT INTO comments VALUES("%s","%s",%s)'''
    c.execute(base % (name.replace('"',"'"),comment.replace('"',"'"),_id))
    conn.commit()

