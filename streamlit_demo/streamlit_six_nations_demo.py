# -*- coding: utf-8 -*-
# +
"""
Created on Tue Nov 22 15:10:50 2022
@author: VolcanoBlue13
"""
import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import folium
from streamlit_folium import folium_static
import utils

import os
# -

# # NOTE: This is adapted from the https://data-science-at-swast-handover-poc-handover-yfa2kz.streamlit.app/
# # Original source code: https://github.com/data-science-at-swast/handover_poc/blob/main/handover.py

## Set the Streamlit page configurations. These set the layout and the title and icon to appear in the tab.
st.set_page_config(page_title='2020 Six Nations',  layout='wide', page_icon=':rugby_football:')

# This sets up the header, using st.columns to tell streamlit we want two coloumns.

t1, t2 = st.columns((0.07,1)) 

current_dir = os.getcwd()

# This assigns the image to the first column
t1.image(f'{current_dir}/images/six_nations.jpeg', width = 100)
# This creates a title and adds some markdown for the second column
t2.title("2020 Guinness Six Nations - Statistics Report")
t2.markdown("  **website:** https://www.sixnationsrugby.com/ **| email:** mailto:data-analytics@nesta.org.uk")


## This adds a spinner into the webpage to let the user know it's updating.
def streamlit_demo():
    with st.spinner('Updating Report...'):

        #Metrics setting and rendering

        player_stats = pd.read_excel(f'{current_dir}/datasets/six_nations.xlsx',sheet_name = 'All player stats')
        team_stats_2019 = pd.read_excel(f'{current_dir}/datasets/six_nations.xlsx',sheet_name = '2019 Team Stats')
        stadiums = pd.read_excel(f'{current_dir}/datasets/six_nations.xlsx',sheet_name = 'Stadiums')
        ## You could read this in and get this list from the data but Streamlit will have to rerun this every time it updates the report, so I recommend keeping as much as you can in the code itself rather than reading it in.
        countries = ["All", "England ", "France", "Ireland", "Italy", "Scotland", "Wales"]
        country = st.selectbox('Choose country', countries, help = 'Filter report to show only one country')

        ## We setup five columns, with the end two being empty to allow for the three metrics to sit nice and centrally on the page.
        metric1, metric2, metric3, metric4, metric5 = st.columns((1,1,1,1,1))

        if country != "All":
            filtered_data = player_stats[player_stats.Country == country]
        else:
            filtered_data = player_stats.copy()
        metric1.write('')
        metric2.metric(label ='Most tries scored',value = str(int(filtered_data['2019 Tries '].max())), delta = str(int(filtered_data['2019 Tries '].max()) - int(filtered_data['2019 Tries '].nlargest(2).values[-1]))+' Compared to the next best player')
        metric3.metric(label ='Most tackles made',value = int(filtered_data['2019 Tackles Made'].max()), delta = str(int(filtered_data['2019 Tackles Made'].max()) - int(filtered_data['2019 Tackles Made'].nlargest(2).values[-1]))+' Compared to the next best player')
        metric4.metric(label = 'Most missed tackles',value = int(filtered_data['2019 Missed Tackles'].max()), delta = str(int(filtered_data['2019 Missed Tackles'].max()) - int(filtered_data['2019 Missed Tackles'].nlargest(2).values[-1]))+' Compared to the next worst player', delta_color = 'inverse')
        metric5.write('')

        # Number of metres gained

        g1, g2, g3 = st.columns((1,1,1))

        fig = px.bar(filtered_data.nlargest(10, "2019 Metres Gained"), x = 'Player', y='2019 Metres Gained', hover_data=["Position Detailed", "Country"], template = 'seaborn')

        fig.update_traces(marker_color='#0000FF')

        fig.update_layout(title_text="Number of metres gained (top 10)",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)

        g1.plotly_chart(fig, use_container_width=True) 

        # Number of defenders beaten

        fig = px.bar(filtered_data.nlargest(10, "2019 Defenders Beaten"), x = 'Player', y='2019 Defenders Beaten', hover_data=["Position Detailed", "Country"], template = 'seaborn')

        fig.update_traces(marker_color='#FDB633')

        fig.update_layout(title_text="Number of defenders beaten (top 10)",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)

        g2.plotly_chart(fig, use_container_width=True)  

        # Number of gain line successes
        largest_smallest = pd.concat([filtered_data.nlargest(5, "2019 Minutes Played"),filtered_data.nsmallest(5, "2019 Minutes Played").sort_values(by="2019 Minutes Played", ascending=False)], axis=0)
        fig = px.bar(largest_smallest, x = 'Player', y='2019 Minutes Played',color = "2019 Minutes Played", hover_data=["Position Detailed", "Country"], template = 'seaborn', color_continuous_scale=px.colors.diverging.Temps)

        mean_number_of_minutes = np.full(len(largest_smallest), filtered_data["2019 Minutes Played"].mean())
        fig.add_scatter(x=largest_smallest["Player"], y=mean_number_of_minutes, mode='lines', line=dict(color="black"), name='Mean')

        fig.update_layout(title_text="Number of minutes played (top 5 and bottom 5)",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None, legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))

        g3.plotly_chart(fig, use_container_width=True) 

        # Waiting Handovers table


        all_positions = filtered_data["Position Detailed"].unique()
        position = st.multiselect("Choose positions to have in table", all_positions, all_positions[:3])

        all_clubs= filtered_data["Club"].unique()
        club = st.multiselect("Choose clubs to have in table", all_clubs, all_clubs[:3])

        table1, table2 = st.columns((2.1, 2.1))

        if len(position) != 0 and len(club) == 0:
            table_data = filtered_data[filtered_data["Position Detailed"].isin(position)]
        elif len(position) == 0 and len(club) != 0:
            table_data = filtered_data[filtered_data["Club"].isin(club)]
        elif len(position) != 0 and len(club) != 0:
            table_data = filtered_data[(filtered_data["Position Detailed"].isin(position)) & (filtered_data["Club"].isin(club))]
        else:
            table_data = filtered_data.copy()

        good_stats = table_data[['Player', 'Position Detailed', 'Club',	'Scrum Score',	'Influence', 'Attacking',	'2019 Points', "2019 Carries", "2019 Clean Breaks", "2019 Gain Line Successes", "2019 Off Loads Made"]].fillna(0)

        fig = go.Figure(
                data = [go.Table (columnorder = [0,1,2,3,4,5,6,7,8,9,10], columnwidth = [20,10,10,10,10,15,15,15,15,15, 15],
                    header = dict(
                     values = list(good_stats.columns),
                     font=dict(size=12, color = 'white'),
                     fill_color = '#264653',
                     line_color = 'rgba(255,255,255,0.2)',
                     align = ['left','center'],
                     #text wrapping
                     height=20
                     )
                  , cells = dict(
                      values = [good_stats[K].tolist() for K in good_stats.columns], 
                      font=dict(size=12),
                      align = ['left','center'],
                      fill_color = "#F0F2F6",
                      line_color = 'rgba(255,255,255,0.2)',
                      height=20))])

        fig.update_layout(title_text="Stats for players",title_font_color = '#0F294A',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=480)                                                           

        table1.plotly_chart(fig, use_container_width=True)    

        # Current Waiting Table

        bad_stats = table_data[['Player', 'Position Detailed', 'Club', "2019 Missed Tackles", "2019 Turnovers Conceded", "2019 Handling Errors", "2019 Penalties Conceded", '2019 Yellow Cards', '2019 Red Cards']].fillna(0)


        fig = go.Figure(
                data = [go.Table (columnorder = [0,1,2,3,4,5, 6,7,8], columnwidth = [20,10,10,10,10,15,15,15,15],
                    header = dict(
                     values = list(bad_stats.columns),
                     font=dict(size=12, color = 'white'),
                     fill_color = '#264653',
                     align = 'left',
                     height=20
                     )
                  , cells = dict(
                      values = [bad_stats[K].tolist() for K in bad_stats.columns], 
                      font=dict(size=12),
                      align = 'left',
                      fill_color='#F0F2F6',
                      height=20))]) 

        fig.update_layout(title_text="Stats against players",title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=480)

        table2.plotly_chart(fig, use_container_width=True)
    
    with st.spinner('Report updated!'):
        time.sleep(1)    
    
    with st.expander("Map of stadiums"):
        st.header(
            f"Map showing stadiums"
        )
        if country == "All":
            start_location = [51.45666444, -0.341161777]
        else:
            filtered_location = stadiums[stadiums.Country==country][["Latitude", "Longitude"]]
            start_location = filtered_location.values[0]
        m = folium.Map(
            location=start_location,
            tiles="CartoDB positron",
            name="Light Map",
            zoom_start=11,
            attr="Stadium map",
        )


        locations = stadiums[["Latitude", "Longitude"]]
        locationlist = locations.values.tolist()

        for point in range(0, len(locationlist)):
            folium.Marker(
                locationlist[point],
                popup=stadiums["Stadium"][point],
                icon=folium.Icon(color="red", icon="rugby-ball", prefix="fa"),
            ).add_to(m)

        folium_static(m, width=1000, height=500)
    
    with st.expander("Altair example"):
        selector=alt.selection_single(empty='all', fields=['Forward Or Back'])

        color_scale=alt.Scale(domain=["Forward", "Back"],
                                range=["red", "blue"])
        base = alt.Chart(player_stats[["Age", "Height In Metres", "Country", "Weight In KG", "Forward Or Back"]]).properties(
            width=250,
            height=250
        ).add_selection(selector)

        points = base.mark_point(filled=True, size=200).encode(
            x=alt.X('mean(Height In Metres):Q',
                    scale=alt.Scale(domain=[1.7,2.0])),
            y=alt.Y('mean(Weight In KG):Q',
                    scale=alt.Scale(domain=[85,120])),
            color=alt.condition(selector,
                                'Forward Or Back:N',
                                alt.value('lightgray'),
                                scale=color_scale),
        )

        hists = base.mark_bar(opacity=0.5, thickness=100).encode(
            x=alt.X('Age',
                    bin=alt.Bin(step=5), # step keeps bin size the same
                    scale=alt.Scale(domain=[15,40])),
            y=alt.Y('count()',
                    stack=None,
                    scale=alt.Scale(domain=[0,60])),
            color=alt.Color('Forward Or Back:N',
                            scale=color_scale)
        ).transform_filter(
            selector
        )


        st.write(alt.hconcat(points,hists))
    
    with st.expander("Pandas demo"):
        pd.set_option("display.precision", 2)
        good_stats.set_index("Player", inplace=True)
        summary_table = st.table(good_stats.style.apply(utils.highlight_min))
        formatter = "{:.2f}"

pwd = st.sidebar.text_input("Password:", type='password')
if pwd == st.secrets["PASSWORD"]:
    streamlit_demo()
elif pwd == '':
    pass
else:
    st.error('wrong password. try again.')
