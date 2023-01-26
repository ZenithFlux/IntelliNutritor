import streamlit as st
import pandas as pd

#---------------------Setting up data-----------------------------
@st.cache
def get_data():    
    df =  pd.read_csv("dataset\\for_app.csv")
    df.index = df.index + 1
    return df

df = get_data()
to_show = ["Calories", "Total Fat", "Cholesterol", "Sugars", "Protein", "Carbohydrate"]

if "fil_cols" not in st.session_state:
    st.session_state["fil_cols"] = []
    st.session_state["fil_range"] = []

#--------------------Streamlit page--------------------------------

with st.sidebar:
    st.title("Choose your diet!")
    
    filter_tab, cols_tab = st.tabs(["Filters", "Columns"])
    
    with filter_tab:
        fil_cols = st.session_state["fil_cols"]
        fil_range = st.session_state["fil_range"]
        
        no_of_rows = st.number_input("Max Rows to display", min_value=1, 
                                     max_value=len(df), value=50, step=1)
        search_text = st.text_input("Search food items by name", placeholder="Food name")
        
        st.header("Add Filters:")
        fil_nut = st.selectbox("Select Nutrient", 
                               df.columns[~df.columns.isin(fil_cols)])
        cols = st.columns(2)
        with cols[0]:
            # min_value = st.number_input("Min", )
            pass
            
        if st.button("\\+ Add Filter", type="primary") and fil_nut != "Food Item":
            fil_cols.append(fil_nut)
            fil_range.append([0, 10000])
                
        for i in range(len(fil_cols)):
            pass
        
        st.write(fil_cols) ##########
        
    with cols_tab:
        for col in df.columns:
            if col == "Food Item": continue
            if not st.checkbox(col, value=True if col in to_show else False):
                df = df.drop(columns=col)


if search_text:
    search_text = search_text.lower().strip()
    df = df[df["Food Item"].str.lower().str.contains(search_text)]
df = df.iloc[:no_of_rows]
df = df.reset_index(drop=True)
df.index = df.index + 1
st.table(df)