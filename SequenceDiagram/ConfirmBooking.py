#ConfirmBooking

from fastapi import FastAPI , HTTPException
from abc import ABC, abstractmethod

from state import PurchaseStatus, StaffStatus
class System:
    def __init__(self):
        self.__staff_list = []

    def add_staff(self, staff):
        self.__staff_list.append(staff)

    def confirm_booking(self, staff_id, booking):
        staff_exists = any(s.staff_id == staff_id for s in self.__staff_list)
        if staff_exists:
            booking.confirm()
            return {"message": f"Booking {booking.booking_id} confirmed by staff {staff_id}"}
        raise HTTPException(status_code=400, detail="Confirmation failed: Authorized staff not found")

class Booking:
    def __init__(self, booking_id, user):
        self.__booking_id = booking_id
        self.__purchase_status = PurchaseStatus.BOOKING

    def confirm(self):
        self.__purchase_status = PurchaseStatus.COMPLETED

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

    @property
    def staff_id(self):
        return self._user_id
    
# # =========================
# # MOCK DATA SETUP
# # =========================

# def setup_mock_data():
#     print("\n========== SETUP MOCK DATA ==========")

#     system = System()

#     staff1 = Staff("Alice", "S001", "DL111")
#     staff2 = Staff("Bob", "S002", "DL222")

#     system.add_staff(staff1)
#     system.add_staff(staff2)

#     user = Staff("MockUser", "U001", "DL999")

#     booking = Booking("B001", user)

#     return system, staff1, staff2, booking


# # =========================
# # TEST FUNCTION
# # =========================

# def test_confirm_success(system, staff, booking):
#     try:
#         result = system.confirm_booking(staff.staff_id, booking)
#         print("SUCCESS")
#         print(result)
#     except HTTPException as e:
#         print("FAILED")
#         print(e.detail)


# def test_staff_not_found(system, booking):
#     try:
#         result = system.confirm_booking("S999", booking)
#         print("SUCCESS")
#         print(result)
#     except HTTPException as e:
#         print("FAILED")
#         print(e.detail)


# def test_multiple_staff(system, staff2, booking):
#     try:
#         result = system.confirm_booking(staff2.staff_id, booking)
#         print("SUCCESS")
#         print(result)
#     except HTTPException as e:
#         print("FAILED")
#         print(e.detail)


# def test_confirm_twice(system, staff, booking):
#     try:
#         system.confirm_booking(staff.staff_id, booking)
#         result = system.confirm_booking(staff.staff_id, booking)
#         print("SUCCESS")
#         print(result)
#     except HTTPException as e:
#         print("FAILED")
#         print(e.detail)


# def test_invalid_staff_type(system, booking):
#     try:
#         result = system.confirm_booking(12345, booking)
#         print("SUCCESS")
#         print(result)
#     except HTTPException as e:
#         print("FAILED")
#         print(e.detail)


# def test_already_completed(system, staff, booking):
#     try:
#         booking.confirm()
#         result = system.confirm_booking(staff.staff_id, booking)
#         print("SUCCESS")
#         print(result)
#     except HTTPException as e:
#         print("FAILED")
#         print(e.detail)


# # =========================
# # RUN TEST CASES
# # =========================

# print("\n========== TEST CONFIRM BOOKING ==========")

# # TEST 1
# system, staff1, staff2, booking = setup_mock_data()
# print("\n[TEST 1] Confirm Booking Success")
# test_confirm_success(system, staff1, booking)

# # TEST 2
# system, staff1, staff2, booking = setup_mock_data()
# print("\n[TEST 2] Staff Not Found")
# test_staff_not_found(system, booking)

# # TEST 3
# system, staff1, staff2, booking = setup_mock_data()
# print("\n[TEST 3] Confirm By Another Staff")
# test_multiple_staff(system, staff2, booking)

# # TEST 4
# system, staff1, staff2, booking = setup_mock_data()
# print("\n[TEST 4] Confirm Booking Twice")
# test_confirm_twice(system, staff1, booking)

# # TEST 5
# system, staff1, staff2, booking = setup_mock_data()
# print("\n[TEST 5] Invalid Staff ID Type")
# test_invalid_staff_type(system, booking)

# # TEST 6
# system, staff1, staff2, booking = setup_mock_data()
# print("\n[TEST 6] Already Completed Booking")
# test_already_completed(system, staff1, booking)