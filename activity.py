from abc import ABC, abstractmethod

# -------------------------------------------------- 
class Activity(ABC):
    def __init__(self, activity_id, min_age):
        self._activity_id = activity_id
        self._min_age = min_age
        self._booking_list = []
        self._assigned_staff = []

    # add and remove booking 
    def add_booking_list(self, activitybooking):
        self._booking_list.append(activitybooking)

    def remove_booking(self, activitybooking):
        if activitybooking in self._booking_list:
            self._booking_list.remove(activitybooking)
    
    # assign & check available 
    def is_available(self, start_date, end_date):
        for booking in self._booking_list:
            if start_date < booking.time.end_date and end_date > booking.time.start_date:
                return False
        return True
    
    def assign_staff(self, staff):
        if staff.is_available_to_work() and staff.assign_work():
            self._assigned_staff.append(staff)
            return True
        return False

    # getter /setter
    @property
    @abstractmethod
    def price(self):
        pass

    @property
    def min_age(self):
        return self._min_age

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
