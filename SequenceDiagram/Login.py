#Login
from fastapi import FastAPI , HTTPException
from abc import ABC, abstractmethod

from state import LogInStatus

class System:
    def __init__(self):
        self.__user_list = []

    def add_user(self, user):
        self.__user_list.append(user)

    def authenticate(self, mail, password):
        for user in self.__user_list:
            if user.email == mail and user.check_password(password):

                if user.is_banned:
                    raise HTTPException(status_code=403, detail="This account has been banned")

                user.login_status = LogInStatus.ONLINE
                return {"message": "Login successful"}

        raise HTTPException(status_code=401, detail="Invalid email or password")
        
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
        self.__login_status = LogInStatus.OFFLINE
        self.__is_banned = False

    def check_password(self, password_input):
        return self.__password == password_input
    
    @property
    def login_status(self):
        return self.__login_status
    
    @login_status.setter
    def login_status(self, status):
        self.__login_status = status

    @property
    def is_banned(self):
        return self.__is_banned
    
    @property
    def email(self):
        return self.__user_mail





# #Mock Data Setup
# system = System()

# user1 = Customer("User1", "U001", "user1@gmail.com", "Password123", 25, "Have")
# user2 = Customer("User2", "U002", "user2@gmail.com", "Password456", 30, "None")
# user3 = Customer("User3", "U003", "banned@gmail.com", "Password789", 40, "Have")

# user3._Customer__is_banned = True

# system.add_user(user1)
# system.add_user(user2)
# system.add_user(user3)

# system._System__user_list.extend([user1, user2, user3])
#
# #Test Case: Login สำเร็จ
# print ("Test Case: Login สำเร็จ")
# try:
#     result = system.authenticate("user1@gmail.com", "Password123")
#     print(result)
# except HTTPException as e:
#     print(e.detail)

# #Test Case: Password ผิด
# print ("\nTest Case: Password ผิด")
# try:
#     result = system.authenticate("user1@gmail.com", "WrongPassword")
#     print(result)
# except HTTPException as e:
#     print(e.status_code, e.detail)

# #Test Case: Email ไม่มีในระบบ
# print ("\nTest Case: Email ไม่มีในระบบ")
# try:
#     result = system.authenticate("unknown@gmail.com", "Password123")
#     print(result)
# except HTTPException as e:
#     print(e.status_code, e.detail)

# #Test Case: User ถูก Ban
# try:
#     result = system.authenticate("banned@gmail.com", "Password789")
#     print(result)
# except HTTPException as e:
#     print(e.status_code, e.detail)

# #Test Case: Login แล้ว status เปลี่ยน
# print ("\nTest Case: Login แล้ว status เปลี่ยน")
# system.authenticate("user1@gmail.com", "Password123")
# print(user1.login_status)

# #Test Case: Login ซ้ำ
# print ("\nTest Case: Login ซ้ำ")
# system.authenticate("user1@gmail.com", "Password123")
# system.authenticate("user1@gmail.com", "Password123")

# #Test Case: Password เป็นค่าว่าง
# print ("\nTest Case: Password เป็นค่าว่าง")
# try:
#     system.authenticate("user1@gmail.com", "")
# except HTTPException as e:
#     print(e.detail)

# #Test Case: Email เป็นค่าว่าง
# print ("\nTest Case: Email เป็นค่าว่าง")
# try:
#     system.authenticate("", "Password123")
# except HTTPException as e:
#     print(e.detail)

# #Test Case: User list ว่าง
# print ("\nTest Case: User list ว่าง")
# empty_system = System()

# try:
#     empty_system.authenticate("user1@gmail.com", "Password123")
# except HTTPException as e:
#     print(e.detail)