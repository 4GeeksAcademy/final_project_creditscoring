import pandas as pd

df_cols = pd.read_csv("Data/raw/accepted_2007_to_2018Q4.csv", nrows=0)
list(df_cols.columns)

for col in df_cols.columns:
    print(col)



