#MakePayment

from fastapi import FastAPI , HTTPException
from abc import ABC, abstractmethod
from datetime import datetime, date

from state import PurchaseStatus

class System:
    def __init__(self):
        self.__promotions = []
        self.__selected_coupons = {}

    def request_payment(self, user, booking):
        items, base = booking.unpaid_items
        promo = max([p.valid_promotion(base) for p in self.__promotions], default=0)
        member = user.calculate_membership()
        item_list = [(item.item_id, item.__class__.__name__, item.price) for item in items]
        return {
            "items": item_list,
            "base_price": base,
            "promotion_discount": promo,
            "membership_discount": member,
            "available_coupons": [c.code for c in user.coupon_list()]
        }

    def select_coupon(self, user, booking, coupon_code):
        items, base = booking.unpaid_items
        promo = max([p.valid_promotion(base) for p in self.__promotions], default=0)
        member = user.calculate_membership()

        coupon_value = 0
        for coupon in user.coupons:
            if coupon_code and coupon.validate_coupon(coupon_code):
                coupon_value = coupon.discount
                break

        final_price = booking.calculate_price(base, promo, member, coupon_value)
        self.__selected_coupons[booking.booking_id] = coupon_code

        return {
            "base_price": base,
            "promotion_discount": promo,
            "membership_discount": member,
            "coupon_discount": coupon_value,
            "final_price": final_price
        }

    def submit_slip_number(self, user, booking, slip):
        items, base = booking.unpaid_items
        if base == 0:
            raise HTTPException(400, "Nothing to pay")

        coupon_code = self.__selected_coupons.get(booking.booking_id)
        promo = max([p.valid_promotion(base) for p in self.__promotions], default=0)
        member = user.calculate_membership()

        coupon_value = 0
        used_coupon = None
        for coupon in user.coupons:
            if coupon_code and coupon.validate_coupon(coupon_code):
                coupon_value = coupon.discount
                used_coupon = coupon
                break

        final_price = booking.calculate_price(base, promo, member, coupon_value)

        if not Bank.verify_transfer(slip):
            raise HTTPException(400, "Transfer failed")

        booking.mark_items_paid(items, final_price)

        if used_coupon:
            used_coupon.set_used(True)

        return Payment.generate_receipt(items, final_price)
    
class Booking:
    def __init__(self, booking_id, user):
        self.__booking_id = booking_id
        self.__user = user
        self.__purchase_status = PurchaseStatus.BOOKING
        self.__residencebooking_list = []
        self.__vehiclebooking_list = []
        self.__activitybooking_list = []
        self.__damage_list = []
        
    @property
    def booking_id(self):
        return self.__booking_id
    
    @property
    def unpaid_items(self):
        all_items = (self.__residencebooking_list + self.__vehiclebooking_list +
                     self.__activitybooking_list + self.__damage_list)
        unpaid = [item for item in all_items if not item.paid]
        total_price = sum(item.price for item in unpaid)
        return unpaid, total_price
    
    def calculate_price(self, base, promo, member_discount_rate, coupon_value):
        total = base - promo
        total -= (total * member_discount_rate)
        total -= coupon_value
        return max(total, 0)
    
    def mark_items_paid(self, items, final_price):
        for item in items:
            item.mark_paid()
        self.__user.add_spent(final_price)
        all_booked_items = (self.__residencebooking_list +
                            self.__vehiclebooking_list +
                            self.__activitybooking_list +
                            self.__damage_list)
        if all(item.paid for item in all_booked_items):
            self.__purchase_status = PurchaseStatus.COMPLETED

class Payment:
    # abstactmethod
    @staticmethod
    def generate_receipt(items, total_amount):
        item_list = [(item.item_id, item.__class__.__name__, item.price) for item in items]
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": item_list,
            "total_amount": round(total_amount, 2)
        }
    
class Bank:
    # verify
    @staticmethod
    def verify_transfer(slip):
        return slip and slip.startswith("OK")
    
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
    
class User(ABC):
    def __init__(self, user_name, user_id, driver_license):
        self._user_name = user_name
        self._user_id = user_id
        self._driver_license = driver_license

