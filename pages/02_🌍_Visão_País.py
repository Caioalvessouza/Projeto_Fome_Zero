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
import inflection


csv_path = r'C:\Users\Caio\Documents\cientista de dados\phyton\Projeto do aluno\zomato\data.csv'
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

st.set_page_config(page_title="Countries", page_icon="🌍", layout="wide")

st.sidebar.markdown("## Filtros")

# Utilizando isin para filtrar os dados
selected_countries = st.sidebar.multiselect(
    "Escolha os Paises que Deseja visualizar os Restaurantes",
    df['country'].unique().tolist(),
    default=["Brasil", "Inglaterra", "Catar", "África do Sul", "Canadá", "Austrália"]
)
filtered_df = df[df['country'].isin(selected_countries)]


st.markdown("# :earth_americas: Visão Países")
##--------------------- QUANTIDADE DE RESTAURANTES POR PAIS -------------------------------------------------
# Criando o gráfico de barras com legendas personalizadas
fig = px.bar(
    filtered_df['country'].value_counts().reset_index(),
    x='index',
    y='country',
    title='Quantidade de Restaurantes por País',
    labels={'index': 'Países', 'country': 'Quantidade de Restaurantes'}
)

# Adicionando rótulos às barras
fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')

# Centralizando o título
fig.update_layout(title_x=0.3)

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)


##---------------------- QUANTIDADE DE CIDADES REGISTRADOS POR PAIS--------------------------------

# Criando o gráfico de barras com legendas personalizadas
fig = px.bar(
    filtered_df['country'].value_counts().reset_index(),
    x='index',
    y='country',
    title='Quantidade de Cidades Registradas por País',
    labels={'index': 'Países', 'country': 'Quantidade de Cidades'}
)

# Adicionando rótulos às barras
fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')

# Centralizando o título
fig.update_layout(title_x=0.3)

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)

##------------------------- MÉDIA DE AVALIAÇÕES FEITAS POR PAIS ------------------------------------------

# Criando o gráfico de barras com legendas personalizadas para a média de avaliações
fig = px.bar(
    filtered_df.groupby('country')['Aggregate rating'].mean().reset_index(),
    x='country',
    y='Aggregate rating',
    title='Média de Avaliações por País',
    labels={'country': 'Países', 'Aggregate rating': 'Média de Avaliações'}
)

# Adicionando rótulos às barras
fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')

# Centralizando o título
fig.update_layout(title_x=0.3)

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)


##----------------------- MÉDIA DE PREÇO DE UM PRATO PARA DUAS PESSOAS POR PAIS ---------------------------

# Criando o gráfico de barras com legendas personalizadas para a média de preço
fig = px.bar(
    filtered_df.groupby('country')['Average Cost for two'].mean().reset_index(),
    x='country',
    y='Average Cost for two',
    title='Média de Preço de um Prato para Duas Pessoas por País',
    labels={'country': 'Países', 'Average Cost for two': 'Média de Preço'}
)

# Adicionando rótulos às barras
fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')

# Centralizando o título
fig.update_layout(title_x=0.3)

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)


