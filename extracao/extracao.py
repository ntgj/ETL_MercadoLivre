import pandas as pd
import requests
import json
import sqlite3

# Conectar ao banco de dados SQLite
db_dir = 'database/base.db'
conn = sqlite3.connect(db_dir)
c = conn.cursor()

# URL da API do Mercado Livre
search_url = 'https://api.mercadolibre.com/sites/MLB/search?q='

# Input para a pesquisa
search = input("Insira aqui a sua pesquisa: ")

# Formata o input 
search_encoded = requests.utils.quote(search)

# Inicializa a página e a lista que irá armazenar os resultados
page = 1
results = []

# Loop para buscar todas as páginas
while True:
    # Faz a requisição para a API
    url = f"{search_url}{search_encoded}&offset={(page-1)*50}"
    print(f"Solicitando URL: {url}")  # Adicionado para depuração
    r = requests.get(url)
    
    # Verifica se a requisição foi bem-sucedida
    if r.status_code == 200:
        data = r.json()

        # Verifica se a chave 'results' está presente na resposta
        if 'results' in data:
            results += data['results']
            print(f"Página {page} processada. Total de itens coletados até agora: {len(results)}")
        else:
            print("Nenhum resultado encontrado ou formato de resposta inesperado.")
            print(f"Resposta da API: {data}")
            break
        
        # Verifica se há mais páginas a serem buscadas
        if 'paging' in data and page < data['paging']['total'] // 50 + 1:
            page += 1
        else:
            break
    else:
        print(f"Erro na requisição: {r.status_code}")
        print(f"URL solicitada: {url}")
        print(f"Resposta da API: {r.text}")
        break

# Lista para armazenar os dicionários de dados
dados_formatados = []

# Loop sobre os itens do JSON
for item in results:
    # Dicionário para armazenar os valores correspondentes às chaves especificadas
    item_formatado = {}

    # Iterar sobre todas as chaves do item
    for key in item.keys():
        # Certificar-se de que qualquer valor não string seja convertido em string
        item_formatado[key] = str(item[key]) if not isinstance(item[key], (str, type(None))) else item[key]
    
    # Adicionar o dicionário do item à lista de dados formatados
    dados_formatados.append(item_formatado)

# Criar dataframe Pandas a partir da lista de dicionários
df = pd.DataFrame(dados_formatados)

# Print dos dados formatados
print("Primeiros 5 itens dos dados formatados:")
print(df.head())

# Defina o nome da tabela no banco de dados
tabela = 'produtos'

# Inserir o dataframe no banco de dados
try:
    df.to_sql(tabela, conn, if_exists='replace', index=False)
    print("Dados inseridos no banco de dados com sucesso!")
except Exception as e:
    print(f"Ocorreu um erro ao inserir os dados no banco de dados: {e}")

# Fechar a conexão com o banco de dados
conn.close()

# Exibe a quantidade total de itens encontrados e algumas amostras
print(f"Total de itens encontrados: {len(results)}")
print(df.head())
