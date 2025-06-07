class User:
    def __init__(self, id, username, password_hash, first_name, last_name, role, registration_date):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.registration_date = registration_date