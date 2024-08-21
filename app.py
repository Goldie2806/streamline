import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

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
    df = pd.read_csv('_select_make_model_round_avg_price_2_as_Price_condition_from_amp_202408211331.csv')
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
AgGrid(df_selection,fit_columns_on_grid_load=True)
st.text("Brought to you by Indy Amp Repair!")

hide_st_style = """
<style>
header {visibility: hidden;}
</style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)