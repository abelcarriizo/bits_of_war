from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

#Conexión
conexion = mysql.connector.connect(
    host = 'localhost',
    user = DB_USER,
    password = DB_PASSWORD
)

cursor = conexion.cursor()

#Crear la base de datos si no existe
cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
cursor.execute(f'USE {DB_NAME}')