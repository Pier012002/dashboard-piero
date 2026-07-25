# GRÁFICOS DE BARRAS EN STREAMLIT:


import plotly.express as px

# GRÁFICO 1
def grafico_ventas_marca(df_filtrado):
    ventas = df_filtrado.groupby("marca")["cantidad"].sum().reset_index()


    grafico01 = px.bar(
        ventas,
        x = "marca",
        y = "cantidad",
        title = "Ventas por Marca"
    )

    return grafico01

# GRÁFICO 2
def grafico_precio_promedio(df_filtrado):
    promedio = df_filtrado.groupby("marca")["precio_venta"].mean().reset_index()


    grafico02 = px.bar(
        promedio,
        x = "marca",
        y = "precio_venta",
        title = "Precio promedio por marca"
    )


    return grafico02