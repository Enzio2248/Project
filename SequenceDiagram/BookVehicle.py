#BookVehicle

from fastapi import FastAPI , HTTPException
from abc import ABC, abstractmethod
from datetime import datetime, date

from state import LogInStatus, ServiceStatus, StaffStatus, PurchaseStatus

class System:
    def __init__(self):
        self.__user_list = []
        self.__staff_list = []
        self.__vehicle_list = []

    def create_vehiclebooking(self, user_id, booking, b_id, vehicle_id, driver_id, start_date, end_date):
        if not self.validate_date(start_date, end_date):
            raise HTTPException(status_code=400, detail="Invalid booking dates")
        user = next((u for u in self.__user_list if u.user_id == user_id), None)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.is_banned:
            raise HTTPException(status_code=403, detail="Banned users cannot make bookings")
        if user.login_status != LogInStatus.ONLINE:
            raise HTTPException(status_code=401, detail="User must be logged in to book")

        vehicle = self.select_vehicle(vehicle_id)

        if vehicle.service_status == ServiceStatus.INACTIVE:
            raise HTTPException(status_code=400, detail="Vehicle is currently out of service")
        if not vehicle.is_available(start_date, end_date):
            raise HTTPException(status_code=400, detail="Vehicle is already booked for these dates")

        staff_to_assign = None
        if user.driver_license == "Have":
            staff_to_assign = None
        else:
            if not driver_id:
                raise HTTPException(status_code=400, detail="Driver license required or please select a staff driver")
            staff_to_assign = next((s for s in self.__staff_list if s.staff_id == driver_id), None)
            if not staff_to_assign:
                raise HTTPException(status_code=404, detail="Staff driver not found")
            if not self.check_driver_license(driver_id):
                raise HTTPException(status_code=400, detail="The selected staff does not have a driver license")
            staff_to_assign.status = StaffStatus.BUSY

        time_slot = TimeSlot(start_date, end_date)
        new_vehicle_booking = Vehiclebooking(b_id, vehicle, user, time_slot, staff_driver=staff_to_assign, price=vehicle.price)

        vehicle.add_booking_list(new_vehicle_booking)
        user.add_booking_list(new_vehicle_booking)
        booking.add_vehiclebooking_list(new_vehicle_booking)
        return new_vehicle_booking
    
    def select_vehicle(self, vehicle_id):
        for vehicle in self.__vehicle_list:
            if isinstance(vehicle, Vehicle) and vehicle.vehicle_id == vehicle_id:
                return vehicle
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    def check_driver_license(self, driver_id):
        for driver in self.__staff_list:
            if driver.staff_id == driver_id:
                return driver.driver_license == "Have"
        raise HTTPException(status_code=400, detail="Error Check Driverlicense")
    
    def validate_date(self, start_date, end_date):
        return (
            isinstance(start_date, (date, datetime))
            and isinstance(end_date, (date, datetime))
            and start_date < end_date
        )
    
class Vehicle(ABC):
    def __init__(self, vehicle_id, capacity):
        self._vehicle_id = vehicle_id
        self._status = ServiceStatus.ACTIVE
        self._capacity = capacity
        self._booking_list = []

    # gettter / setter
    @property
    def service_status(self):
        return self._status

    @property
    @abstractmethod
    def price(self):
        pass

    @property
    def vehicle_id(self):
        return self._vehicle_id

    def is_available(self, start_date, end_date):
        if self._status != ServiceStatus.ACTIVE:
            return False
        for booking in self._booking_list:
            if start_date < booking.time.end_date and end_date > booking.time.start_date:
                return False
        return True
    
    def add_booking_list(self, vehiclebooking):
        self._booking_list.append(vehiclebooking)

class Motorcycle(Vehicle):
    def __init__(self, vehicle_id):
        super().__init__(vehicle_id, capacity=2)
        self._price = 100
    
    # getter / setter
    @property
    def price(self):
        return self._price

class Car(Vehicle):
    def __init__(self, vehicle_id):
        super().__init__(vehicle_id, capacity=4)
        self._price = 500
    
    # getter /setter
    @property
    def price(self):
        return self._price
    
class Vehiclebooking:
    def __init__(self, id, vehicle, user, time, staff_driver, price):
        self.__id = id
        self.__user = user
        self.__vehicle = vehicle
        self.__time = time
        self.__driver = staff_driver
        self.__price = price
        self.__status = PurchaseStatus.BOOKING
        self.__paid = False

    @property
    def time(self):
        return self.__time

class User(ABC):
    def __init__(self, user_name, user_id, driver_license):
        self._user_name = user_name
        self._user_id = user_id
        self._driver_license = driver_license

    @property
    def user_name(self):
        return self._user_name

    @property
    def user_id(self):
        return self._user_id

    @property
    def driver_license(self):
        return self._driver_license

    @driver_license.setter
    def driver_license(self, value):
        self._driver_license = value

