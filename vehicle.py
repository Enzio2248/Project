from abc import ABC, abstractmethod
import uuid
from state import ServiceStatus
# -------------------------------------------------- 
class Vehicle(ABC):
    def __init__(self,  capacity):
        self._vehicle_id = f"ve-{uuid.uuid4().hex}"
        self._status = ServiceStatus.ACTIVE
        self._capacity = capacity
        self._booking_list = []

    # add & remove booking
    def add_booking_list(self, vehiclebooking):
        self._booking_list.append(vehiclebooking)

    def remove_booking(self, vehiclebooking):
        if vehiclebooking in self._booking_list:
            self._booking_list.remove(vehiclebooking)
    
    # check status
    def is_available(self, start_date, end_date):
        if self._status != ServiceStatus.ACTIVE:
            return False
        for booking in self._booking_list:
            if start_date < booking.time.end_date and end_date > booking.time.start_date:
                return False
        return True

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

    @property
    def capacity(self):
        return self._capacity

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