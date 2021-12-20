import requests
import json
import pandas as pd


def get_json_result():

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

    resposta = requests.get('https://pt.global.nba.com/stats2/league/playerstats.json', headers=headers, params=params)

    dados = json.loads(resposta.text)
    return dados

def get_info_player(player):
    info_jogador =player['playerProfile']  
    nome = info_jogador['code']
    pais = info_jogador['country']
    altura = info_jogador['height']
    return nome,pais,altura

def get_info_team(player):
    info_time = player['teamProfile']
    nome_time = info_time['name']
    cidade_time = info_time['city']
    return nome_time,cidade_time

def main():
    dados = get_json_result()

    jogadores = dados['payload']['players']


    lista_jogadores = []

    for jogador in jogadores:

        novo_jogador = {}
        nome,pais,altura = get_info_player(jogador)

        novo_jogador['Nome'] = nome
        novo_jogador['Pais'] = pais
        novo_jogador['Altura'] = altura

        nome_time,cidade_time = get_info_team(jogador)

        novo_jogador['NomeTime'] = nome_time
        novo_jogador['CidadeTime'] = cidade_time

        lista_jogadores.append(novo_jogador)    
    return lista_jogadores
    
if __name__ == '__main__':
    lista_jogadores = main()
    tabela = pd.DataFrame(lista_jogadores)
    tabela['Altura'] = tabela['Altura'].astype('float')

    #Top 3 jogadores mais baixos
    menores_jogadores = tabela[tabela['Altura'] < 1.90].sort_values('Altura').head(3)


    #Contagem das cidades dos times
    times_cidades = tabela['CidadeTime'].value_counts()

