from flask import Flask, render_template, request, jsonify, url_for, redirect
import redis

redis_host = 'redis-12113.c1.us-central1-2.gce.redns.redis-cloud.com'
redis_port = 12113
redis_password = 'sTWC4aYkDgT78hA0VSoK7WAdbyrt67Q6'

client = redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    decode_responses=True
)

app = Flask(__name__)

@app.route('/reset', methods=["POST"])
def reset():
    client.set('amount', 1000.00)
    client.delete('users')
    client.delete('winner')
    client.delete('gameOver')
    return redirect(url_for('index'))

@app.route('/', methods=["POST", "GET"])
def index():
    if client.get('gameOver') == 'True':
        return redirect(url_for('loser'))
    if request.method == "POST":
        name = request.form.get("name")
        if name and not client.sismember('users', name):
            client.sadd('users', name)
            if client.get('decrementing') is None:
                client.set('decrementing', 'True')
        return render_template("bidding.html", name=name)
    return render_template("index.html")

@app.route('/bidding', methods=["POST"])
def bidding():
    if not client.get('winner'):
        winner = request.form.get("name")
        client.set('winner', winner)
        winning_amount = client.get('amount')
        return jsonify({"winner": winner, "amount": winning_amount})

@app.route('/get_winner', methods=["GET"])
def get_winner():
    winner = client.get('winner')
    return jsonify({"winner": winner})

@app.route('/winner')
def show_winner():
    winner = client.get('winner')
    amount = client.get('amount')
    return render_template("winner.html", winner=winner, amount=float(amount))

@app.route('/loser')
def loser():
    return render_template("loser.html")

@app.route('/get_amount', methods=["GET"])
def get_amount():
    amount = client.get('amount')
    if amount is not None:
        return jsonify({"amount": float(amount)})
    return jsonify({"amount": 0.0})

@app.route('/decrement', methods=["POST"])
def decrement():
    current_amount = float(client.get('amount'))
    if current_amount > 0:
        new_amount = max(0, current_amount - 1.50)
        client.set('amount', new_amount)
        client.set('gameOver', str(new_amount <= 0))
    return jsonify({"amount": float(client.get('amount'))})

if __name__ == "__main__":
    app.run(debug=True)
