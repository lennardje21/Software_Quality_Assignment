import os, sys, sqlite3

# Ensure the parent directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class DeleteData:
    def __init__(self):
        self.db_path = os.path.join(sys.path[0], "Database/urbanmobility.db")

    def delete_user(self, user_id: str) -> bool:
        try:
            with sqlite3.connect(self.db_path) as connection:
                query = '''
                    DELETE FROM users WHERE UserID = ?
                '''
                cursor = connection.cursor()
                cursor.execute(query, (user_id,))
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    def delete_traveller(self, traveller_id: str) -> bool:
        try:
            with sqlite3.connect(self.db_path) as connection:
                query = '''
                    DELETE FROM travellers WHERE TravellerID = ?
                '''
                cursor = connection.cursor()
                cursor.execute(query, (traveller_id,))
            return True
        except Exception as e:
            print(f"Error deleting traveller: {e}")
            return False

    def delete_scooter(self, scooter_id: str) -> bool:
        try:
            with sqlite3.connect(self.db_path) as connection:
                query = '''
                    DELETE FROM scooter WHERE ScooterID = ?
                '''
                cursor = connection.cursor()
                cursor.execute(query, (scooter_id,))
            return True
        except Exception as e:
            print(f"Error deleting scooter: {e}")
            return False    
    
    def clear_database(self) -> bool:
        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM users")
                cursor.execute("DELETE FROM travellers")
                cursor.execute("DELETE FROM scooter")
            return True
        except Exception as e:
            print(f"Error clearing database: {e}")
            return False