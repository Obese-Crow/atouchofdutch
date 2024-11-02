from flask import Flask, render_template
#import requests
#import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")
@app.route('/about')
def about():
    return 'About'
#test
