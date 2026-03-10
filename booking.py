from otherclass import DamageItem
from state import PurchaseStatus 
import uuid
# --------------------------------------------------
class Booking:
    def __init__(self,  user):
        self.__booking_id = f"booking-{uuid.uuid4().hex}"
        self.__user = user
        self.__purchase_status = PurchaseStatus.BOOKING
        self.__residencebooking_list = []
        self.__vehiclebooking_list = []
        self.__activitybooking_list = []
        self.__damage_list = []
    
    # add resource and daamage 
    def add_residencebooking_list(self, residencebooking):
        self.__residencebooking_list.append(residencebooking)

    def add_vehiclebooking_list(self, vehiclebooking):
        self.__vehiclebooking_list.append(vehiclebooking)

    def add_activitybooking_list(self, activitybooking):
        self.__activitybooking_list.append(activitybooking)

    def add_damage(self, damage_id, description, price):
        damage = DamageItem(damage_id, description, price)
        self.__damage_list.append(damage)
        return damage.damage_detail

    # comfirm and cancle
    def confirm(self):
        self.__purchase_status = PurchaseStatus.COMPLETED

    def cancel(self):
        self.__purchase_status = PurchaseStatus.CANCELLED

    # show
    def show_all(self):
        print("\n============ Booking List ============")
        print("--- Residence Bookings ---")
        for rb in self.__residencebooking_list:
            print(f"ID: {rb.item_id} | User: {rb.user.user_name} | Room: {rb.room.room_id} | {rb.time.start_date} → {rb.time.end_date}")
        print("\n--- Vehicle Bookings ---")
        for vb in self.__vehiclebooking_list:
            print(f"ID: {vb.item_id} | User: {vb.user.user_name} | Vehicle: {vb.vehicle.vehicle_id}")
        print("\n--- Activity Bookings ---")
        for ab in self.__activitybooking_list:
            print(f"ID: {ab.item_id} | User: {ab.user.user_name} | Activity: {ab.activity.activity_id}")
        print("======================================\n")

    # check room and calculate price
    def start_room_inspection(self):
        if self.__residencebooking_list:
            self.__purchase_status = PurchaseStatus.INSPECTING
            return f"Booking {self.__booking_id}: Inspection started."
        return "No residence booking found"

    def update_status(self, status):
        self.__purchase_status = status

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

    # getter / setter
    @property
    def booking_id(self):
        return self.__booking_id

    @property
    def user_id(self):
        return self.__user.user_id

    @property
    def purchase_status(self):
        return self.__purchase_status

    @property
    def residencebooking_list(self):
        return self.__residencebooking_list

    @property
    def vehiclebooking_list(self):
        return self.__vehiclebooking_list

    @property
    def activitybooking_list(self):
        return self.__activitybooking_list

    @property
    def unpaid_items(self):
        all_items = (self.__residencebooking_list + self.__vehiclebooking_list +
                     self.__activitybooking_list + self.__damage_list)
        unpaid = [item for item in all_items if not item.paid]
        total_price = sum(item.price for item in unpaid)
        return unpaid, total_price

    @property
    def detail(self):
        if not self.__residencebooking_list:
            return {"message": "No residence booking"}
        first_res = self.__residencebooking_list[0]
        return {
            "booking_id": self.__booking_id,
            "user": self.__user.user_name,
            "residence": first_res.room.room_id,
            "start_date": first_res.time.start_date,
            "end_date": first_res.time.end_date,
        }

    @property
    def booking_item(self):
        if self.__residencebooking_list:
            return self.__residencebooking_list[0].detail()
        return None

class Residencebooking:
    def __init__(self, residence, room, user, time, price):
        self.__id = f"rb-{uuid.uuid4().hex}"
        self.__user = user
        self.__residence = residence
        self.__room = room
        self.__time = time
        self.__price = price
        self.__status = PurchaseStatus.BOOKING
        self.__paid = False
    
    # detail
    def detail(self):
        return {
            "booking_id": self.__id,
            "residence_name": self.__residence.residence_name,
            "room_id": self.__room.room_id,
            "customer": self.__user.user_name,
            "period": f"{self.__time.start_date} to {self.__time.end_date}",
            "total_price": self.__price,
            "paid_status": self.__paid
        }
    
    # update status
    def update_status(self, status):
        self.__status = status

    def mark_paid(self):
        self.__paid = True

    # getter / setter
    @property
    def item_id(self): 
        return self.__id

    @property
    def user(self):
        return self.__user

    @property
    def room(self): 
        return self.__room

    @property
    def time(self): 
        return self.__time

    @property
    def price(self): 
        return self.__price

    @property
    def paid(self): 
        return self.__paid

    @property
    def purchase_status(self): 
        return self.__status

class Vehiclebooking:
    def __init__(self, vehicle, user, time, staff_driver, price):
        self.__id = f"vb-{uuid.uuid4().hex}"
        self.__user = user
        self.__vehicle = vehicle
        self.__time = time
        self.__driver = staff_driver
        self.__price = price
        self.__status = PurchaseStatus.BOOKING
        self.__paid = False

    # update status
    def mark_paid(self):
        self.__paid = True

    def update_status(self, status):
        self.__status = status

    # detail
    def detail(self):
        return {
            "booking_id": self.__id,
            "vehicle": self.__vehicle.vehicle_id,
            "driver": self.__driver.user_name if self.__driver else "Self-Drive",
            "period": f"{self.__time.start_date} to {self.__time.end_date}",
            "price": self.__price,
            "is_paid": self.__paid
        }

    # getter / setter
    @property
    def item_id(self): 
        return self.__id

    @property
    def user(self): 
        return self.__user

    @property
    def vehicle(self): 
        return self.__vehicle

    @property
    def time(self): 
        return self.__time

    @property
    def driver(self): 
        return self.__driver

    @property
    def price(self): 
        return self.__price

    @property
    def paid(self): 
        return self.__paid

    @property
    def purchase_status(self): 
        return self.__status

class Activitybooking:
    def __init__(self, id, activity, user, time):
        self.__id = f"ab-{uuid.uuid4().hex}"
        self.__user = user
        self.__activity = activity
        self.__time = time
        self.__price = activity.price
        self.__status = PurchaseStatus.BOOKING
        self.__paid = False

    # update status
    def mark_paid(self):
        self.__paid = True

    def update_status(self, status):
        self.__status = status

    # detail
    def detail(self):
        return {
            "booking_id": self.__id,
            "activity_name": self.__activity.__class__.__name__,
            "user": self.__user.user_name,
            "price": self.__price,
            "status": self.__status
        }

    # getter / setter
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

    @property
    def price(self): 
        return self.__price

    @property
    def paid(self): 
        return self.__paid

    @property
    def purchase_status(self): 
        return self.__status
