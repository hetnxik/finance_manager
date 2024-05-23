import database as db
from datetime import date

# db.insert_user(username="awesomehet", name="het", phone="0123456789", email="het@example.com", monthly_income=10000,
#                debt=0, expenses=[{"date": date.today().strftime("%m/%y"), "amount": 100, "description": "bleh"}])
username = "awesomehet"

""" updating user """
db.update_user(username=username, updates={f"{username}.expenses": [{"amount": 100, "description": "food", "month": date.today().month, "year": date.today().year}, {"amount": 200, "description": "petrol", "month": date.today().month, "year": date.today().year}]})
# {"expenses": [{"date": date.today().strftime("%m/%y"), "amount": 100, "description": "food"}, {"date": date.today().strftime("%m/%y"), "amount": 200, "description": "petrol"}]}
# expenses = db.fetch_user_expenses(username="awesomehet")
# print(expenses)

""" fetching data and storing to csv """
# db.expenses_to_csv(username)
