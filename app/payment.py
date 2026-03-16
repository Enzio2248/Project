from datetime import datetime, date
from otherclass import DamageItem 
from booking import Residencebooking , Vehiclebooking , Activitybooking

# --------------------------------------------------
class Payment:
    # abstactmethod
    @staticmethod
    def generate_receipt(items:list[DamageItem , Residencebooking , Vehiclebooking , Activitybooking], total_amount):
        item_list = [(item.item_id, item.__class__.__name__, item.price) for item in items]
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": item_list,
            "total_amount": round(total_amount, 2)
        }

class Bank:
    # verify
    @staticmethod
    def verify_transfer(slip : str):
        return slip and slip.startswith("OK")

class Coupon:
    def __init__(self, code, discount, expiry):
        self.__code = code
        self.__discount = discount
        self.__expiry = expiry
        self.__used = False

    # validate
    def validate_coupon(self, coupon_code):
        return (
            self.__code == coupon_code
            and not self.__used
            and date.today() <= self.__expiry
        )
    
    # getter / setter
    def set_used(self, value):
        self.__used = value

    @property
    def code(self):
        return self.__code

    @property
    def discount(self):
        return self.__discount

    @property
    def is_used(self):
        return self.__used

class Promotion:
    def __init__(self, discount_rate, min_price, expiry):
        self.__discount_rate = discount_rate
        self.__min_price = min_price
        self.__expiry = expiry

    # validate
    def valid_promotion(self, base_price):
        if base_price >= self.__min_price and date.today() <= self.__expiry:
            return base_price * self.__discount_rate
        return 0
