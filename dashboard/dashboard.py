import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Conecta ao banco de dados SQLite
db_dir = 'database/base.db'
conn = sqlite3.connect(db_dir)

# Define a consulta SQL para buscar todos os dados da tabela 'produtos_transformados'
query = "SELECT * FROM produtos_transformados"

# Executa a consulta e carrega os dados em um dataframe
df = pd.read_sql_query(query, conn)

# Fecha a conexão com o banco de dados
conn.close()

# Garantir que a coluna 'id' seja do tipo string
df['id'] = df['id'].astype(str)

# Configuração Streamlit
st.title('Visualização de Dados do Mercado Livre')

# Descrição do dashboard
st.write("""
    Este dashboard exibe dados de produtos do Mercado Livre, incluindo preço, condição, tipo de listagem e
    modo de compra.
""")

# Tabela de dados com a thumbnail como a primeira coluna
st.subheader('Dados dos Produtos')

# Adiciona coluna de imagem ao DataFrame
df['Imagem'] = df['thumbnail'].apply(lambda x: f'<img src="{x}" style="width: 100px; height: auto;"/>')

# Filtros interativos
st.sidebar.header('Filtros')
condition = st.sidebar.multiselect('Condição', df['condition'].unique())
listing_type_id = st.sidebar.multiselect('Tipo de Listagem', df['listing_type_id'].unique())
buying_mode = st.sidebar.multiselect('Modo de Compra', df['buying_mode'].unique())
domain_id = st.sidebar.multiselect('Domínio', df['domain_id'].unique())
accepts_mercadopago = st.sidebar.selectbox('Aceita Mercado Pago', ['Todos', True, False])

# Aplicar filtros
df_filtered = df.copy()
if condition:
    df_filtered = df_filtered[df_filtered['condition'].isin(condition)]
if listing_type_id:
    df_filtered = df_filtered[df_filtered['listing_type_id'].isin(listing_type_id)]
if buying_mode:
    df_filtered = df_filtered[df_filtered['buying_mode'].isin(buying_mode)]
if domain_id:
    df_filtered = df_filtered[df_filtered['domain_id'].isin(domain_id)]
if accepts_mercadopago != 'Todos':
    df_filtered = df_filtered[df_filtered['accepts_mercadopago'] == accepts_mercadopago]

# Exibe a tabela filtrada
columns_table = ["Imagem", "id", "title", "condition", "listing_type_id", "permalink", "currency_id", "price", "original_price", "available_quantity", "accepts_mercadopago"]
st.markdown(df_filtered.to_html(escape=False, index=False, columns=columns_table), unsafe_allow_html=True)

# Gráfico de Pizza da Condição do Produto
st.subheader('Gráfico de Pizza da Condição do Produto')
if not df_filtered.empty and df_filtered['condition'].notnull().any():
    condition_counts = df_filtered['condition'].value_counts()
    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(condition_counts, labels=condition_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
    ax_pie.axis('equal')
    st.pyplot(fig_pie)
else:
    st.write("Não há dados disponíveis para exibir o gráfico de pizza da condição do produto.")
# Garantir que a coluna 'price' seja do tipo numérico
df_filtered['price'] = pd.to_numeric(df_filtered['price'], errors='coerce')
# Curva de Distribuição de Preços
st.subheader('Curva de Distribuição de Preços')
if not df_filtered.empty and df_filtered['price'].notnull().any():
    fig_dist_price, ax_dist_price = plt.subplots()
    sns.kdeplot(df_filtered['price'].dropna(), ax=ax_dist_price, color='skyblue', fill=True)
    ax_dist_price.set_xlabel('Preço')
    ax_dist_price.set_ylabel('Densidade')
    st.pyplot(fig_dist_price)
else:
    st.write("Não há dados disponíveis para exibir a curva de distribuição de preços.")

# Opção de exportação de dados
st.subheader('Exportar Dados')
st.write('Baixe os dados filtrados:')
csv = df_filtered.to_csv(index=False)
st.download_button(label="Baixar CSV", data=csv, mime='text/csv')
