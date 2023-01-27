import streamlit as st
import pandas as pd

st.set_page_config(page_title="IntelliNutritor", page_icon="icon.png", layout="wide")

# This makes page look better, but it is unsafe
# st.markdown('''<style>
#             header {visibility: hidden;}
#             footer {visibility: hidden;}
#             .css-1vq4p4l.e1fqkh3o4 {margin-top: -75px;}''', unsafe_allow_html=True)

#---------------------Setting up data-----------------------------
@st.cache
def get_data(str_data: str, num_data: str):    
    df =  pd.read_csv(str_data)
    df_num = pd.read_csv(num_data)
    df_num = df_num.drop(index=0, columns="Food Item").astype(float)
    df_num = df_num.reset_index(drop=True)
    return df, df_num

df, df_num = get_data("data\\for_app.csv", "data\\to_analyze.csv")
to_show = ["Calories", "Total Fat", "Cholesterol", "Sugars", "Fiber", "Protein", "Carbohydrate"]

if "fil_cols" not in st.session_state:
    st.session_state["fil_cols"] = []
    st.session_state["col_ranges"] = []

#--------------------Streamlit page--------------------------------

col = st.columns([3,1,1])

with col[0]:
    st.markdown("# IntelliNutritor 🥗")
    st.markdown("🌮 Plan your diet intelligently 🍉☕")
    st.markdown("Use the filters provided on the sidebar to find food items just right for you!")
    st.markdown("##### Note:- Measurements are per 100g")
    
with col[2]:
    st.image("icon.png", width=200)

with st.sidebar:
    st.title("Choose your diet!")
    
    filter_tab, cols_tab = st.tabs(["Filters", "Show Columns"])
    
    with filter_tab:
        fil_cols = st.session_state["fil_cols"]
        col_ranges = st.session_state["col_ranges"]
        
        no_of_rows = st.number_input("Max Rows to display", min_value=1, 
                                     max_value=len(df), value=50, step=1)
        search_text = st.text_input("Search food items by name", placeholder="Food name")
        
        st.header("Add Filters")
        
        default = "Nutrient List"
        nt_list = df.columns.to_series()
        nt_list[0] = default
        fil_nut = st.selectbox("Select Nutrient", nt_list)
        
        cols = st.columns(2)
        with cols[0]:
            min_value = st.number_input("Min", min_value=0., max_value=100_000., step=0.01)
        with cols[1]:
            max_value = st.number_input("Max", min_value=0., max_value=100_000., step=0.01)
            
        if st.button("\\+ Add/Modify Filter", type="primary"):
            if fil_nut not in [default]+fil_cols and min_value<=max_value:
                fil_cols.append(fil_nut)
                col_ranges.append([min_value, max_value])
                
            elif min_value > max_value:
                st.warning("Min should be less than Max")
            
            elif fil_nut in fil_cols:
                col_ranges[fil_cols.index(fil_nut)] = [min_value, max_value]
                
        for i in range(len(fil_cols)):
            if i >= len(fil_cols): break
            rem_key = f"remove_{i}"
            if rem_key in st.session_state and st.session_state[rem_key]:
                del fil_cols[i]
                del col_ranges[i]
                del st.session_state[rem_key]
        
        for i in range(len(fil_cols)):
            cols = st.columns([3,1])
            cols[0].subheader(fil_cols[i])
            cols[1].button(chr(10006), key=f"remove_{i}")                
            
            cols = st.columns(2)
            cols[0].caption(f"**Min:** {col_ranges[i][0]:.2f}")
            cols[1].caption(f"**Max:** {col_ranges[i][1]:.2f}")
        
    with cols_tab:
        for col in df.columns:
            if col == "Food Item": continue
            if not st.checkbox(col, value=True if col in to_show else False):
                df = df.drop(columns=col)

for col, [min, max] in zip(fil_cols, col_ranges):
    cond = (df_num[col] >= min) & (df_num[col] <= max)
    df = df[cond]
    df_num = df_num[cond]

if search_text:
    search_text = search_text.lower().strip()
    df = df[df["Food Item"].str.lower().str.contains(search_text)]
df = df.iloc[:no_of_rows]
df = df.reset_index(drop=True)
df.index = df.index + 1
st.table(df)