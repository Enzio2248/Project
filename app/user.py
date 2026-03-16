from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from booking import Booking
    from payment import Coupon

from abc import ABC, abstractmethod
import uuid
from state import StaffStatus , LogInStatus
# -------------------------------------------------- 
class User(ABC):
    def __init__(self, user_name, driver_license):
        self._user_name = user_name
        self._user_id = f"user-{uuid.uuid4().hex}"
        self._driver_license = driver_license
    
    # getter / setter
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
    def __init__(self, user_name, user_mail, password, age, driver_license = ""):
        super().__init__(user_name, driver_license)
        self.__user_mail = user_mail
        self.__password = password
        self.__membership = "Bronze"
        self.__age = age
        self.__booking_list : list["Booking"] = []
        self.__total_spent = 0
        self.__login_status = LogInStatus.OFFLINE
        self.__coupons : list["Coupon"] = []
        self.__is_banned = False

    def ban_user(self):
        self.__is_banned = True

    # edit and check password
    def edit_profile(self, name, email):
        self._user_name = name
        self.__user_mail = email
        return {"message": "Profile updated"}

    def check_password(self, password_input):
        return self.__password == password_input
    
    # ban user
    def ban(self):
        self.__is_banned = True

    def unban(self):
        self.__is_banned = False
    

    def login(self):
        self.__login_status = LogInStatus.ONLINE

    def logout(self):
        self.__login_status = LogInStatus.OFFLINE

    # get coupon list
    def coupon_list(self):
        return [c for c in self.__coupons if not c.is_used]

    # add 
    def add_booking_list(self, booking):
        self.__booking_list.append(booking)

    def add_coupon(self, coupon):
        self.__coupons.append(coupon)

    def add_spent(self, amount):
        self.__total_spent += amount
        if self.__total_spent >= 50000:
            self.__membership = "Gold"
        elif self.__total_spent >= 20000:
            self.__membership = "Silver"

    def calculate_membership(self):
        if self.__membership == "Gold":
            return 0.10
        elif self.__membership == "Silver":
            return 0.05
        return 0.0

    # getter / setter
    @property
    def is_banned(self):
        return self.__is_banned

    @property
    def email(self):
        return self.__user_mail

    @property
    def login_status(self):
        return self.__login_status
    
    @login_status.setter
    def login_status(self, status):
        self.__login_status = status

    @property
    def coupons(self):
        return self.__coupons
    
    @property
    def password(self):
        return self.__password
    
    @property
    def age(self):
        return self.__age   

    @login_status.setter
    def login_status(self, value):
        self.__login_status = value

class Staff(User):

    def __init__(self, user_name, user_mail, password, driver_license):
        super().__init__(user_name, driver_license)

        self.__user_mail = user_mail
        self.__password = password
        self.__login_status = LogInStatus.OFFLINE
        self._status = StaffStatus.FREE

    def check_password(self, password_input):
        return self.__password == password_input

    def login(self):
        self.__login_status = LogInStatus.ONLINE

    def logout(self):
        self.__login_status = LogInStatus.OFFLINE

    @property
    def email(self):
        return self.__user_mail

    @property
    def login_status(self):
        return self.__login_status
    
    @property
    def staff_id(self):
        return self._user_id

    @property
    def staff_name(self):
        return self._user_name

class Manager(Staff):

    def __init__(self, staff_name, user_mail, password, driver_license):
        super().__init__(staff_name, user_mail, password, driver_license)

    