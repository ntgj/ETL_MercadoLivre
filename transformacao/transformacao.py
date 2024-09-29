import pandas as pd
import sqlite3
import json

# Conectar ao banco de dados SQLite
db_dir = 'database/base.db'
conn = sqlite3.connect(db_dir)

# Definir a consulta SQL para buscar todos os dados da tabela 'produtos'
query = "SELECT * FROM produtos"

# Executar a consulta e carregar os dados em um DataFrame do Pandas
df = pd.read_sql_query(query, conn)

# Fechar a conexão com o banco de dados
conn.close()

# Função para tratar dados JSON
def extract_attributes(attr_list):
    if isinstance(attr_list, str):
        try:
            attr_list = json.loads(attr_list)  # Tenta converter a string JSON para lista
        except json.JSONDecodeError:
            return []  # Retorna lista vazia em caso de erro
    return attr_list if isinstance(attr_list, list) else []

# Expansão da coluna 'attributes'
attributes_df = df['attributes'].apply(extract_attributes).apply(pd.Series)  # Expande a coluna em um DataFrame

# Concatena os dados expandidos com o DataFrame original
df = pd.concat([df, attributes_df], axis=1)

# Remover a coluna original se não for mais necessária
df.drop(columns=['attributes'], inplace=True)


# Removendo linhas com preço negativo e convertendo a coluna price para numérica
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df = df[df['price'] >= 0]

# Salvar os dados transformados de volta no banco de dados
conn = sqlite3.connect(db_dir)
df.to_sql('produtos_transformados', conn, if_exists='replace', index=False)
conn.close()

# Verifica as colunas resultantes
print(df.columns)
