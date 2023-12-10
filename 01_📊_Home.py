import folium
import pandas as pd
import streamlit as st
from folium.plugins import MarkerCluster
from PIL import Image
from streamlit_folium import folium_static
from haversine import haversine
import matplotlib.pyplot as plt
import plotly.express as px
#from utils import general_data as gd
#from utils.process_data import process_data
from collections import Counter

caminho_csv = 'C:/Users/Caio/Documents/cientista de dados/phyton/Projeto do aluno/zomato/data.csv'

# Leia o arquivo CSV e crie o DataFrame
df = pd.read_csv(caminho_csv)




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

#Numerical Data
#Formatação de números
def get_numerical_attributes(df):
# Aqui você pode escrever o código para selecionar as colunas numéricas do DataFrame 'df'
    numerical_data = df.select_dtypes(include=['number'])
    return numerical_data
# Agora você pode chamar a função
numerical_data = get_numerical_attributes(df)




st.set_page_config(page_title="Home", page_icon="📊", layout="wide")

def create_sidebar(df, image_path='logoprojetofomezero.png'):
    imagem = Image.open(image_path)
    st.sidebar.image(imagem, width=120)


    col1, col2 = st.sidebar.columns([1, 4], gap="small")
    col1.image(imagem, width=35)
    col2.markdown("# Fome Zero")

    st.sidebar.markdown("## Filtros")
    print(df.columns)

    
    countries = st.sidebar.multiselect(
    "Escolha os Paises que Deseja visualizar os Restaurantes",
    df.loc[:, "country"].unique().tolist(),
    default=["Brasil", "Inglaterra", "Catar", "África do Sul", "Canadá", "Austrália"],
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



def main():
    st.title("Fome Zero - O Melhor lugar para encontrar seu mais novo restaurante favorito!")
    create_sidebar(df, r"C:\Users\Caio\Documents\cientista de dados\phyton\Projeto do aluno\zomato\logoprojetofomezero.png")
if __name__ == "__main__":
  main()

##-----------------------------------------------------------------------------------------------------------
def create_map(dataframe):
    f = folium.Figure(width=1300, height=900)
    m = folium.Map(max_bounds=True).add_to(f)  ###### arrumar quando terminar colocar o a no mapa
    marker_cluster = MarkerCluster().add_to(m)

    colors = ["darkgreen", "green", "lightgreen", "orange", "red", "darkred"]
  
    for idx, line in dataframe.iterrows():
        name = line["Restaurant Name"]
        price_for_two = line["Average Cost for two"]
        cuisine = line["Cuisines"]
        currency = line["Currency"]
        rating = line["Aggregate rating"]

        # Escolhe uma cor diferente para cada restaurante
        color = colors[idx % len(colors)]
      
        html = "<p><strong>{}</strong></p>".format(name)
        html += "<p>Price: {} ({}) para dois</p>".format(price_for_two, currency)
        html += "<p>Type: {}</p>".format(cuisine)
        html += "<p>Aggregate rating: {}/5.0</p>".format(rating)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker(
            [line["Latitude"], line["Longitude"]],
            popup=popup,
            icon=folium.Icon(color=color, icon="home", prefix="fa"),
        ).add_to(marker_cluster)

    folium_static(m, width=1300, height=900)
  
##-------------------------------------------------------------------------------------------------------------
def main():
    df = pd.read_csv(r'C:\Users\Caio\Documents\cientista de dados\phyton\Projeto do aluno\zomato\data.csv')
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

    st.markdown("### Temos as seguintes marcas dentro da nossa plataforma:")

    # Criação de cinco colunas
    columns = st.columns(5)

    # Exibição de métrica na primeira coluna
    columns[0].metric(
        "Restaurantes Cadastrados",
        value=df['Restaurant ID'].nunique(),
    )

    # Exibição de métrica na segunda coluna
    columns[1].metric(
        "Países Cadastrados",
        value=df.loc[:, 'country'].nunique(),
    )

    # Exibição de métrica na terceira coluna
    columns[2].metric(
        "Cidades Cadastrados",
        value=df.loc[:, 'City'].nunique(),
    )

   
    columns[3].metric(
    "Avaliações/Plataforma",
    value=f"{df['Votes'].sum():,}".replace(',', '.'),
   )


# Exibir a métrica no Streamlit
    columns[4].metric(
    "Tipos de Culinárias cadastradas",
    value=num_unique_cuisines,
   )
 ##----------------------------------------------------------------------------------------------------------------
    st.sidebar.markdown("### Dados Tratados")

    st.sidebar.download_button(
       "Baixar Dados Tratados",
       r"C:\Users\Caio\Documents\cientista de dados\phyton\Projeto do aluno\zomato\data.csv",
       key="download_button"
    )
    create_map(df)

if __name__ == "__main__":
    main()
