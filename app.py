# Albert, Alex, Justin, and Leslie
# Soft Dev Pd 7
# Database Project

from flask import Flask, render_template, request
import sqlite3
from populate import insert_post, insert_comment
import os.path

# app is an instance of the Flask class
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
@app.route("/<title>")
def home(title=None):
    if not os.path.isfile("blogs.db"):
        populate.setup()
    #run populate.py only if blogs.db is not present
    conn = sqlite3.connect("blogs.db")
    c = conn.cursor()
    if title==None:
        if request.method == "POST":
            t = request.form["title"]
            a = request.form["name"]
            e = request.form["entry"]
            q = '''SELECT MAX(id) FROM blogs'''
            maxID = c.execute(q).next()[0] #gets maxID in ID column to assign a new unique ID            
            if not (len(t) == 0 or len(a) == 0 or len(e) == 0):
                insert_post(t,a,e,str(maxID + 1))
                
        q = "SELECT title FROM blogs"
        result = c.execute(q)
        return render_template("index.html",titles=result)
    else:
        #get blog whose title matches the url
        t = title.replace("_"," ")
        q = '''SELECT title,name,entry,id FROM blogs 
        WHERE title = "%s"''' % t
        result = c.execute(q)
        r = result.next()

        #find all comments whose id corresponds to that of the blog
        q = '''SELECT name,comment FROM comments 
               WHERE id = %s''' % r[3]
        comments = c.execute(q)

        return render_template("post.html",text=r,comments=comments)

@app.route("/about")
def about():
        return render_template("about.html")

@app.route("/all")
def all():
    f = open("blogposts.csv")
    data = f.read()
    f.close()
    data = data.split("\n")
    final = []
    for n in data:
        placeholder = n.split(",")
        final.append(placeholder)
    final.remove(["title","name","entry","id"])
    return render_template("all.html",text = final)
               
if __name__=="__main__":
    # set the instance variable debug to True
    app.debug = True
    # call the run method
    app.run()
