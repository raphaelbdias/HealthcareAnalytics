import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Healthcare Analytics", page_icon=None, initial_sidebar_state="auto", menu_items=None)

with open( "files/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    st.sidebar.markdown(f'<style>{css.read()}</style>' , unsafe_allow_html= True)

# Inject custom HTML for the positioned text
df = pd.read_csv('maindata.csv')

gender = df['gender'].value_counts()
# Convert to DataFrame and reset index
gender = gender.reset_index()

# Rename columns
gender.columns = ['Gender', 'Count']
fig = px.pie(gender, names='Gender', values='Count', hole=.4)
st.plotly_chart(fig)
st.dataframe(df)