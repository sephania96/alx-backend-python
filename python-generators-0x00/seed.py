import mysql.connector
import csv
import uuid

def connect_db():
    try:
        return mysql.connector.connect(host="localhost", user="root", password="")
    except mysql.connector.Error as err:
        print(f"Connection Error: {err}")
        return None

