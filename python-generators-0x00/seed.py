import mysql.connector
import csv
import uuid

def connect_db():
    try:
        return mysql.connector.connect(host="localhost", user="root", password="")
    except mysql.connector.Error as err:
        print(f"Connection Error: {err}")
        return None

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

def connect_to_prodev():
    try:
        return mysql.connector.connect(host="localhost", user="root", password="", database="ALX_prodev")
    except mysql.connector.Error as err:
        print(f"Connection Error: {err}")
        return None

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5, 2) NOT NULL,
            INDEX (user_id)
        )
    """)
    print("Table user_data created successfully")
    cursor.close()

def insert_data(connection, filename):
    cursor = connection.cursor()
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                cursor.execute("""
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (str(uuid.uuid4()), row['name'], row['email'], row['age']))
            except mysql.connector.Error as err:
                print(f"Insert error: {err}")
    connection.commit()
    cursor.close()