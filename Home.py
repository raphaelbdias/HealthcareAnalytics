import streamlit as st


st.set_page_config(page_title="Healthcare Analytics", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)


with open( "files/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    st.sidebar.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)



# Inject custom HTML for the positioned text
custom_text_html = """
<div class="title-text">Technical Interview Round:</div>
<div class="subtitle-text">Decision Support Analyst at Health<br>Science North</div>
<div class="datetitle-text"><br><br><br>June 2024</div>
"""
st.markdown(custom_text_html, unsafe_allow_html=True)

with open('files/wave.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)