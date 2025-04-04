import streamlit as st
import pandas as pd
import plotly.express as px

# Carregando os dados
df = pd.read_csv("mercado_dados.csv")

# Cálculo de valor total por produto
df["Valor Total (R$)"] = df["Quantidade"] * df["Preço Unitário (R$)"]

st.set_page_config(page_title="Controle Mercado", layout="wide")

st.title("📊 Dashboard - Controle de Estoque do Mercado")

# Filtros
with st.sidebar:
    st.header("Filtros")
    categorias = st.multiselect("Filtrar por categoria", options=df["Categoria"].unique(), default=df["Categoria"].unique())
    fornecedores = st.multiselect("Filtrar por fornecedor", options=df["Fornecedor"].unique(), default=df["Fornecedor"].unique())

# Aplicando filtros
df_filtrado = df[(df["Categoria"].isin(categorias)) & (df["Fornecedor"].isin(fornecedores))]

# Tabela de dados
st.subheader("📋 Tabela de Produtos")
st.dataframe(df_filtrado, use_container_width=True)

# Gráfico 1 - Produtos por categoria
st.subheader("📦 Produtos por Categoria")
cat_chart = px.bar(df_filtrado.groupby("Categoria")["Quantidade"].sum().reset_index(),
                   x="Categoria", y="Quantidade", color="Categoria",
                   labels={"Quantidade": "Quantidade Total"})
st.plotly_chart(cat_chart, use_container_width=True)

# Gráfico 2 - Proporção por Fornecedor
st.subheader("🏢 Distribuição por Fornecedor")
forn_chart = px.pie(df_filtrado, names="Fornecedor", values="Quantidade", title="Proporção de Quantidade por Fornecedor")
st.plotly_chart(forn_chart, use_container_width=True)

# Gráfico 3 - Valor Total por Produto
st.subheader("💰 Valor Total em Estoque por Produto")
valor_chart = px.bar(df_filtrado.sort_values("Valor Total (R$)", ascending=True),
                     x="Valor Total (R$)", y="Produto", orientation="h",
                     color="Categoria", title="Valor Total em Estoque (R$)")
st.plotly_chart(valor_chart, use_container_width=True)
