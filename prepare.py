import pandas as pd

def preprocess(players_data, region_data):
    # merge with region_data
    players_data = players_data.merge(region_data, on='NOC', how='left')
    # remove duplicates
    players_data.drop_duplicates(inplace=True)
    # one hot encoding the medals
    players_data = pd.concat([players_data, pd.get_dummies(players_data['Medal'])], axis=1)
    return players_data