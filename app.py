# Albert, Alex, Justin, and Leslie
# Soft Dev Pd 7
# Database Project

from flask import Flask, render_template, request
import sqlite3
#import utils

# app is an instance of the Flask class
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
@app.route("/<title>")
def home(title=None):
        conn = sqlite3.connect("blogs.db")
        c = conn.cursor()
        if title==None:
                q = "SELECT title FROM blogs"
                result = c.execute(q)
                return render_template("index.html",titles=result)

if __name__=="__main__":
    # set the instance variable debug to True
    app.debug = True
    # call the run method
    app.run()
