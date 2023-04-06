from infra.repository.nba_repository import nbaRepository
from infra.tasks.nba_statistics.nba_statistics import load_nba

repo = nbaRepository()

# criar o banco
repo.create_table()
# inserir no banco
df, minor_players, teams_cities = load_nba()
repo.insert_db(df)
# Dar select no banco
print(f'{repo.select_all()}\n\n')
print(f'Os 3 menores jogadores: \n{minor_players}\n\n')
print(f'Contagem das cidades dos times: \n{teams_cities}')
