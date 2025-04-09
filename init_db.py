import os
import base64
import mysql.connector
from mysql.connector import errorcode

# Fetch connection details from environment variables
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')

DB_NAME = 'userdb'
TABLE_NAME = 'users'
FILE_PATH = '/config/recs.txt'

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

    # Read and decode the base64 file
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'rb') as file:
            encoded_data = file.read()
            print("Encoded file content:")
            print(encoded_data)
        decoded_text = base64.b64decode(encoded_data).decode('utf-8')

        for line in decoded_text.strip().splitlines():
            name_email = line.strip().split(',')
            if len(name_email) == 2:
                name, email = name_email
                print(f"Inserting record: name='{name}', email='{email}'")
                cursor.execute(
                    f"INSERT INTO {TABLE_NAME} (name, email) VALUES (%s, %s)",
                    (name.strip(), email.strip())
                )
            else:
                print(f"Skipping invalid line: {line}")
        cnx.commit()
        print("All valid records inserted.")
    else:
        print(f"File not found: {FILE_PATH}")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'cnx' in locals() and cnx.is_connected():
        cursor.close()
        cnx.close()
        print("Connection closed.")
