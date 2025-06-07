class Scooter:
    def __init__(self, id, brand, model, serial_number, top_speed, battery_capacity,
                 state_of_charge, target_soc_min, target_soc_max,
                 latitude, longitude, out_of_service_status, mileage,
                 last_maintenance_date, in_service_date):
        self.id = id
        self.brand = brand
        self.model = model
        self.serial_number = serial_number
        self.top_speed = top_speed
        self.battery_capacity = battery_capacity
        self.state_of_charge = state_of_charge
        self.target_soc_min = target_soc_min
        self.target_soc_max = target_soc_max
        self.latitude = latitude
        self.longitude = longitude
        self.out_of_service_status = out_of_service_status
        self.mileage = mileage
        self.last_maintenance_date = last_maintenance_date
        self.in_service_date = in_service_date
