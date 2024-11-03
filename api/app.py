from flask import Flask, render_template, request, jsonify, url_for, redirect
from threading import Lock, Thread
import time

app = Flask(__name__)

users = []
winner = None
winning_amount = None
lock = Lock()
amount = 1000.00
decrementing = False

@app.route('/', methods=["POST", "GET"])
def index():
    global users, decrementing
    if request.method == "POST":
        name = request.form.get("name")
        if name and name not in users:
            users.append(name)
            if not decrementing:
                decrementing = True
                Thread(target=decrement_amount).start()
        return render_template("bidding.html", name = name)
    return render_template("index.html")

@app.route('/bidding', methods=["POST"])
def bidding():
    global winner, winning_amount
    
    with lock:
        if not winner:
            winner = request.form.get("name")
            winning_amount = amount
    return jsonify({"winner": winner, "amount": winning_amount})

@app.route('/get_winner', methods = ["GET"])
def get_winner():
    return jsonify({"winner":winner})

@app.route('/winner')
def show_winner():
    global winner, winning_amount
    return render_template("winner.html", winner = winner, amount = winning_amount)

@app.route('/get_amount', methods = ["GET"])
def get_amount():
    global amount
    return jsonify({"amount": amount})
def decrement_amount():
    global amount
    while amount > 0:
        time.sleep(.005)
        with lock:
            amount = max(0, amount - .01)

if __name__ == "__main__":
    app.run(debug=True)
