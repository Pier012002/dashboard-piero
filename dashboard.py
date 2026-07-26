import streamlit as st
from conexiones import cargar_datos
from indicadores import *
from graficos import *

# 1. Configuración de página
st.set_page_config(page_title="Wigo Motors", layout="wide")

# 2. Control de estado de autenticación
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

def check_credentials(usuario, password):
    USUARIOS = {
        "admin": "1234",
        "piero": "wigo2026"
    }
    return USUARIOS.get(usuario) == password

def mostrar_login():
    st.title("Acceso al Dashboard - Wigo Motors")
    with st.form("form_login"):
        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Iniciar sesión")

        if submit:
            if check_credentials(usuario, password):
                st.session_state.autenticado = True
                st.success("Acceso concedido")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

# 3. BLOQUEO ABSOLUTO: Si no está autenticado, muestra solo el login y detiene la ejecución
if not st.session_state.autenticado:
    mostrar_login()
    st.stop()

df = cargar_datos()
# CONFIGURACIÓN DE DASHBOARD CON STREAMLIT:


st.set_page_config(page_title = "Wigo Motors", 
                   layout="wide")      


st.title("WIGO MOTORS S.A.C.")                      
st.subheader("Buscador comercial") 

st.sidebar.header("Filtros")

df_filtrado = df.copy()

# FILTRO POR MARCA:

valor1 = st.sidebar.selectbox("Seleccionar marca", df["marca"].unique()) # Mostrar las marcas disponibles y sin repetir
df_filtrado = df[df["marca"] == valor1]                                   # Filtrar búsqueda por marca  
 
valor2 = st.sidebar.selectbox("Seleccionar asesor", df["asesor_comercial"].unique()) # Mostrar las marcas disponibles y sin repetir
df_filtrado = df[df["asesor_comercial"] == valor2]                                   # Filtrar búsqueda por marca  
    
valor3 = st.sidebar.selectbox("Seleccionar sede", df["tienda"].unique()) # Mostrar las marcas disponibles y sin repetir
df_filtrado = df[df["tienda"] == valor3]

valor4 = st.sidebar.selectbox("Seleccionar metodo de pago", df["metodo_pago"].unique())
df_filtrado = df[df["metodo_pago"] == valor4]


# Obtenemos el precio mínimo y máximo real de la base de datos para los límites del slider
precio_min_posible = float(df["precio_venta"].min())
precio_max_posible = float(df["precio_venta"].max())
    
    # Creamos el slider de rango (al pasarle una tupla en 'value', Streamlit activa los dos selectores de rango)
rango_precios = st.sidebar.slider(
    "Seleccione el rango de precios (S/)",
    min_value=precio_min_posible,
    max_value=precio_max_posible,
    value=(precio_min_posible, precio_max_posible), # Rango inicial por defecto (todo seleccionado)
    step=100.0 # Incremento del slider
    )
    
    # Filtramos el dataframe conservando solo los precios que se encuentren dentro del rango elegido
df_filtrado = df[(df["precio_venta"] >= rango_precios[0]) & (df["precio_venta"] <= rango_precios[1])]

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
