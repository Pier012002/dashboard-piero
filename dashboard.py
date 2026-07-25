import streamlit as st
from conexiones import cargar_datos
from indicadores import *
from graficos import *

df = cargar_datos()
# CONFIGURACIÓN DE DASHBOARD CON STREAMLIT:


st.set_page_config(page_title = "Wigo Motors", 
                   layout="wide")      


st.title("WIGO MOTORS S.A.C.")                      
st.subheader("Buscador comercial") 


st.sidebar.header("Buscador")
tipo_busqueda = st.sidebar.selectbox("Seleccione tipo de búsqueda", ["Marca", "Asesor comercial", "Sede"])  


df_filtrado = df.copy()

# FILTRO POR MARCA:


if tipo_busqueda == "Marca":
    valor = st.sidebar.selectbox("Seleccionar marca", df["marca"].unique()) # Mostrar las marcas disponibles y sin repetir
    df_filtrado = df[df["marca"] == valor]                                   # Filtrar búsqueda por marca  
    
elif tipo_busqueda == "Asesor comercial":
    valor = st.sidebar.selectbox("Seleccionar asesor", df["asesor_comercial"].unique()) # Mostrar las marcas disponibles y sin repetir
    df_filtrado = df[df["asesor_comercial"] == valor]                                   # Filtrar búsqueda por marca  
    
elif tipo_busqueda == "Sede":
    valor = st.sidebar.selectbox("Seleccionar sede", df["tienda"].unique()) # Mostrar las marcas disponibles y sin repetir
    df_filtrado = df[df["tienda"] == valor]

st.success(f"Registros encontrados: {len(df_filtrado)}")        # Mostrar la cantidad de filas encontradas (color verde)
st.dataframe(df_filtrado)

# INDICADORES GENERALES: 


st.subheader("Indicadores:")


c1, c2, c3, c4 = st.columns(4)          # CREANDO 4 COLUMNAS  


c1.metric("Precio Total", f"S/{precio_total(df_filtrado):,.2f}")          # Calcular el total de monto 
c2.metric("Unidades vendidas", f"{unidades_vendidas(df_filtrado)}")                # Calcular el total de unidades vendidad
c3.metric("Precio promedio", f"S/{precio_promedio(df_filtrado):,.2f}")      # Calculcar el precio promedio
c4.metric("Operaciones", operaciones(df_filtrado))

modelocon_mayorprecio = df_filtrado.loc[df_filtrado['precio_venta'].idxmax(), 'modelo']
modelocon_menorprecio = df_filtrado.loc[df_filtrado['precio_venta'].idxmin(), 'modelo']
    
    #st.metric(f"Precio máximo ({modelocon_mayorprecio})", f"S/{df_filtrado['precio_venta'].max():,.2f}")

c5, c6, c7, c8 = st.columns(4)

c5.metric(f"Precio máximo ({modelocon_mayorprecio})", f"S/{precio_maximo(df_filtrado):,.2f}")
c6.metric(f"Precio mínimo ({modelocon_menorprecio})", f"S/{precio_minimo(df_filtrado):,.2f}")

st.plotly_chart(grafico_ventas_marca(df_filtrado))
st.plotly_chart(grafico_precio_promedio(df_filtrado))