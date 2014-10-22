# Albert, Alex, Justin, and Leslie
# Soft Dev Pd 7
# Database Project

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import populate
import os.path
from time import strftime

# app is an instance of the Flask class
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
@app.route("/<title>",methods=["GET","POST"])
def home(title=None):
    if not os.path.isfile("blogs.db"):
        populate.setup()
    #run populate.py only if blogs.db is not present
    conn = sqlite3.connect("blogs.db")
    c = conn.cursor()
    if title==None:
        error = False;
        if request.method == "POST":
            t = request.form["title"]
            a = request.form["name"]
            e = request.form["entry"]
            q = '''SELECT MAX(id) FROM blogs'''
            maxID = c.execute(q).next()[0] #gets maxID in ID column to assign 
                                           #a new unique ID
            q = '''SELECT title FROM blogs'''
            titleCheck = c.execute(q)
            titleCheck = [w[0] for w in titleCheck]
            if not (len(t) == 0 or len(a) == 0 or len(e) == 0):
                if t in titleCheck:
                    error = True
                else:
                    clock = str(strftime("%I:%M:%S %m/%d/%Y"))
                    print clock
                    populate.insert_post(t,a,e,str(maxID + 1),clock)
                
        q = "SELECT title FROM blogs"
        result = c.execute(q)
        result = [o for o in result][::-1]
        return render_template("index.html",titles=result,haserror=error)
    else:
        #get blog whose title matches the url
        t = title.replace("_"," ")
        q = '''SELECT title,name,entry,id,time FROM blogs 
        WHERE title = "%s"''' % t
        result = c.execute(q)
        try:
            r = result.next()
        except StopIteration:
            return redirect(url_for('home'))

        if request.method == "POST":
            n = request.form["name"]
            e = request.form["comment"]
            if not (len(n) == 0 or len(e) == 0):
                populate.insert_comment(n,e,r[3])
                                        
        #find all comments whose id corresponds to that of the blog
        q = '''SELECT name,comment FROM comments 
               WHERE id = %s''' % r[3]
        print "q " + q
        comments = c.execute(q)
        
        return render_template("post.html",text=r,comments=comments)

@app.route("/about")
def about():
        return render_template("about.html")

@app.route("/all")
def all():
    conn = sqlite3.connect("blogs.db")
    q = '''SELECT title, name, entry,id FROM blogs'''
    posts = c.execute(q)
    b = '''SELECT name, comment FROM comments'''
    comments = c.execute(q)
    return render_template("all.html", comments=comments, posts=posts) 
#Albert don't work all, Leslie is

# @app.route("/all")
# def all():
#     f = open("blogposts.csv")
#     data = f.read()
#     f.close()
#     data = data.split("\n")
#     final = []
#     for n in data:
#         placeholder = n.split(",")
#         final.append(placeholder)
#     final.remove(["title","name","entry","id"])
#     final.remove(["","","",""])
#     return render_template("all.html",text = final)
               
if __name__=="__main__":
    # set the instance variable debug to True
    app.debug = True
    # call the run method
    app.run()
