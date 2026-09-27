import os
import psycopg2

def obtener_conexion():
    conexion = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD", "12345"),
        dbname="tecnosoluciones"
    )
    return conexion