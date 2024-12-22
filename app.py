import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("demodecks.csv")


data = load_data()

# Configurar colores para los decks
deck_colors = {
    "Jinx": "purple",
    "Viktor": "blue",
    "Volibear": "orange",
    "Yasuo": "green",
}

# Sidebar para navegación
st.sidebar.title("Navegación")
option = st.sidebar.radio(
    "Selecciona la sección",
    ["Inicio", "Explorar Datos", "Gráficas por Mazo", "Comparaciones", "Correlaciones"],
)

# Sección: Inicio
if option == "Inicio":
    st.title("EDA - Project K")
    st.subheader("AlexProton")
    st.write(
        "Esta aplicación permite explorar y analizar los datos de cartas del Proyecto K."
    )
    st.image(
        "img\\project-k-images_fgrq.600.webp",
    )

# Sección: Explorar Datos
elif option == "Explorar Datos":
    st.title("Exploración de Datos")
    st.write("A continuación se muestra el dataset:")
    st.dataframe(data)
    st.write("Descripción de las columnas numéricas:")
    st.write(data.describe())

# Sección: Gráficas por Mazo
elif option == "Gráficas por Mazo":
    st.title("Análisis por Mazo")
    selected_deck = st.selectbox("Selecciona un mazo", data["Deck"].unique())
    deck_data = data[data["Deck"] == selected_deck]

    # Conteo por tipo
    st.subheader("Conteo de Tipos de Carta")
    type_count = deck_data["Tipo"].value_counts().reset_index()
    type_count.columns = ["Tipo", "Conteo"]
    fig = px.bar(
        type_count,
        x="Tipo",
        y="Conteo",
        color_discrete_sequence=[deck_colors[selected_deck]],
        title=f"Distribución de Tipos - {selected_deck}",
    )
    st.plotly_chart(fig)

    # Coste promedio de maná
    st.subheader("Coste Promedio de Maná por Tipo")
    avg_mana = (
        deck_data.groupby("Tipo")["Coste Maná"]
        .mean()
        .reset_index()
        .sort_values(by="Tipo")
    )
    fig = px.bar(
        avg_mana,
        x="Tipo",
        y="Coste Maná",
        color_discrete_sequence=[deck_colors[selected_deck]],
        title="Coste Promedio de Maná por Tipo",
    )
    st.plotly_chart(fig)

# Sección: Comparaciones
elif option == "Comparaciones":
    st.title("Comparaciones entre Mazos")

    # Comparación: Conteo por Tipo
    st.subheader("Conteo por Tipo de Carta por Mazo")
    conteo_por_tipo = (
        data.groupby(["Deck", "Tipo"])["Tipo"].count().reset_index(name="Conteo")
    )
    fig = px.bar(
        conteo_por_tipo,
        x="Tipo",
        y="Conteo",
        color="Deck",
        barmode="group",  # Cambiar a barras agrupadas
        color_discrete_map=deck_colors,
        title="Conteo por Tipo de Carta por Mazo (Barras Agrupadas)",
    )
    st.plotly_chart(fig)

    # Comparación: Coste Promedio de Maná
    st.subheader("Coste Promedio de Maná por Mazo")
    avg_mana = data.groupby("Deck")["Coste Maná"].mean().reset_index()
    fig = px.bar(
        avg_mana,
        x="Deck",
        y="Coste Maná",
        color="Deck",
        color_discrete_map=deck_colors,
        title="Coste Promedio de Maná por Mazo",
    )
    st.plotly_chart(fig)

# Sección: Correlaciones
elif option == "Correlaciones":
    st.title("Correlaciones")

    # Scatter plot: Coste de Maná vs Might
    st.subheader("Coste de Maná vs Might")
    fig = px.scatter(
        data,
        x="Coste Maná",
        y="Might",
        color="Deck",
        color_discrete_map=deck_colors,
        title="Coste de Maná vs Might por Mazo",
    )
    st.plotly_chart(fig)

    # Mostrar coeficiente de correlación
    corr = data[["Coste Maná", "Might"]].corr().iloc[0, 1]
    st.write(f"**Coeficiente de correlación**: {corr:.2f}")