class Customer(User):
    def __init__(self, user_name, user_id, user_mail, password, age, driver_license):
        super().__init__(user_name, user_id, driver_license)
        self.__membership = "Bronze"
        self.__coupons = []
        self.__total_spent = 0

    @property
    def coupons(self):
        return self.__coupons

    def calculate_membership(self):
        if self.__membership == "Gold":
            return 0.10
        elif self.__membership == "Silver":
            return 0.05
        return 0.0
    
    def coupon_list(self):
        return [c for c in self.__coupons if not c.is_used]
    
    def add_spent(self, amount):
        self.__total_spent += amount
        if self.__total_spent >= 50000:
            self.__membership = "Gold"
        elif self.__total_spent >= 20000:
            self.__membership = "Silver"

# #--------------Test-------------------
# class MockItem:

#     def __init__(self, item_id, price):
#         self.item_id = item_id
#         self.price = price
#         self.paid = False

#     def mark_paid(self):
#         self.paid = True

# from datetime import date, timedelta


# def setup_mock_data():

#     print("\n========== SETUP MOCK DATA ==========")

#     system = System()

#     user = Customer("John","U001","mail","123",25,"Have")

#     booking = Booking("B001",user)

#     # items
#     item1 = MockItem("R001",1000)
#     item2 = MockItem("V001",500)

#     booking._Booking__residencebooking_list.append(item1)
#     booking._Booking__vehiclebooking_list.append(item2)

#     # promotion
#     promo = Promotion(
#         0.10,
#         500,
#         date.today()+timedelta(days=5)
#     )

#     system._System__promotions = [promo]

#     # coupon
#     coupon = Coupon(
#         "SALE50",
#         50,
#         date.today()+timedelta(days=5)
#     )

#     user.coupons.append(coupon)

#     return system,user,booking

# def test_request_payment(system,user,booking):

#     try:

#         result = system.request_payment(user,booking)

#         print("SUCCESS")
#         print(result)

#     except HTTPException as e:

#         print("FAILED")
#         print(e.detail)

# def test_select_coupon(system,user,booking,coupon):

#     try:

#         result = system.select_coupon(user,booking,coupon)

#         print("SUCCESS")
#         print(result)

#     except HTTPException as e:

#         print("FAILED")
#         print(e.detail)

# def test_submit_payment(system,user,booking,slip):

#     try:

#         result = system.submit_slip_number(user,booking,slip)

#         print("SUCCESS")
#         print(result)

#     except HTTPException as e:

#         print("FAILED")
#         print(e.detail)

# def run_tests():

#     print("\n========== TEST MAKE PAYMENT ==========")

#     # TEST 1
#     system,user,booking = setup_mock_data()
#     print("\n[TEST 1] Request Payment Summary")
#     test_request_payment(system,user,booking)

#     # TEST 2
#     system,user,booking = setup_mock_data()
#     print("\n[TEST 2] Select Valid Coupon")
#     test_select_coupon(system,user,booking,"SALE50")

#     # TEST 3
#     system,user,booking = setup_mock_data()
#     print("\n[TEST 3] Select Invalid Coupon")
#     test_select_coupon(system,user,booking,"BADCODE")

#     # TEST 4
#     system,user,booking = setup_mock_data()
#     print("\n[TEST 4] Submit Payment Success")
#     system.select_coupon(user, booking, "SALE50")
#     test_submit_payment(system,user,booking,"OK123456")

#     # TEST 5
#     system,user,booking = setup_mock_data()
#     print("\n[TEST 5] Submit Payment Transfer Failed")
#     test_submit_payment(system,user,booking,"FAIL123")

#     # TEST 6
#     system,user,booking = setup_mock_data()
#     print("\n[TEST 6] Nothing To Pay")

#     for item in booking._Booking__residencebooking_list + booking._Booking__vehiclebooking_list:
#         item.paid = True

#     test_submit_payment(system,user,booking,"OK999")

# if __name__ == "__main__":
#     run_tests()