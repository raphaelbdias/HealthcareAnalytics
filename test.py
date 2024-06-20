import pandas as pd

df = pd.read_csv('dataHospital.csv')
cols = df.columns[1:17].to_list()
df[cols].to_csv('maindata.csv')