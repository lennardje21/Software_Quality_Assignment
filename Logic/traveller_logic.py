# Logic/traveller_logic.py

from DataModels.user import User
from DataModels.traveller import Traveller
from DataAccess.insert_data import InsertData
from DataAccess.get_data import GetData
from DataAccess.delete_data import DeleteData
import uuid


class TravellerLogic:

    @staticmethod
    def add_traveller(user: User, traveller: Traveller) -> bool:
        if not user.is_authorized("system_admin"):
            return False
        return InsertData().insert_traveller(traveller)

    @staticmethod
    def update_traveller(user: User, traveller: Traveller) -> bool:
        if not user.is_authorized("system_admin"):
            return False
        return InsertData().insert_traveller(traveller)  # Upsert behavior

    @staticmethod
    def delete_traveller(user: User, traveller_id: str) -> bool:
        if not user.is_authorized("system_admin"):
            return False
        return DeleteData().delete_traveller(traveller_id)

    @staticmethod
    def search_traveller(user: User, search_key: str) -> list[Traveller]:
        if not user.is_authorized("system_admin"):
            return []
        return TravellerLogic.search_traveller_by_partial(search_key)

    @staticmethod
    def search_traveller_by_partial(search_key: str) -> list[Traveller]:
        get = GetData()
        all_travellers = get.get_all_travellers()
        key = search_key.lower()
        return [
            t for t in all_travellers if
            key in t.id.lower() or
            key in t.first_name.lower() or
            key in t.last_name.lower() or
            key in t.email_address.lower() or
            key in t.driving_license_number.lower()
        ]

    @staticmethod
    def find_traveller_by_id(traveller_id: str) -> Traveller | None:
        return GetData().get_traveller_by_id(traveller_id)

    @staticmethod
    def create_traveller_from_input() -> Traveller | None:
        import datetime
        from Presentation.general_shared_methods import general_shared_methods

        try:
            print("Please enter traveller details (leave blank to cancel):")
            first = input("First Name: ").strip()
            if not first:
                return None
            last = input("Last Name: ").strip()
            birth = input("Birthday (YYYY-MM-DD): ").strip()
            gender = input("Gender: ").strip()
            street = input("Street Name: ").strip()
            number = input("House Number: ").strip()
            zipcode = input("Zip Code: ").strip()
            city = input("City: ").strip()
            email = input("Email: ").strip()
            phone = input("Mobile Phone: ").strip()
            license = input("Driving License Number: ").strip()

            return Traveller(
                id=str(uuid.uuid4()),
                first_name=first,
                last_name=last,
                birthday=birth,
                gender=gender,
                street_name=street,
                house_number=number,
                zip_code=zipcode,
                city=city,
                email_address=email,
                mobile_phone=phone,
                driving_license_number=license,
                registration_date=str(datetime.date.today())
            )
        except Exception as e:
            print(f"Error creating traveller: {e}")
            return None

    @staticmethod
    def modify_traveller_from_input(existing: Traveller) -> Traveller:
        def update(field_name, current_value):
            val = input(f"{field_name} [{current_value}]: ").strip()
            return val if val else current_value

        return Traveller(
            id=existing.id,
            first_name=update("First Name", existing.first_name),
            last_name=update("Last Name", existing.last_name),
            birthday=update("Birthday", existing.birthday),
            gender=update("Gender", existing.gender),
            street_name=update("Street Name", existing.street_name),
            house_number=update("House Number", existing.house_number),
            zip_code=update("Zip Code", existing.zip_code),
            city=update("City", existing.city),
            email_address=update("Email", existing.email_address),
            mobile_phone=update("Mobile Phone", existing.mobile_phone),
            driving_license_number=update("Driving License Number", existing.driving_license_number),
            registration_date=existing.registration_date
        )
