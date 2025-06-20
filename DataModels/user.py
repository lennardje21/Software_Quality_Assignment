
ROLES_HIERARCHY = {
    "service_engineer": 1,
    "system_admin": 2,
    "super_admin": 3
}

class User:
    def __init__(self, id, username, password_hash, first_name, last_name, role, registration_date, must_change_password=0):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.registration_date = registration_date
        self.must_change_password = must_change_password

    def is_authorized(self, required_role):
        return ROLES_HIERARCHY[self.role] >= ROLES_HIERARCHY[required_role]