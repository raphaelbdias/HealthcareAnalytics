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


st.set_page_config(page_title="Healthcare Analytics", page_icon=":hospital:", initial_sidebar_state="collapsed", menu_items=None, layout='wide')

# Add CSS styles for the containers
container_style = """
    <style>
        .container1 {
            border: 2px solid #3498db;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 20px;
        }
        .container2 {
            /* Add styles for Container 2 if needed */
        }
    </style>
"""

# Display the CSS styles
st.markdown(container_style, unsafe_allow_html=True)

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
# Treat outliers
data_treated = data.copy()
data_treated = treat_outliers_iqr(data_treated, 'Age')


col1, col2 = st.columns([2,1], gap='medium')

with col1:
    st.subheader('Summary statistics', divider='gray')
    subcol1, subcol2 = st.columns([1,1])
    with subcol1:
        st.markdown('<b>Summary statistics of numerical data</b>', unsafe_allow_html=True)


        st.write(data[['Age', 'Hypertension',
            'Diabetes', 'Alcoholism', 'Handicap']].describe())
        
        with st.container(border=True):
            week = pd.DataFrame(data_treated.app_weekday.value_counts()).reset_index()

            day_order = {
                0:'Monday', 1: 'Tuesday', 2:'Wednesday', 3:'Thursday',
                4:'Friday', 5:'Saturday', 6:'Sunday'
            }
            week['day_num'] = week['app_weekday'].map(day_order)
            week_sorted = week.sort_values('app_weekday')

            # Create a Plotly line chart
            fig = px.line(week_sorted, x='day_num', y='count', title='Appointments by Day of the Week')

            # Customize the line chart
            fig.update_traces(mode='lines+markers', marker=dict(size=10, color='#1D9BA1'))
            fig.update_layout(xaxis_title='Day of the Week', yaxis_title='Value')

            # Display in Streamlit
            st.plotly_chart(fig)
        # Histograms

        with st.container(border=True):
            for column in data[['Age']]:
                fig = px.histogram(data, x=column, title=f'{column} Distribution', color_discrete_sequence=["#1D9BA1"])
                st.plotly_chart(fig)

        
        
    with subcol2:   
        with st.container(border=True):
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

        with st.container(border=True):
            gender_counts = data['Gender'].value_counts()

            # Create a pie chart using Plotly
            fig = px.bar(gender_counts, 
                                    title='Appointment gender Distribution',
                                    color=gender_counts.index,
                                    color_discrete_map={'M': '#1D9BA1', 'F': '#A8ECEF'},)
            st.plotly_chart(fig)

        with st.container(border=True):
            # Boxplots before outlier treatment
            fig_before = px.box(data, y='Age', color_discrete_sequence=["#1D9BA1"])

            # Boxplots after outlier treatment
            fig_after = px.box(data_treated, y='Age', color_discrete_sequence=["#1D9BA1"])

            # Create subplots to show side by0 side
            fig_combined = make_subplots(rows=1, cols=2, subplot_titles=("Before Outlier Treatment", "After Outlier Treatment"))

            # Add traces
            fig_combined.add_trace(go.Box(y=data['Age'], name='Before', marker_color='#1D9BA1'), row=1, col=1)
            fig_combined.add_trace(go.Box(y=data_treated['Age'], name='After', marker_color='#1D9BA1'), row=1, col=2)

            # Update layout
            fig_combined.update_layout(showlegend=False, title='Detecting and Treating Outliers in Age',)

            # Display combined plot in Streamlit
            st.plotly_chart(fig_combined)




with col2:
    st.subheader('Model Building', divider='gray')
    with st.container(border=True):
        data_treated['no_show'] = data_treated['Noshow'].apply(lambda x: 1 if x == 'Yes' else 0)

        # Compute correlation matrix
        corr_matrix = data_treated[['no_show','Age', 'Scholarship', 'Hypertension',
            'Diabetes', 'Alcoholism', 'Handicap', 'app_weekday']].corr()

        # Create a Plotly Heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale=[[0.0, '#FFFFFF'], [1.0, '#1D9BA1']],
            colorbar=dict(title='Correlation'),
            text=corr_matrix.values,
            hoverinfo='text'
        ))

        fig.update_layout(
            title='Correlation Heatmap',
            xaxis_title='Features',
            yaxis_title='Features',
            height=600,
            width=800
        )

        st.plotly_chart(fig)
