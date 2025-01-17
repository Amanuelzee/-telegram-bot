import mysql.connector
from config import config

# Establish a connection to the database using a context manager
def db_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )

def add_user(full_name, phone_number, telegram_username, bank_transaction_number):
    try:
        with db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (full_name, phone_number, telegram_username, bank_transaction_number) "
                    "VALUES (%s, %s, %s, %s)",
                    (full_name, phone_number, telegram_username, bank_transaction_number)
                )
                conn.commit()
                print(f"User {full_name} added successfully!")  # Logging for success
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def approve_user(user_id):
    try:
        with db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET status = 'approved' WHERE id = %s", 
                    (user_id,)
                )
                conn.commit()
                print(f"User {user_id} approved successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def get_pending_users():
    try:
        with db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, full_name FROM users WHERE status = 'pending'"
                )
                users = cursor.fetchall()
                print("Fetched pending users successfully!")
        return users
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def assign_car_and_registration_number(user_id):
    try:
        with db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM users WHERE car_number > 0")
                current_count = cursor.fetchone()[0]

                # Calculate car number and registration number
                car_number = (current_count // 65) + 1
                registration_number = f"FH{1000 + user_id}/4"  # Unique registration number

                cursor.execute(
                    "UPDATE users SET car_number = %s, registration_number = %s WHERE id = %s",
                    (car_number, registration_number, user_id)
                )
                conn.commit()
                print(f"Assigned car number {car_number} and registration number {registration_number} to user {user_id}!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def get_admin_notifications():
    try:
        with db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT message FROM admin_notifications ORDER BY timestamp DESC LIMIT 1"
                )
                notification = cursor.fetchone()
                return notification[0] if notification else None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
