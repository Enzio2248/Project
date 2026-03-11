from __future__ import annotations
from fastapi import HTTPException
from abc import ABC, abstractmethod
from state import OperationalStatus 
from booking import Residencebooking
import uuid
# -------------------------------------------------- 
class Residence:
    def __init__(self,  residence_name):
        self.__residence_id = f"re-{uuid.uuid4().hex}"
        self.__residence_name = residence_name
        self.__room_list : list[Room] = []
    
    # add room
    def add_room_list(self, room : Room):
        if any(r.room_id == room.room_id for r in self.__room_list):
            raise HTTPException(status_code=401, detail="Room ID already exists in this residence")
        self.__room_list.append(room)
        return {"message": f"Room {room.room_id} added successfully"}

    # getter / setter
    @property
    def residence_id(self):
        return self.__residence_id

    @property
    def residence_name(self):
        return self.__residence_name

    @property
    def room_list(self):
        return self.__room_list

class Room(ABC):
    def __init__(self,  capacity):
        self._room_id = f"room-{uuid.uuid4().hex}"
        self._capacity = capacity
        self._booking_list : list[Residencebooking] = []
        self._operational_status = OperationalStatus.READY

    # update status
    def is_available(self, start_date, end_date):
        if self._operational_status != OperationalStatus.READY:
            return False
        for booking in self._booking_list:
            if start_date < booking.time.end_date and end_date > booking.time.start_date:
                return False
        return True
    
    def update_operational_status(self, status):
        self._operational_status = status
        return self._operational_status
    
    # add and remove booking
    def add_booking_list(self, residencebooking):
        self._booking_list.append(residencebooking)

    def remove_booking(self, residencebooking):
        if residencebooking in self._booking_list:
            self._booking_list.remove(residencebooking)

    @property
    def booking_list(self):
        return self._booking_list

    # getter / settet
    @property
    @abstractmethod
    def price(self):
        pass

    @property
    def room_id(self):
        return self._room_id

    @property
    def operational_status(self):
        return self._operational_status

    @property
    def capacity(self):
        return self._capacity

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
