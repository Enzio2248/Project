from fastapi import FastAPI , HTTPException
from abc import ABC, abstractmethod
from datetime import datetime, date
from enum import Enum
from pydantic import BaseModel
import re

from otherclass import TimeSlot , Review 
from payment import Payment , Bank , Promotion , Coupon
from booking import Booking , Residencebooking , Vehiclebooking , Activitybooking
from user import Customer , Staff , Manager
from residence import Residence 
from vehicle import Vehicle
from activity import Activity
from state import PurchaseStatus , StaffStatus , LogInStatus , OperationalStatus , ServiceStatus
# ----------------------------------------------------
class System:
    def __init__(self):
        self.__customer_list : list[Customer] = []
        self.__staff_list : list[Staff] = []
        self.__manager_list : list[Manager]= []
        self.__residence_list : list[Residence] = []
        self.__vehicle_list : list[Vehicle] = []
        self.__activity_list : list[Activity] = []
        self.__bookings : list[Booking] = []           
        self.__promotions : list[Promotion] = []
        self.__selected_coupons : dict[str, Coupon] = {}   
        self.__reviews : list[Review]= []          

    def is_manager(self, manager_id: str) -> bool:
        for manager in self.__manager_list:
            if(manager.user_id == manager_id):
                return True
            return False
        
    def add_customer(self, customer):
        self.__customer_list.append(customer)

    # authenticate & register
    def authenticate(self,user):
        if isinstance(user, Customer):
            for customer in self.__customer_list:
                if customer.email == user.email and customer.check_password(user.password):
                    if customer.is_banned:
                        raise HTTPException(status_code=403, detail="This account has been banned")
                    customer.login_status = LogInStatus.ONLINE
                    return {"message": "Login successful"}
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        else: raise HTTPException(status_code=401, detail="Type Error")


    def register(self, user_name, user_mail, password, age, driver_license):
        if "@" not in user_mail:
            raise HTTPException(status_code=400, detail="Invalid email format (must contain @)")
        if len(password) < 9:
            raise HTTPException(status_code=400, detail="Password must be longer than 9 characters")
        if not re.search(r"[A-Z]", password):
            raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter")
        if not re.search(r"\d", password):
            raise HTTPException(status_code=400, detail="Password must contain at least one digit")
        for existing_user in self.__customer_list:
            if existing_user.email == user_mail:
                raise HTTPException(status_code=400, detail="User ID or Email already exists")
        new_user = Customer(user_name, user_mail, password, age, driver_license)
        self.__customer_list.append(new_user)
        return {"message": "User registered successfully"}

    # add resource by manager
    def add_residence(self, residence, manager_id):
        if not self.is_manager(manager_id):
            raise HTTPException(status_code=403, detail="Permission denied: Only managers can add activities")
        if not isinstance(residence, Residence):
            raise HTTPException(status_code=400, detail="Invalid Residence object")
        for existing in self.__residence_list:
            if existing.residence_id == residence.residence_id:
                raise HTTPException(status_code=400, detail="Residence ID already exists")
        if len(residence.room_list) == 0:
            print("Warning: Adding a residence with no rooms")
        self.__residence_list.append(residence)
        return {"message": f"Residence {residence.residence_name} added successfully"}

    def add_vehicle(self, vehicle, manager_id):
        if not isinstance(vehicle, Vehicle):
            raise HTTPException(status_code=403, detail="vehicle type Error")
        if not self.is_manager(manager_id):
            raise HTTPException(status_code=403, detail="Permission denied: Only managers can add activities")
        if any(v.vehicle_id == vehicle.vehicle_id for v in self.__vehicle_list):
            raise HTTPException(status_code=400, detail="Vehicle ID already exists")
        if vehicle.capacity <= 0:
            raise HTTPException(status_code=400, detail="Capacity must be greater than 0")
        self.__vehicle_list.append(vehicle)

    def add_activity(self, manager_id, activity):
        if not isinstance(activity, Activity):
            raise HTTPException(status_code=403, detail="activity type Error")
        if not self.is_manager(manager_id):
            raise HTTPException(status_code=403, detail="Permission denied: Only managers can add activities")
        if not isinstance(activity, Activity):
            raise HTTPException(status_code=400, detail="Invalid Activity object")
        if any(a.activity_id == activity.activity_id for a in self.__activity_list):
            raise HTTPException(status_code=400, detail="Activity ID already exists")
        self.__activity_list.append(activity)
        return {"message": f"Activity '{activity.activity_id}' added successfully"}

    # staff & manager
    def add_staff(self, staff):
        if not isinstance(staff, Staff):
            raise HTTPException(status_code=400, detail="Object is not an instance of Staff")
        all_ids = [s.staff_id for s in self.__staff_list] + [m.staff_id for m in self.__manager_list]
        if staff.staff_id in all_ids:
            raise HTTPException(status_code=400, detail=f"Staff ID {staff.staff_id} already exists")
        self.__staff_list.append(staff)
        return {"message": f"Staff {staff.staff_name} added successfully"}

    def add_manager(self, manager):
        if not isinstance(manager, Manager):
            raise HTTPException(status_code=400, detail="Object is not an instance of manager")
        all_ids = [s.staff_id for s in self.__staff_list] + [m.staff_id for m in self.__manager_list]
        if manager.staff_id in all_ids:
            raise HTTPException(status_code=400, detail=f"Manager ID {manager.staff_id} already exists")
        self.__manager_list.append(manager)
        return {"message": f"Manager {manager.staff_name} added successfully"}

    # add booking
    def add_booking(self, booking):
        if not isinstance(booking, Booking):
            raise HTTPException(status_code=400, detail="Object must be an instance of Booking")
        if any(b.booking_id == booking.booking_id for b in self.__bookings):
            raise HTTPException(status_code=400, detail=f"Booking ID {booking.booking_id} already exists")
        self.__bookings.append(booking)
        return {"message": f"Booking {booking.booking_id} added to system"}

    def add_promotion(self, promotion):
        if not isinstance(promotion, Promotion):
            raise HTTPException(status_code=400, detail="Object must be an instance of Promotion")
        self.__promotions.append(promotion)
        return {"message": "Promotion added successfully"}

    # select create & ban 
    def validate_date(self, start_date, end_date):
        return (
            isinstance(start_date, (date, datetime))
            and isinstance(end_date, (date, datetime))
            and start_date < end_date
        )

    def create_booking(self, user_id):
        user = next((u for u in self.__customer_list if u.user_id == user_id),None)

        if not user :
            raise HTTPException(status_code=404, detail="User not found")
        
        if user.is_banned:
            raise HTTPException(status_code=403, detail="Banned users cannot make bookings")

        if user.login_status != LogInStatus.ONLINE:
            raise HTTPException(status_code=401, detail="User must be logged in ")
        

        new_booking = Booking(user)

        self.__bookings.append(new_booking)
        user.add_booking_list(new_booking)

        return {
            "booking_id": new_booking.booking_id,
            "user_id": user_id
        }

    def select_residence(self, residence_id, room_id):
        for residence in self.__residence_list:
            if residence.residence_id == residence_id:
                for room in residence.room_list:
                    if room.room_id == room_id:
                        return residence, room
        raise HTTPException(status_code=404, detail="Residence or Room not found")

    def create_residencebooking(self, user_id, booking_id , id, residence_id, room_id, start_date, end_date):
        if not self.validate_date(start_date, end_date):
            raise HTTPException(status_code=400, detail="Invalid booking dates")
        user = next((u for u in self.__customer_list if u.user_id == user_id), None)
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

        booking = None
        for b in self.__bookings:
            if b.booking_id == booking_id:
                booking = b
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        room.add_booking_list(new_residence_booking)
        user.add_booking_list(new_residence_booking)
        booking.add_residencebooking_list(new_residence_booking)
        return new_residence_booking

    def check_driver_license(self, driver_id):
        for driver in self.__staff_list:
            if driver.staff_id == driver_id:
                return driver.driver_license != ""
        raise HTTPException(status_code=400, detail="Error Check Driverlicense")

    def select_vehicle(self, vehicle_id):
        for vehicle in self.__vehicle_list:
            if isinstance(vehicle, Vehicle) and vehicle.vehicle_id == vehicle_id:
                return vehicle
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    def create_vehiclebooking(self, user_id, booking_id, b_id, vehicle_id, driver_id, start_date, end_date):
        if not self.validate_date(start_date, end_date):
            raise HTTPException(status_code=400, detail="Invalid booking dates")
        user = next((u for u in self.__customer_list if u.user_id == user_id), None)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.is_banned:
            raise HTTPException(status_code=403, detail="Banned users cannot make bookings")
        if user.login_status != LogInStatus.ONLINE:
            raise HTTPException(status_code=401, detail="User must be logged in to book")

        vehicle = self.select_vehicle(vehicle_id)

        if vehicle.service_status == ServiceStatus.INACTIVE:
            raise HTTPException(status_code=400, detail="Vehicle is currently out of service")
        if not vehicle.is_available(start_date, end_date):
            raise HTTPException(status_code=400, detail="Vehicle is already booked for these dates")
        
        booking = None
        for b in self.__bookings:
            if b.booking_id == booking_id:
                booking = b
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        staff_to_assign = None
        if user.driver_license == "Have":
            staff_to_assign = None
        else:
            if not driver_id:
                raise HTTPException(status_code=400, detail="Driver license required or please select a staff driver")
            staff_to_assign = next((s for s in self.__staff_list if s.staff_id == driver_id), None)
            if not staff_to_assign:
                raise HTTPException(status_code=404, detail="Staff driver not found")
            if not self.check_driver_license(driver_id):
                raise HTTPException(status_code=400, detail="The selected staff does not have a driver license")
            staff_to_assign.status = StaffStatus.BUSY

        time_slot = TimeSlot(start_date, end_date)
        new_vehicle_booking = Vehiclebooking(b_id, vehicle, user, time_slot, staff_driver=staff_to_assign, price=vehicle.price)

        vehicle.add_booking_list(new_vehicle_booking)
        user.add_booking_list(new_vehicle_booking)
        booking.add_vehiclebooking_list(new_vehicle_booking)
        return new_vehicle_booking

    def select_activity(self, activity_id):
        for activity in self.__activity_list:
            if isinstance(activity, Activity) and activity.activity_id == activity_id:
                return activity
        raise HTTPException(status_code=404, detail="Activity not found")

    def create_activitybooking(self, user_id, booking_id , b_id, activity_id, start_date, end_date):
        if not self.validate_date(start_date, end_date):
            raise HTTPException(status_code=400, detail="Error Validate Date")
        user = next((u for u in self.__customer_list if u.user_id == user_id), None)
        if not user:
            raise HTTPException(status_code=400, detail="Not Found User")
        if user.is_banned:
            raise HTTPException(status_code=403, detail="Banned users cannot make bookings")
        if user.login_status != LogInStatus.ONLINE:
            raise HTTPException(status_code=400, detail="User must be logged in to book an activity")

        booking = None
        for b in self.__bookings:
            if b.booking_id == booking_id:
                booking = b
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        activity = self.select_activity(activity_id)
        time_slot = TimeSlot(start_date, end_date)
        new_activity_booking = Activitybooking(b_id, activity, user, time_slot)

        activity.add_booking_list(new_activity_booking)
        user.add_booking_list(new_activity_booking)
        booking.add_activitybooking_list(new_activity_booking)
        return new_activity_booking

    def confirm_booking(self, staff_id, booking_id):
        staff_exists = any(s.staff_id == staff_id for s in self.__staff_list)
        
        booking = None
        for b in self.__bookings:
            if b.booking_id == booking_id:
                booking = b
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        if staff_exists:
            booking.confirm()
            return {"message": f"Booking {booking.booking_id} confirmed by staff {staff_id}"}
        raise HTTPException(status_code=400, detail="Confirmation failed: Authorized staff not found")

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
    
    def ban_user(self, manager_id, user_id):
        is_manager = any(m.staff_id == manager_id for m in self.__manager_list)
        if not is_manager:
            raise HTTPException(status_code=403, detail="Permission denied: Only managers can ban users")

        user = next((u for u in self.__customer_list if u.user_id == user_id), None)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.is_banned:
            raise HTTPException(status_code=400, detail="User is already banned")

        user.ban()
        user.login_status = LogInStatus.OFFLINE
        return {"message": f"User {user_id} has been banned"}

    def unban_user(self, manager_id, user_id):
        is_manager = any(m.staff_id == manager_id for m in self.__manager_list)
        if not is_manager:
            raise HTTPException(status_code=403, detail="Permission denied: Only managers can unban users")

        user = next((u for u in self.__customer_list if u.user_id == user_id), None)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.unban()
        return {"message": f"User {user_id} has been unbanned"}

    def create_review(self, user_id, booking_id, rating, comment):
        user = next((u for u in self.__customer_list if u.user_id == user_id), None)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.login_status != LogInStatus.ONLINE:
            raise HTTPException(status_code=401, detail="User must be logged in to write a review")

        booking = self._get_booking(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        if booking.purchase_status != PurchaseStatus.COMPLETED:
            raise HTTPException(status_code=400, detail="Can only review completed bookings")
        if booking.user_id != user_id:
            raise HTTPException(status_code=403, detail="Can only review your own bookings")

        if any(r.booking_id == booking_id for r in self.__reviews):
            raise HTTPException(status_code=400, detail="You have already reviewed this booking")

        if not (1 <= rating <= 5):
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

        review = Review (user_id, booking_id, rating, comment)
        self.__reviews.append(review)
        return {"message": "Review created successfully", "review_id": review.review_id}

    def process_expired_bookings(self):
        today = date.today()
        expired_count = 0

        for booking in self.__bookings:
            for rb in booking.residencebooking_list:
                end = rb.time.end_date
                end_date = end.date() if isinstance(end, datetime) else end
                if end_date < today and rb.purchase_status == PurchaseStatus.BOOKING:
                    rb.update_status(PurchaseStatus.EXPIRED)
                    rb.room.update_operational_status(OperationalStatus.CLEANING)
                    expired_count += 1

            for vb in booking.vehiclebooking_list:
                end = vb.time.end_date
                end_date = end.date() if isinstance(end, datetime) else end
                if end_date < today and vb.purchase_status == PurchaseStatus.BOOKING:
                    vb.update_status(PurchaseStatus.EXPIRED)
                    if vb.driver:
                        vb.driver.complete_work()
                    expired_count += 1

            for ab in booking.activitybooking_list:
                end = ab.time.end_date
                end_date = end.date() if isinstance(end, datetime) else end
                if end_date < today and ab.purchase_status == PurchaseStatus.BOOKING:
                    ab.update_status(PurchaseStatus.EXPIRED)
                    expired_count += 1

        return {"message": f"Processed {expired_count} expired bookings"}

    def search_manager_by_id(self , manager):
        if not isinstance(manager , Manager):
            raise HTTPException(status_code=400, detail="invalid manager object")
        for managers in self.__manager_list:
            if managers.staff_id == manager.staff_id:
                return manager
    # check room
    def _get_booking(self, booking_id):
        for booking in self.__bookings:
            if booking.booking_id == booking_id:
                return booking
        return None

    def start_room_inspection(self, booking_id):
        booking = self._get_booking(booking_id)
        if not booking:
            return {"error": "Booking not found"}
        return {"message": booking.start_room_inspection()}
    
    def add_damage(self, booking_id, description, price):
        booking = self._get_booking(booking_id)
        if not booking:
            return {"error": "Booking not found"}
        damage = booking.add_damage(description, price)
        return {"damage_recorded": damage}

    def confirm_inspection_complete(self, booking_id, damaged=False):
        booking = self._get_booking(booking_id)
        if not booking:
            return {"error": "Booking not found"}
        if damaged:
            booking.update_status("wait_damage_payment")
        else:
            booking.update_status("wait_checkout_payment")
        return {"message": "inspection finished"}

    # payment
    def request_payment(self, user, booking):
        if not isinstance(user , Customer):
            raise HTTPException(status_code=400, detail="invalid manager object")
        if not isinstance(booking , Booking):
            raise HTTPException(status_code=400, detail="invalid manager object")
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

    def select_coupon(self, user_id, booking_id, coupon_code):
        user = None
        for u in self.__customer_list:
            if u.user_id == user_id:
                user = u
        if not user:
            raise HTTPException(status_code=404, detail="user not found")

        booking = None
        for b in self.__bookings:
            if b.booking_id == booking_id:
                booking = b
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

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

    def submit_slip_number(self, user_id, booking_id , slip):
        user = None
        for u in self.__customer_list:
            if u.user_id == user_id:
                user = u
        if not user:
            raise HTTPException(status_code=404, detail="user not found")

        booking = None
        for b in self.__bookings:
            if b.booking_id == booking_id:
                booking = b
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

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
    
    # getter / setter
    @property
    def promotions(self):
        return self.__promotions

    @property
    def reviews(self):
        return self.__reviews
