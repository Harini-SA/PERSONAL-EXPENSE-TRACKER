from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/budget")
def budget():
    return render_template("budget.html")

@app.route("/add_expense")
def add_expense():
    return render_template("add_expense.html")

@app.route("/goals")
def goals():
    return render_template("goals.html")

if __name__ == "__main__":
    app.run(debug = True)