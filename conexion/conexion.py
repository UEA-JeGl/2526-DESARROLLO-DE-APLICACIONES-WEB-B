import os
import mysql.connector


def obtener_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("MYSQL_PASSWORD"),
        database="tecnosoluciones"
    )

    return conexion