import streamlit as st
import prepare, aid
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as f
import scipy

players_data = pd.read_csv('athlete_events.csv')
actual_data = pd.read_csv('athlete_events.csv')
region_data = pd.read_csv('noc_regions.csv')

players_data = prepare.preprocess(players_data, region_data)

menu = st.sidebar.radio('Select an Option',
                 ('Medal Tally','Overall Analysis','Country-wise Analysis'))

# st.dataframe(players_data)

if menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')

    years, countries, season = aid.year_country_season(players_data)

    selected_year = st.sidebar.selectbox('Select Year', years)

    selected_country = st.sidebar.selectbox('Select Country', countries)

    selected_season = st.sidebar.selectbox('Select Season', season)

    medal_tally = aid.fetch_data(players_data, selected_year, selected_country, selected_season)

    if selected_year == 'Overall' and selected_country == 'Overall' and selected_season == 'Overall':
        st.title('Overall Analysis')

    if selected_year == 'Overall' and selected_country == 'Overall' and selected_season != 'Overall':
        st.title('Overall '+selected_season+' Olympics Analysis')

    if selected_year == 'Overall' and selected_country != 'Overall' and selected_season == 'Overall':
        st.title(selected_country + ' Overall Analysis')

    if selected_year != 'Overall' and selected_country == 'Overall' and selected_season == 'Overall':
        st.title(str(selected_year) + ' Overall Analysis')

    if selected_year != 'Overall' and selected_country != 'Overall' and selected_season == 'Overall':
        st.title(selected_country + ' ' + str(selected_year) + ' Olympics Analysis')

    if selected_year == 'Overall' and selected_country != 'Overall' and selected_season != 'Overall':
        st.title(selected_country + ' ' + selected_season + ' Olympics Analysis')

    if selected_year != 'Overall' and selected_country == 'Overall' and selected_season != 'Overall':
        st.title(str(selected_year) + ' ' + selected_season + ' Olympics Analysis')

    if selected_year != 'Overall' and selected_country != 'Overall' and selected_season != 'Overall':
        st.title(selected_country + ' ' + str(selected_year) + ' ' + selected_season + ' Olympics Analysis')

    st.table(medal_tally)

if menu == 'Overall Analysis':
    editions = players_data['Year'].unique().shape[0]
    cities = players_data['City'].unique().shape[0]
    sports = players_data['Sport'].unique().shape[0]
    athletes = players_data['Name'].unique().shape[0]
    nations = players_data['region'].unique().shape[0]
    events = players_data['Event'].unique().shape[0]

    col1,col2,col3 = st.columns(3)

    with col1:
        st.header('Editions')
        st.title(editions)

    with col2:
        st.header('Total hosts')
        st.title(cities)

    with col3:
        st.header('Total sports')
        st.title(sports)

    col1,col2,col3 = st.columns(3)

    with col1:
        st.header('Total Athletes')
        st.title(athletes)

    with col2:
        st.header('Total nations')
        st.title(nations)

    with col3:
        st.header('Total Events')
        st.title(events)

    st.title('Countries participated over the years')
    country_timeline = aid.timeline_data(players_data,'region')
    figure = px.line(country_timeline, x='Edition', y='region')
    st.plotly_chart(figure)

    st.title('Events over the years')
    event_timeline = aid.timeline_data(players_data, 'Event')
    figure = px.line(event_timeline, x='Edition', y='Event')
    st.plotly_chart(figure)

    st.title('Athletes over the years')
    athlete_timeline = aid.timeline_data(players_data, 'Name')
    figure = px.line(athlete_timeline, x='Edition', y='Name')
    st.plotly_chart(figure)

    st.title('Events over the years sports wise')
    fig,axis = plt.subplots(figsize=(20,20))
    gamma = players_data.drop_duplicates(['Year', 'Sport', 'Event'])
    axis = sns.heatmap(
        gamma.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)

    st.title('Most successful athletes by sports')
    sport_list = players_data['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select Sport',sport_list)
    st.table(aid.successful_by_sport(players_data,selected_sport))

if menu == 'Country-wise Analysis':
    st.sidebar.title('Country wise analysis')

    country_list = players_data['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country_list = st.sidebar.selectbox('Select country',country_list)
    country_data = aid.year_wise_tally_countries(players_data,selected_country_list)
    figure = px.line(country_data, x='Year', y='Medal')
    st.title(selected_country_list + ' ' + 'Medal tally over the years')
    st.plotly_chart(figure)

    st.title(selected_country_list + ' ' + 'sports wise excellence')
    table = aid.country_wise_heatmap(players_data,selected_country_list)
    if table.shape[0] != 0:
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(table,annot=True)
        st.pyplot(fig)
    else:
        st.title('No data available')

    st.title('Top athletes of ' + selected_country_list)
    top = aid.successful_by_country(players_data,selected_country_list)
    st.table(top)

# if menu == 'Player-wise Analysis':
#     athlete_data = players_data.drop_duplicates(subset=['Name', 'region'])
#     a1 = athlete_data['Age'].dropna()
#     a2 = athlete_data[athlete_data['Medal'] == 'Gold']['Age'].dropna()
#     a3 = athlete_data[athlete_data['Medal'] == 'Silver']['Age'].dropna()
#     a4 = athlete_data[athlete_data['Medal'] == 'Bronze']['Age'].dropna()
#
#     figg = f.create_distplot([a1,a2,a3,a4],['Age','Gold','Silver','Bronze'],show_hist=False,show_rug=False)
#     figg.update_layout(autosize=False,width=1000,height=600)
#     st.title('Age distribution')
#     st.plotly_chart(figg)
#
#     x = []
#     name = []
#     # sports = ['Basketball', 'Judo', 'Football', 'Tug Of War', 'Athletics', 'Swimming', 'Badmintion', 'Sailing',
#     #           'Gymnastic',
#     #           'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey', 'Rowing', 'Fencing',
#     #           'Shooting', 'Boxing', 'Takewondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis', 'Golf', 'Softball',
#     #           'Archery',
#     #           'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball', 'Rhythmic Gymnastic', 'Rugby Sevens',
#     #           'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
#     sports = players_data['Sport'].unique().tolist()
#     for sport in sports:
#         tdf = athlete_data[athlete_data['Sport'] == sport]
#         x.append(tdf[tdf['Medal'] == 'Gold']['Age'].dropna())
#         name.append(sport)
#
#     # st.dataframe(x)
#     # st.dataframe(name)
#
#     fig = f.create_distplot(x,name,show_hist=False,show_rug=False)
#     fig.update_layout(autosize=False, width=1000, height=600)
#     st.title('Sports distribution')
#     st.plotly_chart(fig)