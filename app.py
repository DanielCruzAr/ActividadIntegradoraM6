from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from bokeh.plotting import figure

st.set_page_config(layout="centered")
#=====================================DATA=====================================#
    
df = pd.read_csv('Police_Incidents.csv')


mapa = pd.DataFrame()
mapa['Date'] = df['Incident Date']
mapa['Day'] = df['Incident Day of Week']
mapa['District'] = df['Police District']
mapa['Neighbourhood'] = df['Analysis Neighborhood']
mapa['Incident Category'] = df['Incident Category']
mapa['Incident Subcategory'] = df['Incident Subcategory']
mapa['Resolution'] = df['Resolution']
mapa['lat'] = df['Latitude']
mapa['lon'] = df['Longitude']
mapa = mapa.dropna()

def main():
    st.title('Police incident reports from 2018 to 2020 in San Francisco')
    st.markdown('The data shown below belongs to incident reports in the City of San Francisco, from the year 2018 to 2020, woth details from each case such as date, day of the week, police district, neighbourhood in which it happened, type of incident in category and subcategory, exact location and resolution')

    #=====================================SIDEBAR=====================================#

    st.sidebar.title('Filter Options')

    subset_data4 = mapa
    resolution_input = st.sidebar.multiselect('Resolution',
                                            mapa.groupby('Resolution').count().reset_index()['Resolution'].tolist())
    if len(resolution_input) > 0:
        subset_data4 = mapa[mapa['Resolution'].isin(resolution_input)]
    
    subset_data3 = subset_data4
    incident_input = st.sidebar.multiselect('Incident Category',
                                            subset_data4.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())
    if len(incident_input) > 0:
        subset_data3 = subset_data4[subset_data4['Incident Category'].isin(incident_input)]

    subset_data2 = subset_data3
    incident_sub_input = st.sidebar.multiselect('Incident Subcategory',
                                            subset_data3.groupby('Incident Subcategory').count().reset_index()['Incident Subcategory'].tolist())
    if len(incident_sub_input) > 0:
        subset_data2 = subset_data3[subset_data3['Incident Subcategory'].isin(incident_sub_input)]
    
    subset_data1 = subset_data2
    police_district_input = st.sidebar.multiselect('Police District',
                                            subset_data2.groupby('District').count().reset_index()['District'].tolist())
    if len(police_district_input) > 0:
        subset_data1 = subset_data2[subset_data2['District'].isin(police_district_input)]

    subset_data = subset_data1
    neighbourhood_input = st.sidebar.multiselect('Neighbourhood',
                                            subset_data1.groupby('Neighbourhood').count().reset_index()['Neighbourhood'].tolist())
    if len(neighbourhood_input) > 0:
        subset_data = subset_data1[subset_data1['Neighbourhood'].isin(neighbourhood_input)]

    subset_data    

    #=====================================DATA VISUALIZATION=====================================#

    c1, c2, c3 = st.columns(3)
    c1.warning("Total crimes reported: " + str(subset_data.shape[0]))
    c2.warning("Total crimes closed or solved: " + str(subset_data[subset_data['Resolution'] != 'Open or Active'].shape[0]))
    c3.warning("Total crimes open or active: " + str(subset_data[subset_data['Resolution'] == 'Open or Active'].shape[0]))

    st.markdown('Crimes resolution')
    labels = subset_data['Resolution'].unique()
    values = subset_data['Resolution'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    st.plotly_chart(fig)

    if subset_data['Incident Category'].nunique() > 1:
        st.markdown('Crime categories')
        fig1 = go.Figure(data=[go.Bar(
            x=subset_data['Incident Category'].value_counts(),
            y=subset_data['Incident Category'].unique(),
            orientation='h',
        )])
        st.plotly_chart(fig1)

    subcat = st.toggle('Click to see incident subcategories')
    if subcat:
        st.markdown('Subtype of crimes committed')
        fig2 = go.Figure(data=[go.Bar(
            x=subset_data['Incident Subcategory'].value_counts(),
            y=subset_data['Incident Subcategory'].unique(),
            orientation='h',
        )])
        st.plotly_chart(fig2)

    st.markdown('It is important to mention that any police district can answer to any incident, the neighbourhood in which it happened is not related to the police district')
    st.markdown('Crime locations in San Francisco')
    st.map(subset_data, color=(.1,.3,.6,.5))

    st.markdown('Districts with the most crimes')
    st.bar_chart(subset_data['District'].value_counts())

    neighbourhood = st.toggle('Click to see neighbourhoods with the most crimes')
    if neighbourhood:
        st.markdown('Neighbourhoods with the most crimes')
        st.bar_chart(subset_data['Neighbourhood'].value_counts())

    st.markdown('Crimes through the years')
    st.line_chart(subset_data['Date'].value_counts())

    day = st.toggle('Click to see crimes per day of the week')
    if day:
        st.markdown('Crimes ocurred per day of the week')
        st.bar_chart(subset_data['Day'].value_counts())

    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if __name__ == '__main__':
    main()