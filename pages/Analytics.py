import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date
import plotly.express as px
from outlier import treat_outliers_z_score, treat_outliers_iqr

from plotly.subplots import make_subplots
import plotly.graph_objects as go


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


st.subheader('Treating "Age" outliers')
# Boxplots before outlier treatment
fig_before = px.box(data, y='Age', color_discrete_sequence=["#1D9BA1"])

# Treat outliers
data_treated = data.copy()
data_treated = treat_outliers_iqr(data_treated, 'Age')

# Boxplots after outlier treatment
fig_after = px.box(data_treated, y='Age', color_discrete_sequence=["#1D9BA1"])

# Create subplots to show side by side
fig_combined = make_subplots(rows=1, cols=2, subplot_titles=("Before Outlier Treatment", "After Outlier Treatment"))

# Add traces
fig_combined.add_trace(go.Box(y=data['Age'], name='Before', marker_color='#1D9BA1'), row=1, col=1)
fig_combined.add_trace(go.Box(y=data_treated['Age'], name='After', marker_color='#1D9BA1'), row=1, col=2)

# Update layout
fig_combined.update_layout(showlegend=False)

# Display combined plot in Streamlit
st.plotly_chart(fig_combined)

week = pd.DataFrame(data.app_weekday.value_counts()).reset_index()

day_order = {
    0:'Monday', 1: 'Tuesday', 2:'Wednesday', 3:'Thursday',
    4:'Friday', 5:'Saturday', 6:'Sunday'
}
week['day_num'] = week['app_weekday'].map(day_order)
week_sorted = week.sort_values('app_weekday')

# Create a Plotly line chart
fig = px.line(week_sorted, x='day_num', y='count')

# Customize the line chart
fig.update_traces(mode='lines+markers', marker=dict(size=10, color='#1D9BA1'))
fig.update_layout(xaxis_title='Day of the Week', yaxis_title='Value')

# Display in Streamlit
st.subheader('Appointments by Day of the Week')
st.plotly_chart(fig)

st.subheader("Model Building and Predictions")

