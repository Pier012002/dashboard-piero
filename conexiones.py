import pandas as pd
import mysql.connector 



# INFORMACIÓN DE CONEXIÓN A LA BASE DE DATOS
# ------------------------------------------


def cargar_datos():         # FUNCIÓN PARA REALIZAR LA CONEXIÓN A LA DB Y OBTENER LA TABLA DE DATOS


    try:
        conexion_db = mysql.connector.connect(
            host="sql10.freesqldatabase.com",
            user="sql10833735",
            password="9UeFiiSCXD",
            database="sql10833735"
        )


        consulta_sql = "SELECT * FROM ventas_vehiculos" 
        df = pd.read_sql(consulta_sql, conexion_db)     
        conexion_db.close()
        
        return df       # DEVOLVER EL RESULTADO AL ARCHIVO QUE LO SOLICITÓ


    except Exception as error:
        print(f"SE ENCONTRÓ UN PROBLEMA: {error}")
        
        
        