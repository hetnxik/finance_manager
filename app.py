import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px
import database as db

import yaml
from yaml.loader import SafeLoader

# Page config
st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

authenticator.login()
try:
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
except Exception as e:
    print(e)

name = st.session_state["name"]
username = st.session_state["username"]

# Page designing
if st.session_state["authentication_status"]:

    # Home page
    authenticator.logout(location="sidebar")
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Expenses')

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

    # Main Page
    st.sidebar.title(f"Welcome {name}")

    df = db.expenses_to_df(username)

    pie_chart = px.pie(df, values='amount', names='description', labels='description', hole=0.3)
    pie_chart.update_traces(textinfo="label+value")

    month = st.number_input("Select the Month:", placeholder="Month", step=1, min_value=1, max_value=12)
    year = st.number_input("Select the Year:", placeholder="Month", step=1, min_value=1)

    if st.button("Plot"):
        temp_df = df[(df['month'] == month) & (df['year'] == year)]
        pie_chart = px.pie(temp_df, values='amount', names='description', labels='description', hole=0.3)
        pie_chart.update_traces(textinfo="label+value")

        st.plotly_chart(pie_chart, use_container_width=True)

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
