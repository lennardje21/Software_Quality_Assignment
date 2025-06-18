import re
import datetime

class InputValidators:

    # Traveller input validation
    @staticmethod
    def validate_name(name: str) -> bool:
        return bool(re.fullmatch(r"[A-Za-zÀ-ÿ\-\' ]{2,}", name.strip()))

    @staticmethod
    def validate_birthday(date_str: str) -> bool:
        try:
            datetime.datetime.strptime(date_str.strip(), "%Y-%m-%d")
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
