import os
import psycopg2


def obtener_conexion():

    database_url = os.getenv("DATABASE_URL")

    if database_url:
        conexion = psycopg2.connect(database_url)
    else:
        conexion = psycopg2.connect(
            host="localhost",
            port=5432,
            user="postgres",
            password=os.getenv("POSTGRES_PASSWORD", "12345"),
            dbname="tecnosoluciones"
        )

    return conexion