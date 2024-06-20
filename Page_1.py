import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Healthcare Analytics", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

with open( "files/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    st.sidebar.markdown(f'<style>{css.read()}</style>' , unsafe_allow_html= True)

# Inject custom HTML for the positioned text
df = pd.read_csv('maindata.csv')

page1title = """
    <div class="page1title-text">Summary Statistics of Patient Records</div>
"""
st.markdown(page1title, unsafe_allow_html=True)

mcol1, mcol2 = st.columns([1,1])

with mcol1:
    with st.container():
        col1, col2 = st.columns([2,1])

        with col1: 
            arrival_counts = df['arrivalhour_bin'].value_counts()
            # Convert to DataFrame and reset index
            arrival_counts = arrival_counts.reset_index()

            # Rename columns
            arrival_counts.columns = ['Arrival Hour', 'Count']
            # print(arrival_counts)
            with st.container():
                custom_text_html = """
                <div class="charttitle-text">Peak Visiting Hours</div>
                """
                st.markdown(custom_text_html, unsafe_allow_html=True)
                st.line_chart(arrival_counts, x='Arrival Hour', y='Count',color="#1D9BA1")

        with col2:
            gender = df['gender'].value_counts()
            # Convert to DataFrame and reset index
            gender = gender.reset_index()
            

            # Rename columns
            gender.columns = ['Gender', 'Count']
            print(gender)
            with st.container():
                fig = px.pie(gender, names='Gender', values='Count', hole=.4,
                             color=gender.Gender,
                            color_discrete_map={'Male': '#1D9BA1', 'Female': '#A8ECEF'})
                st.plotly_chart(fig)