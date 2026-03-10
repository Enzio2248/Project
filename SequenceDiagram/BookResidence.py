#BookResidence

from fastapi import FastAPI , HTTPException
from abc import ABC, abstractmethod
from datetime import datetime, date

from state import LogInStatus, OperationalStatus, PurchaseStatus

class System:
    def __init__(self):
        self.__user_list = []
        self.__residence_list = []

    def create_residencebooking(self, user_id, booking, id, residence_id, room_id, start_date, end_date):
        if not self.validate_date(start_date, end_date):
            raise HTTPException(status_code=400, detail="Invalid booking dates")
        user = next((u for u in self.__user_list if u.user_id == user_id), None)
        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        if user.is_banned:
            raise HTTPException(status_code=403, detail="Banned users cannot make bookings")
        if user.login_status != LogInStatus.ONLINE:
            raise HTTPException(status_code=400, detail="User must be logged in to make a booking")

        residence, room = self.select_residence(residence_id, room_id)

        if room.operational_status != OperationalStatus.READY:
            if room.operational_status == OperationalStatus.REPAIR:
                raise HTTPException(status_code=400, detail="Cannot book: Room is currently under repair")
            elif room.operational_status == OperationalStatus.CLEANING:
                raise HTTPException(status_code=400, detail="Cannot book: Room is currently being cleaned")
            else:
                raise HTTPException(status_code=400, detail=f"Cannot book: Room status is {room.operational_status.value}")

        if not room.is_available(start_date, end_date):
            raise HTTPException(status_code=400, detail="Room is already booked for these dates")

        time_slot = TimeSlot(start_date, end_date)
        new_residence_booking = Residencebooking(id, residence, room, user, time_slot, price=room.price)

        room.add_booking_list(new_residence_booking)
        user.add_booking_list(new_residence_booking)
        booking.add_residencebooking_list(new_residence_booking)
        return new_residence_booking
    
    def select_residence(self, residence_id, room_id):
        for residence in self.__residence_list:
            if residence.residence_id == residence_id:
                for room in residence.room_list:
                    if room.room_id == room_id:
                        return residence, room
        raise HTTPException(status_code=404, detail="Residence or Room not found")
    
    def validate_date(self, start_date, end_date):
        return (
            isinstance(start_date, (date, datetime))
            and isinstance(end_date, (date, datetime))
            and start_date < end_date
        )
    
class Residence:
    def __init__(self, residence_id, residence_name):
        self.__residence_id = residence_id
        self.__residence_name = residence_name
        self.__room_list = []

    @property
    def residence_id(self):
        return self.__residence_id
    
    @property
    def room_list(self):
        return self.__room_list

class Room(ABC):
    def __init__(self, room_id, capacity):
        self._room_id = room_id
        self._capacity = capacity
        self._booking_list = []
        self._operational_status = OperationalStatus.READY

    def is_available(self, start_date, end_date):
        if self._operational_status != OperationalStatus.READY:
            return False
        for booking in self._booking_list:
            if start_date < booking.time.end_date and end_date > booking.time.start_date:
                return False
        return True
    
    @property
    def booking_list(self):
        return self._booking_list

    # add and remove booking
    def add_booking_list(self, residencebooking):
        self._booking_list.append(residencebooking)

    @property
    def operational_status(self):
        return self._operational_status
    
    @property
    def room_id(self):
        return self._room_id
    
class NormalRoom(Room):
    def __init__(self, room_id):
        super().__init__(room_id, capacity=2)
        self._price = 1000
    
    # getter / setter
    @property
    def price(self):
        return self._price

class KingRoom(Room):
    def __init__(self, room_id):
        super().__init__(room_id, capacity=4)
        self._price = 3000

    # getter / setter
    @property
    def price(self):
        return self._price


class Residencebooking:
    def __init__(self, id, residence, room, user, time, price):
        self.__id = id
        self.__user = user
        self.__residence = residence
        self.__room = room
        self.__time = time
        self.__price = price
        self.__status = PurchaseStatus.BOOKING
        self.__paid = False

    @property
    def time(self):
        return self.__time
    
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

class Booking:
    def __init__(self, booking_id, user):
        self.__residencebooking_list = []
    
    def add_residencebooking_list(self, residencebooking):
        self.__residencebooking_list.append(residencebooking)


class Customer:
    def __init__(self, user_id):
        self._user_id = user_id
        self.__booking_list = []
        self.__login_status = LogInStatus.OFFLINE
        self.__is_banned = False

    @property
    def user_id(self):
        return self._user_id

    @property
    def login_status(self):
        return self.__login_status

    @login_status.setter
    def login_status(self, status):
        self.__login_status = status

    @property
    def is_banned(self):
        return self.__is_banned

    def ban_user(self):
        self.__is_banned = True

    def add_booking_list(self, booking):
        self.__booking_list.append(booking)



# system = System()

# # USERS
# user1 = Customer("U001")
# user2 = Customer("U002")
# user3 = Customer("U003")

# # login user1
# user1.login_status = LogInStatus.ONLINE

# # banned user
# user3.login_status = LogInStatus.ONLINE
# user3.ban_user()

# system._System__user_list = [user1, user2, user3]

# # RESIDENCE
# res1 = Residence("R001", "Sea Resort")

# room1 = NormalRoom("RM01")
# room2 = KingRoom("RM02")

# res1.room_list.append(room1)
# res1.room_list.append(room2)

# system._System__residence_list = [res1]

# # BOOKING OBJECT
# booking = Booking("B001", user1)

# start_date = datetime(2026,5,1)
# end_date = datetime(2026,5,3)


# def test_residence_booking(user_id, room_id, start, end):

#     try:
#         result = system.create_residencebooking(
#             user_id,
#             booking,
#             "RB001",
#             "R001",
#             room_id,
#             start,
#             end
#         )

#         print("BOOKING SUCCESS")

#     except HTTPException as e:

#         print("BOOKING FAILED")
#         print(f"ERROR {e.status_code}: {e.detail}")

# print("\n========== TEST RESIDENCE BOOKING ==========")

# print("\n[TEST 1] Booking Success")
# test_residence_booking("U001","RM01",start_date,end_date)


# print("\n[TEST 2] User Not Found")
# test_residence_booking("U999","RM01",start_date,end_date)


# print("\n[TEST 3] User Not Login")
# test_residence_booking("U002","RM01",start_date,end_date)


# print("\n[TEST 4] User Banned")
# test_residence_booking("U003","RM01",start_date,end_date)


# print("\n[TEST 5] Room Under Repair")
# room1._operational_status = OperationalStatus.REPAIR
# test_residence_booking("U001","RM01",start_date,end_date)
# room1._operational_status = OperationalStatus.READY


# print("\n[TEST 6] Room Cleaning")
# room1._operational_status = OperationalStatus.CLEANING
# test_residence_booking("U001","RM01",start_date,end_date)
# room1._operational_status = OperationalStatus.READY


# print("\n[TEST 7] Room Already Booked")
# test_residence_booking("U001","RM01",start_date,end_date)


# print("\n[TEST 8] Invalid Date")
# test_residence_booking("U001","RM01",end_date,start_date)


# print("\n[TEST 9] Room Not Found")
# test_residence_booking("U001","RM99",start_date,end_date)


# print("\n[TEST 10] Residence Not Found")

# try:
#     system.create_residencebooking(
#         "U001",
#         booking,
#         "RB002",
#         "R999",
#         "RM01",
#         start_date,
#         end_date
#     )
# except HTTPException as e:
#     print("BOOKING FAILED")
#     print(f"ERROR {e.status_code}: {e.detail}")