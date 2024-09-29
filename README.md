 # Mercado Livre ETL e Dashboard

Este projeto realiza a extração, transformação e visualização de dados do Mercado Livre. Utilizamos Python, SQLite e Streamlit para construir uma pipeline ETL e um dashboard interativo.

Este projeto está limitado a 1000 resultados por pesquisa, limite de usuário público da API do Mercado Livre, porém,  pode-se facilmente implementar a utilização de um token para aumentar este limite.
## Instalação

- Clone o repositório:
   git clone https://github.com/ntgj/ETL_MercadoLivre.git
   cd ETL_MercadoLivre

    Crie e ative um ambiente virtual:
    python -m venv venv
    source venv/Scripts/activate

    Instale as dependências:
    pip install -r requirements.txt

## Uso
    - Extração de Dados
    python extracao/extracao.py
    - Transformação de Dados
    python transformacao/transformacao.py
    - Visualização de Dados
    streamlit run dashboard/dashboard.py

# Descrição dos arquivos .py

# extracao.py
Este script realiza a extração de dados da API do Mercado Livre com base em uma consulta fornecida pelo usuário. Ele coleta todos os itens correspondentes à consulta e os salva em um banco de dados SQLite.

# transformacao.py
Este script realiza a transformação dos dados extraídos, expandindo a coluna attributes para criar colunas adicionais no DataFrame, e então salva os dados transformados em uma nova tabela no banco de dados.

# dashboard.py
Este script utiliza o Streamlit para criar um dashboard interativo que permite a visualização dos dados transformados. Ele gera gráficos para mostrar a distribuição das condições dos produtos, preços e marcas.
