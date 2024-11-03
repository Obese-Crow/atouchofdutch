from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import join_room, SocketIO
from flask_cors import CORS

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"

CORS(app)
socketio = SocketIO(app)

@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        session["name"] = name
        return redirect(url_for("bidding"))
    return render_template("index.html")

@app.route('/bidding', methods=["POST", "GET"])
def bidding():
    if request.method == "POST":
        winner_name = session.get("name")
        socketio.emit("winner", {"name": winner_name}, room="restaurant")  # Emit winner
        return redirect(url_for("winner", name=winner_name))
    name = session.get("name")
    return render_template("bidding.html", name=name)

@app.route('/winner/<name>')
def winner(name):
    return " " + name + " Wins!"

@socketio.on("connect")
def connect(auth):
    join_room("restaurant")

if __name__ == "__main__":
    socketio.run(app)