class Customer(User):
    def __init__(self, user_name, user_id, user_mail, password, age, driver_license):
        super().__init__(user_name, user_id, driver_license)
        self.__login_status = LogInStatus.OFFLINE
        self.__booking_list = []
        self.__is_banned = False

    def ban_user(self):
        self.__is_banned = True

    @property
    def is_banned(self):
        return self.__is_banned

    @property
    def login_status(self):
        return self.__login_status
    
    @login_status.setter
    def login_status(self, status):
        self.__login_status = status
    
    def add_booking_list(self, booking):
        self.__booking_list.append(booking)

class Staff(User):
    def __init__(self, user_name, user_id, driver_license):
        super().__init__(user_name, user_id, driver_license)
        self._status = StaffStatus.FREE
    
    @property
    def staff_id(self):
        return self._user_id
    
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

class Booking:
    def __init__(self, booking_id, user):
        self.__booking_id = booking_id
        self.__user = user
        self.__vehiclebooking_list = []

    def add_vehiclebooking_list(self, vehiclebooking):
        self.__vehiclebooking_list.append(vehiclebooking)

class TimeSlot:
    def __init__(self, start_date, end_date):
        self.__start_date = start_date
        self.__end_date = end_date

    # getter / setter
    @property
    def duration_days(self):
        delta = self.__end_date - self.__start_date
        return delta.days if delta.days > 0 else 1

    @property
    def start_date(self): 
        return self.__start_date

    @property
    def end_date(self): 
        return self.__end_date
    
from datetime import datetime

# =========================
# MOCK DATA SETUP
# =========================

def setup_mock_data():

    system = System()

    # USERS
    user1 = Customer("John","U001","john@mail.com","123",25,"Have")
    user2 = Customer("Jane","U002","jane@mail.com","123",25,"None")
    user3 = Customer("Mike","U003","mike@mail.com","123",25,"Have")

    # login user1
    user1.login_status = LogInStatus.ONLINE

    # banned user
    user3.login_status = LogInStatus.ONLINE
    user3.ban_user()

    system._System__user_list = [user1,user2,user3]

    # STAFF
    staff1 = Staff("DriverA","S001","Have")
    staff2 = Staff("DriverB","S002","None")

    system._System__staff_list = [staff1,staff2]

    # VEHICLES
    car1 = Car("V001")
    bike1 = Motorcycle("V002")

    system._System__vehicle_list = [car1,bike1]

    # BOOKING
    booking = Booking("B001",user1)

    return system, booking, car1

def test_vehicle_booking(system, booking, user_id, vehicle_id, driver_id, start, end):

    try:

        system.create_vehiclebooking(
            user_id,
            booking,
            "VB001",
            vehicle_id,
            driver_id,
            start,
            end
        )

        print("BOOKING SUCCESS")

    except HTTPException as e:

        print("BOOKING FAILED")
        print(f"ERROR {e.status_code}: {e.detail}")

# def run_tests():

#     system, booking, car1 = setup_mock_data()

#     start_date = datetime(2026,6,1)
#     end_date = datetime(2026,6,3)

#     print("\n========== TEST VEHICLE BOOKING ==========")

#     print("\n[TEST 1] Booking Success (User have license)")
#     test_vehicle_booking(system,booking,"U001","V001",None,start_date,end_date)

#     print("\n[TEST 2] User Not Found")
#     test_vehicle_booking(system,booking,"U999","V001",None,start_date,end_date)

#     print("\n[TEST 3] User Not Login")
#     test_vehicle_booking(system,booking,"U002","V001","S001",start_date,end_date)

#     print("\n[TEST 4] User Banned")
#     test_vehicle_booking(system,booking,"U003","V001",None,start_date,end_date)

#     print("\n[TEST 5] Vehicle Not Found")
#     test_vehicle_booking(system,booking,"U001","V999",None,start_date,end_date)

#     print("\n[TEST 6] Vehicle Out Of Service")
#     car1._status = ServiceStatus.INACTIVE
#     test_vehicle_booking(system,booking,"U001","V001",None,start_date,end_date)
#     car1._status = ServiceStatus.ACTIVE

#     print("\n[TEST 7] Vehicle Already Booked")
#     test_vehicle_booking(system,booking,"U001","V001",None,start_date,end_date)

#     print("\n[TEST 8] Invalid Date")
#     test_vehicle_booking(system,booking,"U001","V001",None,end_date,start_date)

#     print("\n[TEST 9] User No License But No Driver Selected")
#     test_vehicle_booking(system,booking,"U002","V001",None,start_date,end_date)

#     print("\n[TEST 10] Staff Driver Not Found")
#     test_vehicle_booking(system,booking,"U002","V001","S999",start_date,end_date)

#     print("\n[TEST 11] Staff Without Driver License")
#     test_vehicle_booking(system,booking,"U002","V001","S002",start_date,end_date)

#     print("\n[TEST 12] Booking Success With Staff Driver")
#     test_vehicle_booking(system,booking,"U002","V002","S001",start_date,end_date)

# if __name__ == "__main__":
#     run_tests()