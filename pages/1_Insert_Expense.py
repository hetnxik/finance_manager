import streamlit as st
import streamlit_authenticator as stauth
import database as db

from datetime import date

import yaml
from yaml.loader import SafeLoader

st.set_page_config(page_title="Insertion", page_icon=":bar_chart:", layout="wide")

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

name = st.session_state["name"]
username = st.session_state["username"]

if st.session_state["authentication_status"]:

    # Home page
    authenticator.logout(location="sidebar")
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')

    # Reset password
    try:
        if authenticator.reset_password(username=st.session_state["username"], location="sidebar"):
            try:
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
            except Exception as e:
                print(e)
            st.success('Password modified successfully')
    except Exception as e:
        st.error(e)

    # Update User
    try:
        if authenticator.update_user_details(username=st.session_state["username"], location="sidebar"):
            try:
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
            except Exception as e:
                print(e)
            st.success('Entries updated successfully')
    except Exception as e:
        st.error(e)

    # Page Design

    amount = st.number_input("Insert amount:", placeholder="Enter your expense", step=1)
    st.write(f"{amount}")

    category = st.selectbox("Insert a category:", options=("Food", "Petrol", "Entertainment", "Clothing"))
    st.write(f"{category}")

    if st.button("Log"):
        expense = {"amount": amount, "description": category, "month": date.today().month,
                   "year": date.today().year}
        db.add_expense(username=username, expense=expense)
        st.write(f"added {expense['amount']} in {expense['description']} to database")
