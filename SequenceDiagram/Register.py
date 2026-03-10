#Register

from fastapi import FastAPI , HTTPException
from abc import ABC, abstractmethod
import re

class System:
    def __init__(self):
        self.__user_list = []

    def register(self, user_name, user_id, user_mail, password, age, driver_license):
        if "@" not in user_mail:
            raise HTTPException(status_code=400, detail="Invalid email format (must contain @)")
        if len(password) < 9:
            raise HTTPException(status_code=400, detail="Password must be longer than 9 characters")
        if not re.search(r"[A-Z]", password):
            raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter")
        if not re.search(r"\d", password):
            raise HTTPException(status_code=400, detail="Password must contain at least one digit")
        for existing_user in self.__user_list:
            if existing_user.user_id == user_id or existing_user.email == user_mail:
                raise HTTPException(status_code=400, detail="User ID or Email already exists")
        new_user = Customer(user_name, user_id, user_mail, password, age, driver_license)
        self.__user_list.append(new_user)
        return {"message": "User registered successfully"}

class User(ABC):
    def __init__(self, user_name, user_id, driver_license):
        self._user_name = user_name
        self._user_id = user_id
        self._driver_license = driver_license
    
class Customer(User):
    def __init__(self, user_name, user_id, user_mail, password, age, driver_license):
        super().__init__(user_name, user_id, driver_license)
        self.__user_mail = user_mail
        self.__password = password
        self.__age = age

    @property
    def email(self):
        return self.__user_mail

    @property
    def user_id(self):
        return self._user_id






# # Mock System

# system = System()

# # mock user ที่มีอยู่แล้วในระบบ
# system._System__user_list = [
#     Customer("John", "U001", "john@gmail.com", "Password123", 25, "DL001"),
#     Customer("Jane", "U002", "jane@gmail.com", "Password456", 22, "DL002")
# ]

# # =========================
# # Test Function
# # =========================

# def test_register(name, uid, mail, password, age, license_id):

#     try:
#         result = system.register(name, uid, mail, password, age, license_id)

#         print("\n===== REGISTER SUCCESS =====")
#         print(f"\tName:\t{name}")
#         print(f"\tEmail:\t{mail}")
#         print(result)

#     except HTTPException as e:

#         print("\n===== REGISTER FAILED =====")
#         print(f"\tName:\t{name}")
#         print(f"\tEmail:\t{mail}")
#         print(f"\tError:\t{e.status_code} {e.detail}")


# # =========================
# # TEST CASES
# # =========================

# print("\n========== TEST REGISTER ==========")


# # 1 Register Success
# test_register(
#     "Alice",
#     "U003",
#     "alice@gmail.com",
#     "Password789",
#     23,
#     "DL003"
# )


# # 2 Email ไม่มี @
# test_register(
#     "Bob",
#     "U004",
#     "bobgmail.com",
#     "Password123",
#     30,
#     "DL004"
# )


# # 3 Password สั้นเกิน
# test_register(
#     "Chris",
#     "U005",
#     "chris@gmail.com",
#     "Pass12",
#     28,
#     "DL005"
# )


# # 4 ไม่มีตัวพิมพ์ใหญ่
# test_register(
#     "David",
#     "U006",
#     "david@gmail.com",
#     "password123",
#     28,
#     "DL006"
# )


# # 5 ไม่มีตัวพิมพ์เล็ก
# test_register(
#     "Emma",
#     "U007",
#     "emma@gmail.com",
#     "PASSWORD123",
#     28,
#     "DL007"
# )


# # 6 ไม่มีตัวเลข
# test_register(
#     "Frank",
#     "U008",
#     "frank@gmail.com",
#     "PasswordABC",
#     28,
#     "DL008"
# )


# # 7 User ID ซ้ำ
# test_register(
#     "George",
#     "U001",
#     "george@gmail.com",
#     "Password123",
#     28,
#     "DL009"
# )


# # 8 Email ซ้ำ
# test_register(
#     "Henry",
#     "U010",
#     "john@gmail.com",
#     "Password123",
#     28,
#     "DL010"
# )


# # 9 Password ไม่มีตัวใหญ่ + ตัวเลข
# test_register(
#     "Ivan",
#     "U011",
#     "ivan@gmail.com",
#     "passwordabc",
#     28,
#     "DL011"
# )


# # 10 Password ไม่มีตัวเล็ก + ตัวเลข
# test_register(
#     "Jack",
#     "U012",
#     "jack@gmail.com",
#     "PASSWORDABC",
#     28,
#     "DL012"
# )


# # =========================
# # Show Users In System
# # =========================

# print("\n========== USERS IN SYSTEM ==========")

# for user in system._System__user_list:
#     print(user.email)