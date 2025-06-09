import datetime


class Traveller:
    def __init__(self, id, first_name, last_name, 
    birthday, gender, street_name, house_number, 
    zip_code, city, email_address, mobile_phone, 
    driving_license_number, registration_date):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.gender = gender
        self.street_name = street_name
        self.house_number = house_number
        self.zip_code = zip_code
        self.city = city
        self.email_address = email_address
        self.mobile_phone = mobile_phone
        self.driving_license_number = driving_license_number
        self.registration_date = registration_date or datetime.now().strftime('%d-%m-%Y %H:%M:%S')