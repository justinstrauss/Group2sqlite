# Albert, Alex, Justin, and Leslie
# Soft Dev Pd 7
# Database Project

from flask import Flask, render_template, request
import sqlite3
import populate
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
                
@app.route("/post")
@app.route("/1")
@app.route("/2")
def post():
    f = open("blogposts.csv")
    data = f.split("\n")
    f.close()
    for n in data:
        number = 1
        return render_template("post.html",text = data[number])

@app.route("/all")
def all():
    f = open("blogposts.csv")
    data = f.read().split("\n")
    f.close()
    return render_template("all.html",text = data)

    
if __name__=="__main__":
    # set the instance variable debug to True
    app.debug = True
    # call the run method
    app.run()
