# Logic/login_logic.py

import sqlite3
from DataModels.user import User

DB_PATH = 'Database/urbanmobility.db'

class LoginLogic:

    @staticmethod
    def authenticate_user(username: str, password: str) -> str | None:
        """
        Verifies credentials and returns the user's role if valid.
        """
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT Role
            FROM users
            WHERE UserName = ? AND PasswordHash = ?
        """, (username, password))

        row = cursor.fetchone()
        connection.close()

        if row:
            return row[0]  # role
        return None

    @staticmethod
    def get_user_object(username: str, password: str) -> User | None:
        """
        Returns a User object from the database if credentials are valid.
        """
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT UserID, UserName, PasswordHash, FirstName, LastName, Role, RegistrationDate
            FROM users
            WHERE UserName = ? AND PasswordHash = ?
        """, (username, password))

        row = cursor.fetchone()
        connection.close()

        if row:
            return User(
                id=row[0],
                username=row[1],
                password_hash=row[2],
                first_name=row[3],
                last_name=row[4],
                role=row[5],
                registration_date=row[6]
            )
        return None
