import re
import datetime

class InputValidators:

    # Traveller input validation
    @staticmethod
    def validate_name(name: str) -> bool:
        return bool(re.fullmatch(r"[A-Za-zÀ-ÿ\-\' ]{2,}", name.strip()))

    @staticmethod
    def validate_date(s: str) -> bool:
        try:
            datetime.datetime.strptime(s.strip(), "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_gender(gender: str) -> bool:
        return gender.strip().lower() in ["male", "female"]

    @staticmethod
    def validate_street_name(street: str) -> bool:
        return len(street.strip()) >= 2

    @staticmethod
    def validate_house_number(number: str) -> bool:
        return number.strip().isdigit()

    @staticmethod
    def validate_zipcode(zipcode: str) -> bool:
        zipcode = zipcode.upper()
        return bool(re.fullmatch(r"\d{4}[A-Z]{2}", zipcode.strip()))

    @staticmethod
    def validate_city(city: str, allowed_cities: list[str]) -> bool:
        return city.strip().capitalize() in [c.capitalize() for c in allowed_cities]

    @staticmethod
    def validate_email(email: str) -> bool:
        return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email.strip()))

    @staticmethod
    def validate_mobile_phone(phone: str) -> bool:
        return bool(re.fullmatch(r"\d{8}", phone.strip()))  # Expects just 8 digits

    @staticmethod
    def validate_driving_license_number(license_num: str) -> bool:
        license_num = license_num.upper()
        if bool(re.fullmatch(r"[A-Z]{1}\d{8}", license_num.strip())):
            return True
        if bool(re.fullmatch(r"[A-Z]{2}\d{7}", license_num.strip())):
                return True
        return False
    
    @staticmethod
    def validate_search_key(value):
        # Limit length
        if not value or len(value) > 100:
            return False
        # Basic sanitization: allow letters, digits, basic symbols
        pattern = r"^[\w\s\-@.']+$"
        return re.match(pattern, value.strip()) is not None
    

    # Scooter input validation
    @staticmethod
    def validate_integer_range(value: str, min_val=0, max_val=999999):
        try:
            val = int(value)
            return min_val <= val <= max_val
        except:
            return False

    @staticmethod
    def validate_float_range(value: str, min_val=-90.0, max_val=90.0):
        try:
            val = float(value)
            return min_val <= val <= max_val
        except:
            return False

    @staticmethod
    def validate_yes_no(value: str) -> bool:
        return value.strip().lower() in ['yes', 'no']

    @staticmethod
    def validate_id(s: str) -> bool:
        return bool(re.match(r"^[A-Za-z0-9\-_]{1,50}$", s))  # Safe ID format

    @staticmethod
    def validate_percentage(s: str) -> bool:
        return s.isdigit() and 0 <= int(s) <= 100

    @staticmethod
    def validate_latitude(s: str) -> bool:
        try:
            val = float(s)
            return -90.0 <= val <= 90.0
        except ValueError:
            return False

    @staticmethod
    def validate_longitude(s: str) -> bool:
        try:
            val = float(s)
            return -180.0 <= val <= 180.0
        except ValueError:
            return False

    @staticmethod
    def validate_boolean(s: str) -> bool:
        return s.lower() in ['yes', 'no', 'true', 'false', '0', '1']

    @staticmethod
    def validate_positive_number(s: str) -> bool:
        try:
            return float(s) >= 0
        except ValueError:
            return False

    @staticmethod
    def validate_safe_string(value: str) -> bool:
        # Only letters, numbers, underscores allowed
        return bool(re.match(r'^[a-zA-Z0-9_]+$', value))

    @staticmethod
    def validate_generic_name(value: str) -> bool:
        return bool(re.match(r"^[a-zA-Z0-9\s\-]{2,50}$", value.strip()))

    @staticmethod
    def validate_alphanumeric(value: str) -> bool:
        return bool(re.match(r"^[a-zA-Z0-9\-]+$", value.strip()))
    
    @staticmethod
    def validate_username(username: str) -> bool:
        # Letters, numbers, and underscores; 3–30 characters
        return bool(re.fullmatch(r"[a-zA-Z0-9_]{3,30}", username.strip()))
