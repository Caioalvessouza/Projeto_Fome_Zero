
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

#---------------------------------------------------------------------------------------
# Carregar os dados do CSV
csv_path = 'data.csv'
df = pd.read_csv(csv_path)

#---------------------------------------------------------------------------------------
#limpeza dados e troca de nomes das colunas

# Limpeza dos dados
df_cleaned = df.dropna(subset=['Cuisines'])
df_cleaned = df_cleaned.dropna()

# Renomeie as colunas
def rename_columns(df):
    # Insira aqui a lógica para renomear suas colunas, se necessário
    return df

# Função para criar a coluna 'price_type'
def create_price_type(x):
    # Insira aqui a lógica para criar a coluna 'price_type' com base na coluna 'price_range'
    return x

# Função para obter o nome do país com base no código do país
def country_name(x):
    # Insira aqui a lógica para obter o nome do país com base no código do país
    return x

# Função para obter o nome da cor com base na coluna 'rating_color'
def color_name(x):
    # Insira aqui a lógica para obter o nome da cor com base na coluna 'rating_color'
    return x

# Processamento dos dados
def process_data(file_path):
    # Carregue o DataFrame
    df = pd.read_csv(file_path)

    # Limpeza dos dados
    df_cleaned = df.dropna(subset=['Cuisines'])
    df_cleaned = df_cleaned.dropna()


#----------------------------------------------------------------------------------------

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

###-----------------------------------------------------------------------------

## Criação da coluna  nome das Cores
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
df["color_name"] = df["Rating color"].map(COLORS)

#------------------------------------------------------------------------------------------------------
#Numerical Data
#Formatação de números
def get_numerical_attributes(df):
# Aqui você pode escrever o código para selecionar as colunas numéricas do DataFrame 'df'
    numerical_data = df.select_dtypes(include=['number'])
    return numerical_data
# Agora você pode chamar a função
numerical_data = get_numerical_attributes(df)

st.set_page_config(page_title="Culinária", page_icon="🍽️", layout="wide")


# Criar filtro ------------------------------------------------------------------------
st.sidebar.markdown("## Filtros")

# Utilizando isin para filtrar os dados
selected_countries = st.sidebar.multiselect(
    "Escolha os Paises que Deseja visualizar os Restaurantes",
    df['country'].unique().tolist(),
    default=["Brasil", "Inglaterra", "Catar", "África do Sul", "Canadá", "Austrália"]
)
#---------------------------------------------------------------------------------------
##Treat NA
##Tratar NA
df = df.dropna()
df.isna().sum()

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


#####---------------------------------------------------------------------------------

# Criar filtro top 20 restaurantes que deseja visualizar 

top_n = st.sidebar.slider(
        "Selecione a quantidade de Restaurantes que deseja visualizar", 1, 20, 10
)

#---------------------------------------------------------------------------------------

# Criar filtro no sidebar esquerdo 
selected_cuisines = st.sidebar.multiselect(
    "Escolha os Tipos de Culinária ",
    df.loc[:, "Cuisines"].unique().tolist(),
    default=[
        "Bar Food",
        "Vegetarian",
        "Bengali",
        "Mineira",
        "Asian",
        "Drinks Only",
        "Sushi",
        "Argentine",
        "Durban",
        "Indian",
        "Fast Food",
        "Healthy Food",
        "Iranian",
        "Burger",
        "Portuguese",
        "Cafe",
        "French",
        "Brazilian",
        "Ice Cream",
        "Armenian",
    ],  
)

#---------------------------------------------------------------------------------------

# Criar título com figura 
st.markdown("#  :knife_fork_plate: Visão Culinárias")


# Criar subtitulo 
st.markdown(f"## Melhores Restaurantes dos Principais tipos Culinários")

#---------------------------------------------------------------------------------------


st.markdown(f"## Top 20 Restaurantes")

## Criar tabela e subtitulos com os melhores restaurantes-------------------------------------------------------------------
# Colunas selecionadas
selected_columns = ['Restaurant ID', 'Restaurant Name', 'country', 'City', 'Cuisines', 'Average Cost for two', 'Aggregate rating', 'Votes']

# Sort by 'Aggregate rating' in descending order
df_sorted = df.sort_values(by='Aggregate rating', ascending=False)

# Selecionar os top 20 restaurantes com base na classificação do Aggregate rating
top_20_df = df_sorted.head(20)

# Remover pontos da coluna 'Restaurant ID'
top_20_df['Restaurant ID'] = top_20_df['Restaurant ID'].astype(str).str.replace('.', '')

# Selecione o restaurante com a classificação mais alta nos TOP 20
top_restaurant = top_20_df.iloc[0]


# Criar a métrica para o número de tipos de culinárias cadastradas
num_unique_cuisines = top_20_df['Cuisines'].nunique()
#---------------------------------------------------------------------------------------------------------
# Criação de colunas no Streamlit
columns = st.columns(5)


