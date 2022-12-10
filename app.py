import streamlit as st
import pandas as pd

st.set_page_config(initial_sidebar_state= "collapsed")

#---------------------Setting up data-----------------------------
@st.cache
def get_data():    
    df =  pd.read_csv("dataset\\for_app.csv")
    df.index = df.index + 1
    return df

df = get_data()
to_show = ["Calories", "Total Fat", "Cholesterol", "Sugars", "Protein", "Carbohydrate"]

#--------------------Streamlit page--------------------------------

with st.sidebar:
    no_of_rows = st.slider("Rows to display", min_value=1, max_value=1000, value=50)
    
    for col in df.columns:
        if col == "Food Item": continue
        if not st.checkbox(col, value=True if col in to_show else False):
            df = df.drop(columns=col)
            
    df = df.iloc[:no_of_rows]

st.dataframe(df)
# st.table(df)