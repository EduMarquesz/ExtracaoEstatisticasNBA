import requests
import pandas as pd
from pandas import DataFrame
from typing import Dict, List, Any, Tuple

def get_json_result() -> Dict[str, Any]:

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'Accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://pt.global.nba.com/statistics/',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = (
        ('conference', 'All'),
        ('country', 'All'),
        ('individual', 'All'),
        ('locale', 'pt'),
        ('pageIndex', '0'),
        ('position', 'All'),
        ('qualified', 'false'),
        ('season', '2021'),
        ('seasonType', '2'),
        ('split', 'All Team'),
        ('statType', 'points'),
        ('team', 'All'),
        ('total', 'perGame'),
    )

    response = requests.get('https://pt.global.nba.com/stats2/league/playerstats.json', headers=headers, params=params)
    return response.json()


def get_info_player(player: Dict[str, Any]) -> str:
    player_info = player['playerProfile']  
    name = player_info['code']
    country = player_info['country']
    height = player_info['height']
    return name, country, height


def get_info_team(player: Dict[str, Any]) -> str:
    team_info = player['teamProfile']
    team_name = team_info['name']
    team_city = team_info['city']
    return team_name, team_city


def main() -> List[Dict[str, Any]]:
    datas = get_json_result()

    players = datas['payload']['players']

    list_players = []

    for player in players:

        new_player = {}
        name, country, height = get_info_player(player)

        new_player['name'] = name
        new_player['country'] = country
        new_player['height'] = height

        team_name, team_city = get_info_team(player)

        new_player['team_name'] = team_name
        new_player['team_city'] = team_city

        list_players.append(new_player)    
    return list_players


def load_nba() -> Tuple[List[Dict[str, Any]], DataFrame, DataFrame]:
    list_players = main()
    df = pd.DataFrame(list_players)
    df['height'] = df['height'].str.replace(',', '.').str.replace(' ', '')
    df['height'] = df['height'].astype('float')

    #Top 3 jogadores mais baixos
    minor_players = df[df['height'] < 1.90].sort_values('height').head(3)


    #Contagem das cidades dos times
    teams_cities = df['team_city'].value_counts()

    nba_dict = df.to_dict(orient='records')
    return nba_dict, minor_players, teams_cities