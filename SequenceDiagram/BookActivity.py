#BookActivity

from fastapi import FastAPI , HTTPException
from abc import ABC, abstractmethod

from state import LogInStatus

class System:
    def __init__(self):
        self.__user_list = []
        self.__activity_list = []

    def create_activitybooking(self, user_id, booking, b_id, activity_id, start_date, end_date):
        if not self.validate_date(start_date, end_date):
            raise HTTPException(status_code=400, detail="Error Validate Date")
        user = next((u for u in self.__user_list if u.user_id == user_id), None)
        if not user:
            raise HTTPException(status_code=400, detail="Not Found User")
        if user.is_banned:
            raise HTTPException(status_code=403, detail="Banned users cannot make bookings")
        if user.login_status != LogInStatus.ONLINE:
            raise HTTPException(status_code=400, detail="User must be logged in to book an activity")

        activity = self.select_activity(activity_id)
        time_slot = TimeSlot(start_date, end_date)
        new_activity_booking = Activitybooking(b_id, activity, user, time_slot)

        activity.add_booking_list(new_activity_booking)
        user.add_booking_list(new_activity_booking)
        booking.add_activitybooking_list(new_activity_booking)
        return new_activity_booking
    
    def select_activity(self, activity_id):
        for activity in self.__activity_list:
            if isinstance(activity, Activity) and activity.activity_id == activity_id:
                return activity
        raise HTTPException(status_code=404, detail="Activity not found")
    
    def validate_date(self, start_date, end_date):
        if start_date >= end_date:
            return False
        return True

class Activity(ABC):
    def __init__(self, activity_id, min_age):
        self._activity_id = activity_id
        self._min_age = min_age
        self._booking_list = []

    def add_booking_list(self, activitybooking):
        self._booking_list.append(activitybooking)
    
    @property
    @abstractmethod
    def price(self):
        pass

    @property
    def activity_id(self):
        return self._activity_id

class Driving(Activity):
    def __init__(self, activity_id):
        super().__init__(activity_id, min_age=25)
        self._price = 1000

    # getter /setter
    @property
    def price(self):
        return self._price

class Hiking(Activity):
    def __init__(self, activity_id):
        super().__init__(activity_id, min_age=15)
        self._price = 1200

    # getter /setter
    @property
    def price(self):
        return self._price

class Activitybooking:
    def __init__(self, id, activity, user, time):
        self.__id = id
        self.__user = user
        self.__activity = activity
        self.__time = time

    @property
    def item_id(self): 
        return self.__id

    @property
    def user(self): 
        return self.__user

    @property
    def activity(self): 
        return self.__activity

    @property
    def time(self): 
        return self.__time
    
class Booking:
    def __init__(self, booking_id, user):
        self.__booking_id = booking_id
        self.__user = user
        self.__activitybooking_list = []

    def add_activitybooking_list(self, activitybooking):
        self.__activitybooking_list.append(activitybooking)
    
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
        self.__membership = "Bronze"
        self.__age = age
        self.__booking_list = []
        self.__total_spent = 0
        self.__login_status = LogInStatus.OFFLINE
        self.__coupons = []
        self.__is_banned = False

    def login(self):
        self.__login_status = LogInStatus.ONLINE

    def logout(self):
        self.__login_status = LogInStatus.OFFLINE

    def ban(self):
        self.__is_banned = True

    @property
    def login_status(self):
        return self.__login_status
    
    @property
    def is_banned(self):
        return self.__is_banned
    
    def add_booking_list(self, booking):
        self.__booking_list.append(booking)

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

    
# from datetime import datetime, timedelta

# def setup_mock_data(system):

#     print("\n========== SETUP MOCK DATA ==========")

#     # Users
#     user1 = Customer("Alice","U001","alice@mail","1234",30,True)
#     user2 = Customer("Bob","U002","bob@mail","1234",20,False)

#     user1.login()
#     user2.login()

#     system._System__user_list.append(user1)
#     system._System__user_list.append(user2)

#     # Activities
#     act1 = Driving("A001")
#     act2 = Hiking("A002")

#     system._System__activity_list.append(act1)
#     system._System__activity_list.append(act2)

#     print("Mock Users:", len(system._System__user_list))
#     print("Mock Activities:", len(system._System__activity_list))

#     return user1, user2, act1, act2


# def run_tests():

#     system = System()

#     user1, user2, act1, act2 = setup_mock_data(system)

#     booking = Booking("B001", user1)

#     start = datetime.now()
#     end = start + timedelta(days=2)

#     print("\n========== TEST ACTIVITY BOOKING ==========")

#     # TEST 1 SUCCESS
#     try:
#         print("\n[TEST 1] Booking Success")
#         result = system.create_activitybooking(
#             "U001",
#             booking,
#             "AB001",
#             "A001",
#             start,
#             end
#         )
#         print("PASS : Booking created")
#     except HTTPException as e:
#         print("FAIL :", e.detail)

#     # TEST 2 USER NOT FOUND
#     try:
#         print("\n[TEST 2] User Not Found")

#         system.create_activitybooking(
#             "U999",
#             booking,
#             "AB002",
#             "A001",
#             start,
#             end
#         )

#         print("FAIL : Should not pass")

#     except HTTPException as e:
#         print("PASS :", e.detail)

#     # TEST 3 USER NOT LOGIN
#     try:
#         print("\n[TEST 3] User Not Login")

#         user2.logout()

#         system.create_activitybooking(
#             "U002",
#             booking,
#             "AB003",
#             "A001",
#             start,
#             end
#         )

#         print("FAIL : Should not pass")

#     except HTTPException as e:
#         print("PASS :", e.detail)

#     # TEST 4 USER BANNED
#     try:
#         print("\n[TEST 4] User Banned")

#         user1.ban()

#         system.create_activitybooking(
#             "U001",
#             booking,
#             "AB004",
#             "A001",
#             start,
#             end
#         )

#         print("FAIL : Should not pass")

#     except HTTPException as e:
#         print("PASS :", e.detail)

#     # reset
#     user1._Customer__is_banned = False

#     # TEST 5 ACTIVITY NOT FOUND
#     try:
#         print("\n[TEST 5] Activity Not Found")

#         system.create_activitybooking(
#             "U001",
#             booking,
#             "AB005",
#             "A999",
#             start,
#             end
#         )

#         print("FAIL : Should not pass")

#     except HTTPException as e:
#         print("PASS :", e.detail)

#     # TEST 6 INVALID DATE
#     try:
#         print("\n[TEST 6] Invalid Date")

#         system.create_activitybooking(
#             "U001",
#             booking,
#             "AB006",
#             "A001",
#             end,
#             start
#         )

#         print("FAIL : Should not pass")

#     except HTTPException as e:
#         print("PASS :", e.detail)


# if __name__ == "__main__":
#     run_tests()