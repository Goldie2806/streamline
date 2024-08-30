import streamlit as st
import pandas as pd
import json
import os


st.set_page_config(
    layout="centered",
    page_title="What's the lowest?",
    page_icon=":moneybag:"
)
st.title("For The Car Audio Enthusiast")
st.markdown("""This tool was created to provide current market pricing on car audio equipment. 
            Currently, we're in beta mode with data being added daily and more features coming shortly.
            To get started follow the prompts on the left.""") 



#caching data instead of reloading on each filter call
@st.cache_data
def getdata():
    df = pd.read_csv('amps.csv')
    return df
df = getdata()


# sidebar
st.sidebar.header("Which amp are you looking for?")
make_model = st.sidebar.multiselect(
    "Select Make & Model:",
    options=df["make_model"].unique()
)

df_selection = df.query(
    "make_model == @make_model"
)

"---"
st.table(df_selection)
st.text("Brought to you by Indy Amp Repair!")

"---"
st.title("Have you recently sold an Amp?")
st.markdown("""Please fill out the form below as this data will give other users like yourself a better idea how much an amp is worth.""") 
with st.form(key = 'User_Submit'):
    make = st.text_input("What make was the amp?", "", placeholder = "Ex. Kicker")
    model = st.text_input("What model was the amp?", "",placeholder = "Ex. XS50")
    number = st.number_input("How much did you sell the amp for?")
    option = st.selectbox(
        "What condition was the amp in?",
        ("New", "Pre-Owned", "Parts Only"),
    )
    date = st.date_input("When did you sell this amp?")
    submit_button = st.form_submit_button()
dt_str = date.strftime("%Y-%m-%d")
str_date = json.dumps(dt_str)
if submit_button:
    response = (
    supabase.table("ampdata")
    .insert({"make":make, "model":model, "price":number, "condition":option, "sold_date":str_date})
    .execute()
)

hide_st_style = """
<style>
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)
