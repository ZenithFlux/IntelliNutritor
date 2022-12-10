import pandas as pd

def process_data(path):
    'Load dataset from csv and modify to be used in app'
    
    df = pd.read_csv(path)
    
    for col in df:
        if col == 'Food Item': continue
        for i in range(len(df[col])):
            if not df[col][i].replace(".", "").isnumeric(): continue
            df[col][i] = f"{df[col][i]} {df[col][0]}"
    
    df = df.drop(index=0)
    rename_dict = {}
    for col in df.columns:
        rename_dict[col] = col.replace("_", " ").title()
    rename_dict['item'] = "Food Item"
    
    df = df.rename(columns= rename_dict)
    return df

p = process_data("dataset\\to_analyze.csv")
p.to_csv("dataset\\for_app.csv", index=False)