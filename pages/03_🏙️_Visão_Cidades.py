#LIBRARIES - bibliotecas
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime
##(biblioteca para buscar imagem dentro do notebook)
from PIL import Image
#pip install haversine
from haversine import haversine
# Importe o módulo de expressões regulares
import re

import seaborn as sns

# Carregar os dados do CSV
csv_path = 'data.csv'
df = pd.read_csv(csv_path)

COUNTRIES = {
    1: "Índia",
    14: "Austrália",
    30: "Brasil",
    37: "Canadá",
    94: "Indonésia",
    148: "Nova Zelândia",
    162: "Filipinas",
    166: "Catar",
    184: "Singapura",
    189: "África do Sul",
    191: "Sri Lanka",
    208: "Turquia",
    214: "Emirados Árabes Unidos",
    215: "Inglaterra",
    216: "Estados Unidos da América",
}
# Adicione a coluna 'country' ao DataFrame usando o mapeamento
df['country'] = df['Country Code'].map(COUNTRIES)

st.set_page_config(page_title="Cities", page_icon="🏙️", layout="wide")



st.sidebar.markdown("## Filtros")

# Utilizando isin para filtrar os dados
selected_countries = st.sidebar.multiselect(
    "Escolha os Paises que Deseja visualizar os Restaurantes",
    df['country'].unique().tolist(),
    default=["Brasil", "Inglaterra", "Catar", "África do Sul", "Canadá", "Austrália"]
)

# Criar uma cópia do DataFrame
df_copy = df.copy()

# Tratar valores NA removendo linhas
df_copy = df_copy.dropna(subset=['Cuisines'])

# Modificar a cópia
df_copy["Cuisines"] = df_copy["Cuisines"].apply(lambda x: x.split(",")[0].strip() if isinstance(x, str) else x)

# Remover duplicatas
df_copy = df_copy.drop_duplicates(subset=['Cuisines'])

# Atribuir a cópia de volta ao DataFrame original
df = df_copy

# Criar a métrica para o número de tipos de culinárias cadastradas
num_unique_cuisines = df['Cuisines'].nunique()
filtered_df = df[df['country'].isin(selected_countries)]

st.markdown("# :cityscape: Visão Cidades")

##---------------------- TOP 10 CIDADES COM MAIS RESTAURANTES NA BASE DE DADOS --------------------------------

# 1 - Agrupe por país e cidade e conte o número de restaurantes em cada grupo
#contagem_restaurantes = df.groupby(['country', 'City'])['Restaurant ID'].count().reset_index()

contagem_restaurantes = filtered_df.groupby(['country', 'City'])['Restaurant ID'].count().reset_index()

# 2 - Ordene em ordem decrescente para encontrar as cidades e países com mais restaurantes
contagem_ordenada = contagem_restaurantes.sort_values(by='Restaurant ID', ascending=False)

# 3 - Dicionário de cores para cada país
cores_por_pais = {
    "Índia": "rgb(255, 0, 0)",
    "Austrália": "rgb(0, 0, 255)",
    "Brasil": "rgb(0, 128, 0)",
    "Canadá": "rgb(255, 165, 0)",
    "Indonésia": "rgb(255, 192, 203)",
    "Nova Zelândia": "rgb(128, 0, 128)",
    "Filipinas": "rgb(255, 255, 0)",
    "Catar": "rgb(255, 69, 0)",
    "Singapura": "rgb(255, 140, 0)",
    "África do Sul": "rgb(0, 255, 0)",
}

# 2 - Adicionando a coluna do país para obter a legenda
top_cities_df = filtered_df[filtered_df['City'].isin(contagem_ordenada.head(10)['City'])][['City', 'country']]



# 4 - Gráfico de barras com legendas personalizadas
fig = px.bar(
    contagem_ordenada.head(10),
    x='City',
    y='Restaurant ID',
    color='country',
    color_discrete_map=cores_por_pais,
    labels={'City': 'Cidade', 'Restaurant ID': 'Número de Restaurantes', 'country': 'País'},
    title='Top 10 Cidades com Mais Restaurantes',
)

# 5 - Adicionando rótulos às barras
fig.update_traces(texttemplate='%{y}', textposition='outside')

# 7 - Ajustando o tamanho do gráfico
fig.update_layout(width=1000, height=450)  # Ajuste os valores de largura (width) e altura (height) conforme necessário

# 6 - Centralizando o título
fig.update_layout(title_x=0.2)



# 7 - Exibindo o gráfico no Streamlit
st.plotly_chart(fig)


##---------------------- TOP 7 cidades com restaurantes com média de avaliação acima de 4 --------------------------------
# 1 - Agrupe por país e cidade, calcule a média das avaliações e conte o número de restaurantes em cada grupo
avaliacao_media_cidades = filtered_df.groupby(['country', 'City'])['Aggregate rating'].mean().reset_index()

# 2 - Filtrar para cidades com média de avaliação acima de 4
cidades_acima_de_4 = avaliacao_media_cidades[avaliacao_media_cidades['Aggregate rating'] > 4].sort_values(by='Aggregate rating', ascending=False).head(7)

