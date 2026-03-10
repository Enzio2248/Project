#StartInspection

from fastapi import FastAPI , HTTPException
from abc import ABC, abstractmethod

from state import PurchaseStatus, StaffStatus

class System:
    def __init__(self):
        self.__bookings = []

    def add_booking(self, booking):
        self.__bookings.append(booking)

    def start_room_inspection(self, booking_id):
        booking = self._get_booking(booking_id)
        if not booking:
            return {"error": "Booking not found"}
        return {"message": booking.start_room_inspection()}
    
    def add_damage(self, booking_id, damage_id, description, price):
        booking = self._get_booking(booking_id)
        if not booking:
            return {"error": "Booking not found"}
        damage = booking.add_damage(damage_id, description, price)
        return {"damage_recorded": damage}
    
    def confirm_inspection_complete(self, booking_id, damaged=False):
        booking = self._get_booking(booking_id)
        if not booking:
            return {"error": "Booking not found"}
        if damaged:
            booking.update_status("wait_damage_payment")
        else:
            booking.update_status("wait_checkout_payment")
        return {"message": "inspection finished"}
    
    def _get_booking(self, booking_id):
        for booking in self.__bookings:
            if booking.booking_id == booking_id:
                return booking
        return None

class Booking:
    def __init__(self, booking_id, user):
        self.__booking_id = booking_id
        self.__residencebooking_list = []
        self.__damage_list = []
        self.__purchase_status = PurchaseStatus.BOOKING
    
    def add_residence_booking(self, residence):
        self.__residencebooking_list.append(residence)

    def start_room_inspection(self):
        if self.__residencebooking_list:
            self.__purchase_status = PurchaseStatus.INSPECTING
            return f"Booking {self.__booking_id}: Inspection started."
        return "No residence booking found"
    
    def add_damage(self, damage_id, description, price):
        damage = DamageItem(damage_id, description, price)
        self.__damage_list.append(damage)
        return damage.damage_detail
    
    def update_status(self, status):
        self.__purchase_status = status

    @property
    def purchase_status(self):
        return self.__purchase_status
    
    @property
    def booking_id(self):
        return self.__booking_id

class User(ABC):
    def __init__(self, user_name, user_id, driver_license):
        self._user_name = user_name
        self._user_id = user_id
        self._driver_license = driver_license
    
class Staff(User):
    def __init__(self, user_name, user_id, driver_license):
        super().__init__(user_name, user_id, driver_license)
        self._status = StaffStatus.FREE

class DamageItem:
    def __init__(self, damage_id, description, price):
        self.__damage_id = damage_id
        self.__description = description
        self.__price = price
        self.__paid = False

    @property
    def price(self):
        return self.__price
    
    @property
    def damage_detail(self):
        return {
            "damage_id": self.__damage_id,
            "description": self.__description,
            "price": self.__price
        }
    
class MockResidenceBooking:
    def __init__(self, residence_id):
        self.residence_id = residence_id


    
# class MockResidenceBooking:
#     def __init__(self, residence_id):
#         self.residence_id = residence_id

# def setup_mock_data():
#     print("\n========== SETUP MOCK DATA ==========")

#     system = System()

#     staff = Staff("Alice", "S001", "DL111")
#     user = Staff("MockUser", "U001", "DL999")

#     booking = Booking("B001", user)

#     # add residence booking
#     residence = MockResidenceBooking("R001")
#     booking._Booking__residencebooking_list.append(residence)

#     system.add_booking(booking)

#     return system, booking

# def test_start_inspection(system, booking):
#     try:
#         result = system.start_room_inspection(booking.booking_id)
#         print("SUCCESS")
#         print(result)
#     except Exception as e:
#         print("FAILED")
#         print(e)


# def test_booking_not_found(system):
#     try:
#         result = system.start_room_inspection("B999")
#         print("SUCCESS")
#         print(result)
#     except Exception as e:
#         print("FAILED")
#         print(e)


# def test_add_damage(system, booking):
#     try:
#         result = system.add_damage(booking.booking_id, "D001", "Broken table", 500)
#         print("SUCCESS")
#         print(result)
#     except Exception as e:
#         print("FAILED")
#         print(e)


# def test_add_damage_booking_not_found(system):
#     try:
#         result = system.add_damage("B999", "D001", "Broken table", 500)
#         print("SUCCESS")
#         print(result)
#     except Exception as e:
#         print("FAILED")
#         print(e)


# def test_confirm_inspection_no_damage(system, booking):
#     try:
#         result = system.confirm_inspection_complete(booking.booking_id, damaged=False)
#         print("SUCCESS")
#         print(result)
#         print("status:", booking.purchase_status)
#     except Exception as e:
#         print("FAILED")
#         print(e)


# def test_confirm_inspection_with_damage(system, booking):
#     try:
#         result = system.confirm_inspection_complete(booking.booking_id, damaged=True)
#         print("SUCCESS")
#         print(result)
#         print("status:", booking.purchase_status)
#     except Exception as e:
#         print("FAILED")
#         print(e)

# print("\n========== TEST START INSPECTION ==========")

# # TEST 1
# system, booking = setup_mock_data()
# print("\n[TEST 1] Start Inspection Success")
# test_start_inspection(system, booking)

# # TEST 2
# system, booking = setup_mock_data()
# print("\n[TEST 2] Booking Not Found")
# test_booking_not_found(system)

# # TEST 3
# system, booking = setup_mock_data()
# print("\n[TEST 3] Add Damage")
# test_add_damage(system, booking)

# # TEST 4
# system, booking = setup_mock_data()
# print("\n[TEST 4] Add Damage Booking Not Found")
# test_add_damage_booking_not_found(system)

# # TEST 5
# system, booking = setup_mock_data()
# print("\n[TEST 5] Confirm Inspection No Damage")
# test_confirm_inspection_no_damage(system, booking)

# # TEST 6
# system, booking = setup_mock_data()
# print("\n[TEST 6] Confirm Inspection With Damage")
# test_confirm_inspection_with_damage(system, booking)