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
        f = open("blogposts.csv")
        data = f.split("\n")
        f.close()
        if not os.path.isfile("blogs.db"):
                populate.setup()
        #run populate.py only if blogs.db is not present
        conn = sqlite3.connect("blogs.db")
        c = conn.cursor()
        if title==None:
                q = "SELECT title FROM blogs"
                result = c.execute(q)
                return render_template("index.html",titles=result,range = range(data.len()))
        else:
                t = title.replace("_"," ")
                q = '''SELECT title,entry,id FROM blogs
                       WHERE title = ''' + t
                result = c.execute(q)
                return render_template("blog.html",blogs=result)


                
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


if __name__=="__main__":
    # set the instance variable debug to True
    app.debug = True
    # call the run method
    app.run()
