from flask import Flask, render_template, request, redirect, url_for
#import requests
#import json

app = Flask(__name__)

@app.route('/',methods = ["POST","GET"])
def home():
    if request.method == "POST":
        return redirect(url_for("bidding"))
    return render_template("index.html")
@app.route('/bidding')
def bidding():
    return render_template("bidding.html")
#test
##
