import mysql.connector
from config import config  # Assuming your config is in the 'config.py' file

# Test database connection
try:
    conn = mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASS,
        database=config.DB_NAME
    )
    
    if conn.is_connected():
        print("Successfully connected to the database!")
    else:
        print("Failed to connect to the database!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
