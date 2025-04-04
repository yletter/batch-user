import os
import mysql.connector
from mysql.connector import errorcode

# Fetch connection details from environment variables
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')

DB_NAME = 'userdb'
TABLE_NAME = 'users'

TABLES = {
    TABLE_NAME: (
        "CREATE TABLE IF NOT EXISTS users ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  name VARCHAR(100),"
        "  email VARCHAR(100)"
        ") ENGINE=InnoDB"
    )
}

try:
    cnx = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )
    cursor = cnx.cursor()

    print("Connected to MySQL server")

    # Create database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    print(f"Database `{DB_NAME}` checked/created.")

    cursor.execute(f"USE {DB_NAME}")

    # Create table
    for table_name, table_desc in TABLES.items():
        print(f"Creating table `{table_name}`...")
        cursor.execute(table_desc)

    # Insert a row
    cursor.execute(
        f"INSERT INTO {TABLE_NAME} (name, email) VALUES (%s, %s)",
        ("John Doe", "john@example.com")
    )

    cnx.commit()
    print("Row inserted into table.")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'cnx' in locals() and cnx.is_connected():
        cursor.close()
        cnx.close()
        print("Connection closed.")
