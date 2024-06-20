import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date
import plotly.express as px


st.set_page_config(page_title="Healthcare Analytics", page_icon=None, initial_sidebar_state="collapsed", menu_items=None, )

with open( "files/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    st.sidebar.markdown(f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.title('Exploratory Data Analysis')
# Inject custom HTML for the positioned text
data = pd.read_csv('noshowappointments-kagglev2-may-2016.csv')

data['ScheduledDay'] = pd.to_datetime(data['ScheduledDay']).dt.date.astype('datetime64[ns]')
data['AppointmentDay'] = pd.to_datetime(data['AppointmentDay']).dt.date.astype('datetime64[ns]')

data['sch_weekday'] =  data['ScheduledDay'].dt.dayofweek
data['app_weekday'] =  data['AppointmentDay'].dt.dayofweek

data=data.drop(['PatientId','AppointmentID','Neighbourhood'],axis=1)

data=data.rename(columns={'Hipertension':'Hypertension','Handcap':'Handicap','SMS_received':'SMSreceived','No-show':'Noshow'})
# gender = df['gender'].value_counts()
# # Convert to DataFrame and reset index
# gender = gender.reset_index()

# # Rename columns
# gender.columns = ['Gender', 'Count']
# fig = px.pie(gender, names='Gender', values='Count', hole=.4)
# st.plotly_chart(fig)
# st.dataframe(data)

st.markdown('<b>Summary statistics of numerical data</b>', unsafe_allow_html=True)
st.write(data[['Age', 'Scholarship', 'Hypertension',
       'Diabetes', 'Alcoholism', 'Handicap']].describe())

# Get the value counts of the 'Noshow' column
noshow_counts = data['Noshow'].value_counts()

# Create a pie chart using Plotly
fig = px.pie(noshow_counts, 
                        values=noshow_counts.values, 
                        names=noshow_counts.index, 
                        title='Appointment Noshow Distribution',
                        color=noshow_counts.index,
                        color_discrete_map={'Yes': '#1D9BA1', 'No': '#A8ECEF'},
                        hole=.6)

# Display the pie chart in Streamlit
st.plotly_chart(fig)


# Histograms
st.subheader('Histograms')
for column in data[['Age']]:
    fig = px.histogram(data, x=column, title=f'Histogram of {column}', color_discrete_sequence=["#1D9BA1"])
    st.plotly_chart(fig)

# Boxplots
st.subheader('Boxplots')
for column in data[['Age']]:
    fig = px.box(data, y=column, title=f'Boxplot of {column}', color_discrete_sequence=["#1D9BA1"])
    st.plotly_chart(fig)