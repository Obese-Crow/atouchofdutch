from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

@app.route('/')
def home():
    return 'meme!'

@app.route('/about')
def about():
    return 'About'
