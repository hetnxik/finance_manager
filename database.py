import os

import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.cursor import Cursor
from pymongo.results import DeleteResult, UpdateResult
from pymongo.typings import _DocumentType

load_dotenv(".env")

uri = f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@cluster0.cgvcyc3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

db = client["expenseTracker"]
users = db["users"]


def insert_user(username: str, name: str, phone: int, email: str, monthly_income: int, debt: int, expenses: list) -> object:
    data = {"username": username, username: {"name": name, "phone": phone, "email": email, "monthly_income": monthly_income, "debt": debt, "expenses": expenses}}
    return users.insert_one(data)


def fetch_all_users() -> Cursor[_DocumentType]:
    return users.find()


def get_user(username: str) -> _DocumentType:
    return users.find_one({"username": username})


def update_user(username: str, updates: dict) -> UpdateResult:
    users.update_one({"username": username}, {"$set": updates})


def delete_user(username: str) -> DeleteResult:
    return users.delete_one({"username": username})


def fetch_user_expenses(username: str) -> list[dict]:
    user: dict = users.find_one({"username": username})
    return user[username]["expenses"]


def expenses_to_df(username: str) -> pd.DataFrame:
    expenses: list = fetch_user_expenses(username)
    df = pd.DataFrame(expenses)
    return df


def add_expense(username: str, expense: dict) -> None:
    expenses = fetch_user_expenses(username )
    expenses.append(expense)
    update_user(username, updates={f"{username}.expenses": expenses})
    return None
