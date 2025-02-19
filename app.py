from flask import Flask, render_template, request, redirect, url_for
import hashlib
import datetime

app = Flask(__name__)

# Blockchain class
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(f"{self.index}{self.timestamp}{self.data}{self.previous_hash}".encode())
        return sha.hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, str(datetime.datetime.now()), "Genesis Block", "0")

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(
            len(self.chain), 
            str(datetime.datetime.now()), 
            data, 
            previous_block.hash
        )
        self.chain.append(new_block)


# Initialize Blockchain
blockchain = Blockchain()

# Routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/vote", methods=["GET", "POST"])
def vote():
    if request.method == "POST":
        voter_id = request.form.get("voter_id")
        candidate = request.form.get("candidate")

        # Add the vote to the blockchain
        data = f"Voter ID: {voter_id}, Candidate: {candidate}"
        blockchain.add_block(data)

        return redirect(url_for("chain"))
    return render_template("vote.html")


@app.route("/chain")
def chain():
    return render_template("chain.html", blockchain=blockchain)


if __name__ == "__main__":
    app.run(debug=True)