# Exibição de métricas na primeira coluna
columns[0].metric(
    f"{top_restaurant['country']}: {top_restaurant['Restaurant Name']}",
    value=f"{top_restaurant['Aggregate rating']:.1f}/5.0",
)


# Selecione o restaurante "Jacaranda Coffee Lane"
jacaranda_restaurant = top_20_df[top_20_df['Restaurant Name'] == 'Jacaranda Coffee Lane'].iloc[0]

# Exibição de métricas na segunda coluna para "Jacaranda Coffee Lane"
columns[1].metric(
    f"{jacaranda_restaurant['country']}: {jacaranda_restaurant['Restaurant Name']}",
    value=f"{jacaranda_restaurant['Aggregate rating']:.1f}/5.0",
)


# Selecione o restaurante "Ippudo"
Ippudo_restaurant = top_20_df[top_20_df['Restaurant Name'] == 'Ippudo'].iloc[0]

# Exibição de métricas na segunda coluna para "Ippudo"
columns[2].metric(
    f"{Ippudo_restaurant['country']}: {Ippudo_restaurant['Restaurant Name']}",
    value=f"{Ippudo_restaurant['Aggregate rating']:.1f}/5.0",
)


# Selecione o restaurante "Trilye"
Trilye_restaurant = top_20_df[top_20_df['Restaurant Name'] == 'Trilye'].iloc[0]

# Exibição de métricas na segunda coluna para "Trilye"
columns[3].metric(
    f"{Trilye_restaurant['country']}: {Trilye_restaurant['Restaurant Name']}",
    value=f"{Trilye_restaurant['Aggregate rating']:.1f}/5.0",
)


# Selecione o restaurante "Hoppers"
Hoppers_restaurant = top_20_df[top_20_df['Restaurant Name'] == 'Hoppers'].iloc[0]

# Exibição de métricas na segunda coluna para "Hoppers"
columns[4].metric(
    f"{Hoppers_restaurant['country']}: {Hoppers_restaurant['Restaurant Name']}",
    value=f"{Hoppers_restaurant['Aggregate rating']:.1f}/5.0",
)



# Exibir a tabela no Streamlit com ajuste de tamanho
st.dataframe(top_20_df[selected_columns], width=1250, height=500) 



###--------------------------------------------------------------------------------------------------------------------------
# Agrupando o DataFrame por tipo de culinária e calculando a média de avaliação
culinary_ratings = df.groupby('Cuisines')['Aggregate rating'].mean().reset_index()

# Selecionando as top 20 culinárias com base na média de avaliação
top_20_cuisines = culinary_ratings.sort_values(by='Aggregate rating', ascending=False).head(20)



# Filtrando as top N culinárias com base na seleção do usuário
filtered_cuisines = top_20_cuisines.head(top_n)

# Criando gráfico de barras
fig = px.bar(
    filtered_cuisines,
    x='Cuisines',
    y='Aggregate rating',
    title=f'Top {top_n} Culinárias Baseadas na Média de Avaliação',
    labels={'Cuisines': 'Tipo de Culinária', 'Aggregate rating': 'Média de Avaliação'},
)

# Ajustando o tamanho do gráfico centralizando o título
fig.update_layout(width=1200, height=400, title_x=0.3)

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig)





##---------------------------------------------------------------------------------------------------------------------------

# Agrupando o DataFrame por tipo de culinária e calculando a média de avaliação
culinary_ratings = df.groupby('Cuisines')['Aggregate rating'].mean().reset_index()

# Selecionando as 20 piores culinárias com base na média de avaliação (ordem ascendente)
bottom_20_cuisines = culinary_ratings.sort_values(by='Aggregate rating').head(20)

# Aplicar filtros no DataFrame
filtered_bottom_20_cuisines = bottom_20_cuisines[bottom_20_cuisines['Cuisines'].isin(selected_cuisines)]

# Filtrar também pelo top_n
filtered_bottom_20_cuisines = filtered_bottom_20_cuisines.nlargest(top_n, 'Aggregate rating')

# Criar gráfico de barras com os dados filtrados
#fig = px.bar(
    #filtered_bottom_20_cuisines,
    #x='Cuisines',
    #y='Aggregate rating',
    #title=f'Top {len(filtered_bottom_20_cuisines)} Piores Culinárias Baseadas na Média de Avaliação',
    #labels={'Cuisines': 'Tipo de Culinária', 'Aggregate rating': 'Média de Avaliação'},
#)
# Criar gráfico de barras com os dados filtrados
fig = px.bar(
    filtered_bottom_20_cuisines,
    x='Cuisines',
    y='Aggregate rating',
    title=f'Top {top_n} Piores Culinárias Baseadas na Média de Avaliação',
    labels={'Cuisines': 'Tipo de Culinária', 'Aggregate rating': 'Média de Avaliação'},
)

# Ajustando o tamanho do gráfico  centralizando o título
fig.update_layout(width=1200, height=400, title_x=0.3 )

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig)





















