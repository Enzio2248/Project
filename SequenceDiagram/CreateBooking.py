#CreateBooking

from fastapi import FastAPI , HTTPException
from abc import ABC, abstractmethod

from state import LogInStatus

class System:
    def __init__(self):
        self.__user_list = []
        self.__bookings = []

    def create_booking(self, user_id, booking_id):
        user = next((u for u in self.__user_list if u.user_id == user_id),None)

        if not user :
            raise HTTPException(status_code=404, detail="User not found")
        
        if user.is_banned:
            raise HTTPException(status_code=403, detail="Banned users cannot make bookings")

        if user.login_status != LogInStatus.ONLINE:
            raise HTTPException(status_code=401, detail="User must be logged in ")
        
        new_booking = Booking(booking_id,user)

        self.__bookings.append(new_booking)
        user.add_booking_list(new_booking)

        return {
            "booking_id": new_booking.booking_id,
            "user_id": user_id
        }
    
class Booking:
    def __init__(self, booking_id, user):
        self.__booking_id = booking_id
        self.__user = user

    @property
    def booking_id(self):
        return self.__booking_id

class User(ABC):
    def __init__(self, user_name, user_id, driver_license):
        self._user_name = user_name
        self._user_id = user_id
        self._driver_license = driver_license

    @property
    def user_id(self):
        return self._user_id
    
class Customer(User):
    def __init__(self, user_name, user_id, user_mail, password, age, driver_license):
        super().__init__(user_name, user_id, driver_license)
        self.__user_mail = user_mail
        self.__password = password
        self.__age = age
        self.__booking_list = []
        self.__login_status = LogInStatus.OFFLINE
        self.__is_banned = False

    def ban_user(self):
        self.__is_banned = True

    @property
    def email(self):
        return self.__user_mail

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

# # =========================
# # MOCK SYSTEM
# # =========================

# system = System()

# # users
# user1 = Customer("John", "U001", "john@gmail.com", "Password123", 25, "DL001")
# user2 = Customer("Jane", "U002", "jane@gmail.com", "Password456", 22, "DL002")
# user3 = Customer("Mike", "U003", "mike@gmail.com", "Password789", 30, "DL003")

# # login user1
# user1.login_status = LogInStatus.ONLINE

# # banned user
# user3.login_status = LogInStatus.ONLINE
# user3.ban_user()

# system._System__user_list = [user1, user2, user3]

# def test_booking(user_id, booking_id):

#     try:
#         booking = system.create_booking(user_id, booking_id)

#         print("\n===== BOOKING SUCCESS =====")
#         print(f"\tUser ID:\t{user_id}")
#         print(f"\tBooking ID:\t{booking.booking_id}")

#     except HTTPException as e:

#         print("\n===== BOOKING FAILED =====")
#         print(f"\tUser ID:\t{user_id}")
#         print(f"\tError:\t{e.status_code} {e.detail}")

# print("\n========== TEST CREATE BOOKING ==========")

# print("\n[TEST 1] Booking Success")
# test_booking("U001", "B001")

# print("\n[TEST 2] User Not Found")
# test_booking("U999", "B002")

# print("\n[TEST 3] User Not Login")
# test_booking("U002", "B003")

# print("\n[TEST 4] User Banned")
# test_booking("U003", "B004")

# print("\n[TEST 5] Multiple Booking Same User")
# test_booking("U001", "B005")
# test_booking("U001", "B006")

# print("\n[TEST 6] Empty Booking ID")
# test_booking("U001", "")

# print("\n[TEST 7] Duplicate Booking ID")
# test_booking("U001", "B001")