from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "expenses.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "category": self.category,
            "date": self.date}

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
def add_expenses():
    return render_template("add_expense.html")

@app.route("/goals")
def goals():
    return render_template("goals.html")

@app.route("/expenses", methods=["GET"])
def get_expense():
    expense = Expense.query.order_by(Expense.id.desc()).all()
    return jsonify([e.to_dict() for e in expense])

@app.route("/expenses", methods=["POST"])
def add_expense():
    data = request.get_json()
    expense = Expense(
        name=data["name"],
        amount=data["amount"],
        category=data["category"],
        date=data["date"]
    )
    db.session.add(expense)
    db.session.commit()
    return jsonify(expense.to_dict()), 201

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)