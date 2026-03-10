from datetime import datetime
import uuid
# --------------------------------------------------
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


class DamageItem:
    def __init__(self, damage_id, description, price):
        self.__damage_id = damage_id
        self.__description = description
        self.__price = price
        self.__paid = False

    # mark paid
    def mark_paid(self):
        self.__paid = True

    # getter / setter
    @property
    def damage_id(self):
        return self.__damage_id

    @property
    def item_id(self):
        return self.__damage_id

    @property
    def damage_detail(self):
        return {
            "damage_id": self.__damage_id,
            "description": self.__description,
            "price": self.__price
        }

    @property
    def paid(self):
        return self.__paid

    @property
    def price(self):
        return self.__price

class Review:
    def __init__(self, user_id, booking_id, rating, comment):
        self.__review_id = f"review-{uuid.uuid4().hex}"
        self.__user_id = user_id
        self.__booking_id = booking_id
        self.__rating = rating      
        self.__comment = comment
        self.__created_at = datetime.now()

    # getter / setter
    @property
    def review_id(self): 
        return self.__review_id

    @property
    def user_id(self): 
        return self.__user_id

    @property
    def booking_id(self): 
        return self.__booking_id

    @property
    def rating(self): 
        return self.__rating

    @property
    def comment(self): 
        return self.__comment

    @property
    def created_at(self): 
        return self.__created_at

    @property
    def detail(self):
        return {
            "review_id": self.__review_id,
            "user_id": self.__user_id,
            "booking_id": self.__booking_id,
            "rating": self.__rating,
            "comment": self.__comment,
            "created_at": self.__created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
