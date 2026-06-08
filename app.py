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
class Income(db.Model):
    id =db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    amount = db.Column(db.Float, nullable = False)
    date = db.Column(db.String(100), nullable = False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
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

@app.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
        return jsonify({"message": "Expense deleted successfully"}), 200
    return jsonify({"error": "Expense not found"}), 404

@app.route("/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    data = request.get_json()
    expense = Expense.query.get(expense_id)
    if expense:
        expense.name = data["name"]
        expense.amount = data["amount"]
        expense.category = data["category"]
        expense.date = data["date"]
        db.session.commit()
        return jsonify(expense.to_dict()), 200
    return jsonify({"error": "Expense not found"}), 404

@app.route("/dashboard/summary",methods=["GET"])
def dashboard_summary():
    expenses = Expense.query.all()
    incomes = Income.query.all()
    total_expenses = sum(e.amount for e in expenses)
    total_income = sum(i.amount for i in incomes)
    savings = total_income - total_expenses
    return jsonify({"total_expenses": total_expenses,
                    "total_income": total_income,
                    "savings":savings})

@app.route("/dashboard/recent_transactions", methods = ["GET"])
def recent_transactions():
    expenses = Expense.query.order_by(Expense.id.desc()).limit(5).all()
    return jsonify([e.to_dict() for e in expenses])
@app.route("/add_income", methods=["GET"])
def add_income():
    return render_template("add_income.html")

@app.route("/income", methods=["GET"])
def get_income():
    income = Income.query.order_by(Income.id.desc()).all()
    return jsonify([i.to_dict() for i in income])

@app.route("/income", methods=["POST"])
def add_incomes():
    data = request.get_json()
    income = Income(
        name=data["name"],
        amount=data["amount"],
        date=data["date"]
    )
    db.session.add(income)
    db.session.commit()
    return jsonify(income.to_dict()), 201
@app.route("/income/<int:income_id>", methods=["PUT"])
def edit_income(income_id):
    data = request.get_json()
    income = Income.query.get(income_id)
    if income:
        income.name = data["name"]
        income.amount = data["amount"]
        income.date = data["date"]
        db.session.commit()
        return jsonify(income.to_dict()), 200
    return jsonify({"error": "Income not found"}), 404
@app.route("/income/<int:id>", methods=["DELETE"])
def delete_income(id):
    income = Income.query.get(id)
    if income:
        db.session.delete(income)
        db.session.commit()
        return jsonify({"message":"income deleted"})
    return jsonify({"error":"error in deleting the expense"}),404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)