import mysql.connector
from mysql.connector import Error
from backend.config import get_settings

settings = get_settings()

def delete_table(
    host=settings.DB_ENDPOINT, 
    user=settings.DB_USERNAME, 
    password=settings.DB_PASSWORD, 
    database=settings.DB_NAME, 
    table_name='user_configurations'):

    try:
        connection = mysql.connector.connect(
            host=host, 
            user=user, 
            password=password, 
            database=database
        )

        if connection.is_connected():
            cursor = connection.cursor()
            drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
            cursor.execute(drop_table_query)
            connection.commit()
            print(f"Table '{table_name}' deleted successfully.")
    except Error as e:
        print(f"Error deleting table: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print('MySQL Table deleted.')
    
if __name__ == "__main__":
    delete_table()