# 3 - Dicionário de cores para cada país
cores_por_pais = {
    "Índia": "rgb(255, 0, 0)",
    "Austrália": "rgb(0, 0, 255)",
    "Brasil": "rgb(0, 128, 0)",
    "Canadá": "rgb(255, 165, 0)",
    "Indonésia": "rgb(255, 192, 203)",
    "Nova Zelândia": "rgb(128, 0, 128)",
    "Filipinas": "rgb(255, 255, 0)",
    "Catar": "rgb(255, 69, 0)",
    "Singapura": "rgb(255, 140, 0)",
    "África do Sul": "rgb(0, 255, 0)",
}

# 4 - Gráfico de barras com legendas personalizadas
fig_avaliacao = px.bar(
    cidades_acima_de_4,
    x='City',
    y='Aggregate rating',
    color='country',
    color_discrete_map=cores_por_pais,
    labels={'City': 'Cidade', 'Aggregate rating': 'Média de Avaliação', 'country': 'País'},
    title='Top 7 Cidades com Média de Avaliação Acima de 4',
)

# 5 - Adicionando rótulos às barras
fig_avaliacao.update_traces(texttemplate='%{y}', textposition='outside')

# 7 - Ajustando o tamanho do gráfico
fig_avaliacao.update_layout(width=1300, height=450)  # Ajuste os valores de largura (width) e altura (height) conforme necessário

# 6 - Centralizando o título
fig_avaliacao.update_layout(title_x=0.2)

# 7 - Exibindo o gráfico no Streamlit
st.plotly_chart(fig_avaliacao)


##---------------------- TOP  cidades com restaurantes com média de avaliação abaixo 2.5 --------------------------------

# Filtrar para cidades especificadas
cidades_especificas = df[df['City'].isin(['Gangtok', 'Ooty'])]

# Dicionário de cores para cada país
cores_por_pais = {
    "Índia": "rgb(255, 0, 0)",
    "Austrália": "rgb(0, 0, 255)",
    "Brasil": "rgb(0, 128, 0)",
    "Canadá": "rgb(255, 165, 0)",
    "Indonésia": "rgb(255, 192, 203)",
    "Nova Zelândia": "rgb(128, 0, 128)",
    "Filipinas": "rgb(255, 255, 0)",
    "Catar": "rgb(255, 69, 0)",
    "Singapura": "rgb(255, 140, 0)",
    "África do Sul": "rgb(0, 255, 0)",
}

# Criar um DataFrame com as avaliações específicas
data = {'City': ['Gangtok', 'Ooty'],
        'Aggregate rating': [1.774118, 2.453933],
        'country': ['Índia', 'Índia']}

cidades_especificas = pd.DataFrame(data)

# Gráfico de barras com legendas personalizadas
fig_avaliacao = px.bar(
    cidades_especificas,
    x='City',
    y='Aggregate rating',
    color='country',
    color_discrete_map=cores_por_pais,
    labels={'City': 'Cidade', 'Aggregate rating': 'Média de Avaliação', 'country': 'País'},
    title='Média de Avaliação para as Cidades avaliação abaixo de 2.5',
)

# Adicionando rótulos às barras
fig_avaliacao.update_traces(texttemplate='%{y}', textposition='outside')

# Ajustando o tamanho do gráfico
fig_avaliacao.update_layout(width=600, height=450)  # Ajuste os valores de largura (width) e altura (height) conforme necessário

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig_avaliacao)

##---------------------- TOP 10 cidades com restaurantes com tipos de culinárias distintos --------------------------------


# Substitua os dados anteriores pelos novos dados fornecidos
top_cidades_culinarias_distintas = pd.DataFrame({
    'City': ['Birmingham', 'Doha', 'Montreal', 'São Paulo', 'Manchester', 'Houston', 'Perth', 'Philadelphia', 'Portland', 'Calgary'],
    'Distinct_Cuisines_Count': [32, 31, 30, 30, 30, 30, 29, 29, 28, 28]
})

# Dicionário de cores para cada país
cores_por_pais = {
    "Índia": "rgb(255, 0, 0)",
    "Austrália": "rgb(0, 0, 255)",
    "Brasil": "rgb(0, 128, 0)",
    "Canadá": "rgb(255, 165, 0)",
    "Indonésia": "rgb(255, 192, 203)",
    "Nova Zelândia": "rgb(128, 0, 128)",
    "Filipinas": "rgb(255, 255, 0)",
    "Catar": "rgb(255, 69, 0)",
    "Singapura": "rgb(255, 140, 0)",
    "África do Sul": "rgb(0, 255, 0)",
}

# Gráfico de barras com legendas personalizadas
fig_culinarias = px.bar(
    top_cidades_culinarias_distintas,
    x='City',
    y='Distinct_Cuisines_Count',
    color='City',  # Não é necessário colorir por país, pois você já tem o número de culinárias distintas por cidade
    color_discrete_map=cores_por_pais,
    labels={'City': 'Cidade', 'Distinct_Cuisines_Count': 'Tipos de Culinárias Distintos'},
    title='Top 10 Cidades com Restaurantes que Oferecem Tipos de Culinárias Distintos',
)

# Adicionando rótulos às barras
fig_culinarias.update_traces(texttemplate='%{y}', textposition='outside')

# Ajustando o tamanho do gráfico
fig_culinarias.update_layout(width=1300, height=450)

# Centralizando o título
fig_culinarias.update_layout(title_x=0.2)

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig_culinarias)


