#CancelBooking

from fastapi import FastAPI , HTTPException
from abc import ABC, abstractmethod

from state import PurchaseStatus, ServiceStatus, OperationalStatus, StaffStatus

class System:
    def __init__(self):
        self.__manager_list = []
        self.__booking_list = []

    def cancel_booking(self, booking_id, requester_id):
        booking = self._get_booking(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        is_manager = any(m.user_id == requester_id for m in self.__manager_list)
        is_owner = booking.user_id == requester_id

        if not is_manager and not is_owner:
            raise HTTPException(status_code=403, detail="Permission denied")

        if not is_manager and booking.purchase_status != PurchaseStatus.BOOKING:
            raise HTTPException(status_code=400, detail="Can only cancel bookings with status BOOKING")

        for rb in booking.residencebooking_list:
            rb.room.remove_booking(rb)
            rb.update_status(PurchaseStatus.CANCELLED)

        for vb in booking.vehiclebooking_list:
            vb.vehicle.remove_booking(vb)
            if vb.driver:
                vb.driver.complete_work()
            vb.update_status(PurchaseStatus.CANCELLED)

        for ab in booking.activitybooking_list:
            ab.activity.remove_booking(ab)
            ab.update_status(PurchaseStatus.CANCELLED)

        booking.cancel()
        return {"message": f"Booking {booking_id} has been cancelled"}
    
    def _get_booking(self, booking_id):
        for b in self.__booking_list:
            if b.booking_id == booking_id:
                return b
        return None
    
class Booking:
    def __init__(self, booking_id, user):
        self.__booking_id = booking_id
        self.__user = user
        self.__purchase_status = PurchaseStatus.BOOKING
        self.__residencebooking_list = []
        self.__vehiclebooking_list = []
        self.__activitybooking_list = []

    def cancel(self):
        self.__purchase_status = PurchaseStatus.CANCELLED

    @property
    def booking_id(self):
        return self.__booking_id

    @property
    def purchase_status(self):
        return self.__purchase_status
    
    @property
    def user_id(self):
        return self.__user.user_id
    
    @property
    def residencebooking_list(self):
        return self.__residencebooking_list

    @property
    def vehiclebooking_list(self):
        return self.__vehiclebooking_list

    @property
    def activitybooking_list(self):
        return self.__activitybooking_list

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

    def update_status(self, status):
        self.__status = status

    @property
    def room(self): 
        return self.__room

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

    def update_status(self, status):
        self.__status = status

    @property
    def vehicle(self): 
        return self.__vehicle
    
    @property
    def driver(self): 
        return self.__driver

class Activitybooking:
    def __init__(self, id, activity, user, time):
        self.__id = id
        self.__user = user
        self.__activity = activity
        self.__time = time
        self.__price = activity.price
        self.__status = PurchaseStatus.BOOKING
        self.__paid = False

    def update_status(self, status):
        self.__status = status

    @property
    def activity(self): 
        return self.__activity

class Room(ABC):
    def __init__(self, room_id, capacity):
        self._room_id = room_id
        self._capacity = capacity
        self._booking_list = []
        self._operational_status = OperationalStatus.READY

    def remove_booking(self, residencebooking):
        if residencebooking in self._booking_list:
            self._booking_list.remove(residencebooking)

class Vehicle(ABC):
    def __init__(self, vehicle_id, capacity):
        self._vehicle_id = vehicle_id
        self._status = ServiceStatus.ACTIVE
        self._capacity = capacity
        self._booking_list = []

    def remove_booking(self, vehiclebooking):
        if vehiclebooking in self._booking_list:
            self._booking_list.remove(vehiclebooking)

class User(ABC):
    def __init__(self, user_name, user_id, driver_license):
        self._user_name = user_name
        self._user_id = user_id
        self._driver_license = driver_license

    @property
    def user_id(self):
        return self._user_id

class Staff(User):
    def __init__(self, user_name, user_id, driver_license):
        super().__init__(user_name, user_id, driver_license)

    def complete_work(self):
        self._status = StaffStatus.FREE

from datetime import datetime

# # =========================
# # MOCK DATA SETUP
# # =========================

# class DummyActivity:
#     def __init__(self):
#         self.price = 100

#     def remove_booking(self, booking):
#         pass


# class DummyResidence:
#     def remove_booking(self, booking):
#         pass


# class DummyRoom(Room):
#     def __init__(self, room_id):
#         super().__init__(room_id, 2)


# class DummyVehicle(Vehicle):
#     def __init__(self, vehicle_id):
#         super().__init__(vehicle_id, 4)


# def setup_mock_data():

#     system = System()

#     print("\n========== SETUP MOCK DATA ==========")

#     # USERS
#     user1 = Staff("John","U001","Have")
#     user2 = Staff("Jane","U002","Have")

#     # MANAGER
#     manager = Staff("Boss","M001","Have")

#     system._System__manager_list = [manager]

#     # ROOM
#     room = DummyRoom("R001")

#     # VEHICLE
#     vehicle = DummyVehicle("V001")

#     # ACTIVITY
#     activity = DummyActivity()

#     # BOOKING
#     booking = Booking("B001",user1)

#     # RESIDENCE BOOKING
#     rb = Residencebooking("RB001",None,room,user1,None,100)
#     booking.residencebooking_list.append(rb)

#     # VEHICLE BOOKING
#     vb = Vehiclebooking("VB001",vehicle,user1,None,user2,200)
#     booking.vehiclebooking_list.append(vb)

#     # ACTIVITY BOOKING
#     ab = Activitybooking("AB001",activity,user1,None)
#     booking.activitybooking_list.append(ab)

#     system._System__booking_list = [booking]

#     print("Mock booking created")

#     return system, booking, user1, user2, manager

# def test_cancel_booking(system, booking_id, requester):

#     try:

#         result = system.cancel_booking(booking_id, requester)

#         print("SUCCESS:", result)

#     except HTTPException as e:

#         print("FAILED")
#         print(f"ERROR {e.status_code}: {e.detail}")

# def run_tests():

#     system, booking, user1, user2, manager = setup_mock_data()

#     print("\n========== TEST CANCEL BOOKING ==========")

#     # TEST 1 SUCCESS OWNER
#     print("\n[TEST 1] Cancel By Owner")
#     test_cancel_booking(system,"B001","U001")

#     # RESET
#     booking._Booking__purchase_status = PurchaseStatus.BOOKING

#     # TEST 2 SUCCESS MANAGER
#     print("\n[TEST 2] Cancel By Manager")
#     test_cancel_booking(system,"B001","M001")

#     # RESET
#     booking._Booking__purchase_status = PurchaseStatus.BOOKING

#     # TEST 3 BOOKING NOT FOUND
#     print("\n[TEST 3] Booking Not Found")
#     test_cancel_booking(system,"B999","U001")

#     # TEST 4 PERMISSION DENIED
#     print("\n[TEST 4] Permission Denied")
#     test_cancel_booking(system,"B001","U999")

#     # TEST 5 STATUS NOT BOOKING
#     print("\n[TEST 5] Cannot Cancel Paid Booking")

#     booking._Booking__purchase_status = PurchaseStatus.INSPECTING

#     test_cancel_booking(system,"B001","U001")

#     print("\n[TEST 6] Manager Cancel Even If Not BOOKING")

#     booking._Booking__purchase_status = PurchaseStatus.COMPLETED

#     test_cancel_booking(system,"B001","M001")

# if __name__ == "__main__":
#     run_tests()