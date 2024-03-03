import numpy as np

def medals(data):
    medal_tally = data.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

def year_country_season(data):
    years = data['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    countries = np.unique(data['region'].dropna().values).tolist()
    countries.insert(0, 'Overall')

    season = data['Season'].unique().tolist()
    season.insert(0, 'Overall')

    return years, countries, season


def fetch_data(data, years, countries, season):
    medals = data.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    counter = 0
    if (years == 'Overall' and countries == 'Overall' and season == 'Overall'):
        current_data = medals

    if (years != 'Overall' and countries == 'Overall' and season == 'Overall'):
        current_data = medals[medals['Year'] == years]

    if (years == 'Overall' and countries != 'Overall' and season == 'Overall'):
        counter = 1
        current_data = medals[medals['region'] == countries]

    if (years == 'Overall' and countries == 'Overall' and season != 'Overall'):
        current_data = medals[medals['Season'] == season]

    if (years != 'Overall' and countries != 'Overall' and season != 'Overall'):
        current_data = medals[
            (medals['Year'] == years) & (medals['Season'] == season) & (medals['region'] == countries)]

    if (years != 'Overall' and countries != 'Overall' and season == 'Overall'):
        current_data = medals[(medals['Year'] == years) & (medals['region'] == countries)]

    if (years != 'Overall' and countries == 'Overall' and season != 'Overall'):
        current_data = medals[(medals['Year'] == years) & (medals['Season'] == season)]

    if (years == 'Overall' and countries != 'Overall' and season != 'Overall'):
        counter = 1
        current_data = medals[(medals['region'] == countries) & (medals['Season'] == season)]

    if (counter == 1):
        beta = current_data.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()

    else:
        beta = current_data.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                              ascending=False).reset_index()

    beta['Total'] = beta['Gold'] + beta['Silver'] + beta['Bronze']

    return beta

def timeline_data(data,column):
    timeline = data.drop_duplicates(['Year', column])['Year'].value_counts().reset_index().sort_values('Year')
    timeline = timeline.rename(columns={'Year': 'Edition', 'count': column})
    return timeline


def successful_by_sport(players_data, sport):
    sport_data = players_data.dropna(subset=['Medal'])

    if sport != 'Overall':
        sport_data = sport_data[sport_data['Sport'] == sport]

    alpha = sport_data['Name'].value_counts().reset_index().head(15).merge(players_data, left_on='Name', right_on='Name',how='left')[['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    alpha.rename(columns={'count': 'Medals'}, inplace=True)
    return alpha

def year_wise_tally_countries(players_data,country):
    country_data = players_data.dropna(subset='Medal')
    country_data.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],
                                 inplace=True)
    new_data = country_data[country_data['region'] == country]
    final_data = new_data.groupby('Year').count()['Medal'].reset_index()
    return final_data

def country_wise_heatmap(players_data,country):
    country_data = players_data.dropna(subset='Medal')
    country_data.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],
                                 inplace=True)
    new_data = country_data[country_data['region'] == country]
    table = new_data.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return table


def successful_by_country(players_data, country):
    data = players_data.dropna(subset=['Medal'])

    data = data[data['region'] == country]

    alpha = data['Name'].value_counts().reset_index().head(10).merge(players_data, left_on='Name', right_on='Name',
                                                                     how='left')[['Name', 'count', 'Sport']].drop_duplicates('Name')
    alpha.rename(columns={'count': 'Medals'}, inplace=True)
    return alpha