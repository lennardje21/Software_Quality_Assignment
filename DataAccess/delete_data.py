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
    
    def revoke_restore_codes_for_admin(self, target_admin_id: str) -> bool:
        try:
            from Logic.cryptography import Cryptography
            self.cryptography = Cryptography()
            
            with sqlite3.connect(self.db_path) as connection:
                # First, get all unused restore codes
                query_select = "SELECT id, target_admin_id FROM restore_codes WHERE used = 0"
                cursor = connection.cursor()
                cursor.execute(query_select)
                rows = cursor.fetchall()
                
                matching_code_ids = []
                for row in rows:
                    decrypted_admin_id = self.cryptography.decrypt(row[1])
                    if decrypted_admin_id == target_admin_id:
                        matching_code_ids.append(row[0])
                
                if not matching_code_ids:
                    print("No matching unused restore codes found for this admin.")
                    return False
                
                # Delete the matching codes using their IDs
                placeholders = ', '.join(['?'] * len(matching_code_ids))
                delete_query = f"DELETE FROM restore_codes WHERE id IN ({placeholders})"
                cursor.execute(delete_query, matching_code_ids)
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error revoking restore codes: {e}")
            return False