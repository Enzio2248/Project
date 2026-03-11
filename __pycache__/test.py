from enum import Enum

# -------------------------------------------------- 
class LogInStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"

class OperationalStatus(Enum):
    READY = "ready"
    REPAIR = "repair"
    CLEANING = "cleaning"

class ServiceStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class StaffStatus(Enum):
    FREE = "free"
    BUSY = "busy"

class PurchaseStatus(Enum):
    BOOKING = "booking"
    INSPECTING = "inspecting"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    EXPIRED = "expired"


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

        self.__user_counter = 1
        self.__residencebooking_counter = 1

    def is_manager(self, manager_id: str) -> bool:
        for manager in self.__manager_list:
            if manager.staff_id == manager_id:
                return True
        return False
        
    def add_customer(self, customer):
        self.__customer_list.append(customer)

    # authenticate & register
    def authenticate(self, email, password):
        for user in self.__customer_list:
            if user.email == email and user.check_password(password):
                if user.is_banned:
                    raise HTTPException(status_code=403, detail="This account has been banned")

                user.login_status = LogInStatus.ONLINE
                return {
                    "message": "Login success",
                    "user_id": user.user_id,
                    "name": user.user_name
                }

        raise HTTPException(status_code=401, detail="Invalid email or password")

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
        user_id = self.generate_user_id()

        new_customer = Customer(
            user_name,
            user_mail,
            password,
            age,
            driver_license
           )

        new_customer._user_id = user_id

        self.__customer_list.append(new_customer)

        return {"message": "User registered", "user_id": user_id}

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

    def create_residencebooking(self, user_id, booking_id, residence_id, room_id, start_date, end_date):

        if not self.validate_date(start_date, end_date):
            raise HTTPException(status_code=400, detail="Invalid booking dates")

        user = next((u for u in self.__customer_list if u.user_id == user_id), None)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.is_banned:
            raise HTTPException(status_code=403, detail="Banned users cannot make bookings")

        if user.login_status != LogInStatus.ONLINE:
            raise HTTPException(status_code=401, detail="User must be logged in")

        residence, room = self.select_residence(residence_id, room_id)

        if room.operational_status != OperationalStatus.READY:
            raise HTTPException(status_code=400, detail="Room is not ready")

        if not room.is_available(start_date, end_date):
            raise HTTPException(status_code=400, detail="Room already booked for these dates")

        booking = None
        for b in self.__bookings:
            if b.booking_id == booking_id:
                booking = b

        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        time_slot = TimeSlot(start_date, end_date)

        rb_id = self.generate_residencebooking_id()

        new_residence_booking = Residencebooking(
            residence,
            room,
            user,
            time_slot,
            room.price
        )

        room.add_booking_list(new_residence_booking)
        user.add_booking_list(new_residence_booking)
        booking.add_residencebooking_list(new_residence_booking)

        return {
            "message": "Residence booked successfully",
            "residence_booking_id": rb_id,
            "room_id": room.room_id,
            "residence_id": residence.residence_id
        }

    def check_driver_license(self, driver_id):
        for driver in self.__staff_list:
            if driver.staff_id == driver_id:
                return driver.driver_license != ""
        raise HTTPException(status_code=400, detail="Error Check Driverlicense")

    def select_vehicle(self, vehicle_id):

        print("vehicle list:", [v.vehicle_id for v in self.__vehicle_list])

        for vehicle in self.__vehicle_list:
            if vehicle.vehicle_id == vehicle_id:
                return vehicle

        raise HTTPException(status_code=404, detail="Vehicle not found")

    def create_vehiclebooking(self, user_id, booking_id, vehicle_id, driver_id, start_date, end_date):

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

        if not user.driver_license:

            if not driver_id:
                raise HTTPException(status_code=400, detail="Please select a staff driver")

            staff_to_assign = next((s for s in self.__staff_list if s.staff_id == driver_id), None)

            if not staff_to_assign:
                raise HTTPException(status_code=404, detail="Staff driver not found")

            if not self.check_driver_license(driver_id):
                raise HTTPException(status_code=400, detail="The selected staff does not have a driver license")

            staff_to_assign.status = StaffStatus.BUSY

        time_slot = TimeSlot(start_date, end_date)

        new_vehicle_booking = Vehiclebooking(
            vehicle,
            user,
            time_slot,
            staff_driver=staff_to_assign,
            price=vehicle.price
        )

        vehicle.add_booking_list(new_vehicle_booking)
        user.add_booking_list(new_vehicle_booking)
        booking.add_vehiclebooking_list(new_vehicle_booking)

        return {
            "message": "Vehicle booked successfully",
            "vehicle_id": vehicle.vehicle_id,
            "booking_id": booking.booking_id
        }

    def select_activity(self, activity_id):
        for activity in self.__activity_list:
            if isinstance(activity, Activity) and activity.activity_id == activity_id:
                return activity
        raise HTTPException(status_code=404, detail="Activity not found")

    def create_activitybooking(self, user_id, booking_id, activity_id, start_date, end_date):

        if not self.validate_date(start_date, end_date):
            raise HTTPException(status_code=400, detail="Error Validate Date")

        user = next((u for u in self.__customer_list if u.user_id == user_id), None)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.is_banned:
            raise HTTPException(status_code=403, detail="Banned users cannot make bookings")

        if user.login_status != LogInStatus.ONLINE:
            raise HTTPException(status_code=401, detail="User must be logged in to book an activity")

        booking = None
        for b in self.__bookings:
            if b.booking_id == booking_id:
                booking = b

        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        activity = self.select_activity(activity_id)

        time_slot = TimeSlot(start_date, end_date)

        new_activity_booking = Activitybooking(
            activity,
            user,
            time_slot
        )

        activity.add_booking_list(new_activity_booking)
        user.add_booking_list(new_activity_booking)
        booking.add_activitybooking_list(new_activity_booking)

        return {
            "message": "Activity booked successfully",
            "activity_id": activity.activity_id,
            "booking_id": booking.booking_id
        }
    
    def confirm_booking(self, staff_id, booking_id):

        staff_exists = any(s.staff_id == staff_id for s in self.__staff_list)
        manager_exists = any(m.staff_id == staff_id for m in self.__manager_list)

        booking = None
        for b in self.__bookings:
            if b.booking_id == booking_id:
                booking = b

        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        if staff_exists or manager_exists:
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
    def request_payment(self, user_id, booking_id):

        user = next((u for u in self.__customer_list if u.user_id == user_id), None)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        booking = self._get_booking(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
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

    def generate_user_id(self):

        user_id = f"U{self.__user_counter:03d}"
        self.__user_counter += 1

        return user_id
    
    def generate_residencebooking_id(self):
        
        rb_id = f"RB{self.__residencebooking_counter:03d}"
        self.__residencebooking_counter += 1

        return rb_id
    
class User(ABC):
    def __init__(self, user_name, driver_license):
        self._user_name = user_name
        self._user_id = f"user-{uuid.uuid4().hex}"
        self._driver_license = driver_license
    
    # getter / setter
    @property
    def user_name(self):
        return self._user_name

    @property
    def user_id(self):
        return self._user_id

    @property
    def driver_license(self):
        return self._driver_license
    
    @driver_license.setter
    def driver_license(self, value):
        self._driver_license = value

class Customer(User):
    def __init__(self, user_name, user_mail, password, age, driver_license = ""):
        super().__init__(user_name, driver_license)
        self.__user_mail = user_mail
        self.__password = password
        self.__membership = "Bronze"
        self.__age = age
        self.__booking_list : list["Booking"] = []
        self.__total_spent = 0
        self.__login_status = LogInStatus.OFFLINE
        self.__coupons : list["Coupon"] = []
        self.__is_banned = False

    def ban_user(self):
        self.__is_banned = True

    # edit and check password
    def edit_profile(self, name, email):
        self._user_name = name
        self.__user_mail = email
        return {"message": "Profile updated"}

    def check_password(self, password_input):
        return self.__password == password_input
    
    # ban user
    def ban(self):
        self.__is_banned = True

    def unban(self):
        self.__is_banned = False
    

    def login(self):
        self.__login_status = LogInStatus.ONLINE

    def logout(self):
        self.__login_status = LogInStatus.OFFLINE

    # get coupon list
    def coupon_list(self):
        return [c for c in self.__coupons if not c.is_used]

    # add 
    def add_booking_list(self, booking):
        self.__booking_list.append(booking)

    def add_coupon(self, coupon):
        self.__coupons.append(coupon)

    def add_spent(self, amount):
        self.__total_spent += amount
        if self.__total_spent >= 50000:
            self.__membership = "Gold"
        elif self.__total_spent >= 20000:
            self.__membership = "Silver"

    def calculate_membership(self):
        if self.__membership == "Gold":
            return 0.10
        elif self.__membership == "Silver":
            return 0.05
        return 0.0

    # getter / setter
    @property
    def is_banned(self):
        return self.__is_banned

    @property
    def email(self):
        return self.__user_mail

    @property
    def login_status(self):
        return self.__login_status
    
    @login_status.setter
    def login_status(self, status):
        self.__login_status = status

    @property
    def coupons(self):
        return self.__coupons
    
    @property
    def password(self):
        return self.__password
    
    @property
    def age(self):
        return self.__age   

    @login_status.setter
    def login_status(self, value):
        self.__login_status = value

class Staff(User):
    def __init__(self, user_name, driver_license):
        super().__init__(user_name, driver_license)
        self._status = StaffStatus.FREE

    # work update status
    def is_available_to_work(self):
        return self._status == StaffStatus.FREE

    def assign_work(self):
        if self.is_available_to_work():
            self._status = StaffStatus.BUSY
            return True
        return False

    def complete_work(self):
        self._status = StaffStatus.FREE
    
    # getter / setter 
    @property
    def staff_id(self):
        return self._user_id

    @property
    def staff_name(self):
        return self._user_name
    
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status_value):
        self._status = status_value

class Manager(Staff):
    def __init__(self, staff_name, driver_license):
        super().__init__(staff_name, driver_license)

class Residence:
    def __init__(self,residence_id ,  residence_name):
        self.__residence_id = residence_id
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
    def __init__(self, room_id,  capacity):
        self._room_id = room_id
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
    def __init__(self,room_id):
        super().__init__(room_id,capacity=2)
        self._price = 1000
    
    # getter / setter
    @property
    def price(self):
        return self._price

class KingRoom(Room):
    def __init__(self,room_id):
        super().__init__(room_id,capacity=4)
        self._price = 3000

    # getter / setter
    @property
    def price(self):
        return self._price

class Vehicle(ABC):
    def __init__(self, capacity, vehicle_id=None):
        self._vehicle_id = vehicle_id or f"ve-{uuid.uuid4().hex}"
        self._status = ServiceStatus.ACTIVE
        self._capacity = capacity
        self._booking_list: list["Vehiclebooking"] = []

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
    def __init__(self, vehicle_id=None):
        super().__init__(capacity=2, vehicle_id=vehicle_id)
        self._price = 100

    @property
    def price(self):
        return self._price

class Car(Vehicle):
    def __init__(self, vehicle_id=None):
        super().__init__(capacity=4, vehicle_id=vehicle_id)
        self._price = 500

    @property
    def price(self):
        return self._price
    
class Activity(ABC):
    def __init__(self, activity_id, min_age):
        self._activity_id = activity_id
        self._min_age = min_age
        self._booking_list : list["Activitybooking"] = []
        self._assigned_staff : list[Staff]= []

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
    
    def assign_staff(self, staff : Staff):
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
    def __init__(self):
        super().__init__("A001", min_age=25)
        self._price = 1000

    # getter /setter
    @property
    def price(self):
        return self._price

class Hiking(Activity):
    def __init__(self):
        super().__init__("A002", min_age=15)
        self._price = 1200

    # getter /setter
    @property
    def price(self):
        return self._price
    
class Booking:
    def __init__(self,  user):
        self.__booking_id = f"booking-{uuid.uuid4().hex}"
        self.__user : Customer = user
        self.__purchase_status = PurchaseStatus.BOOKING
        self.__residencebooking_list : list[Residencebooking]= []
        self.__vehiclebooking_list : list[Vehiclebooking]= []
        self.__activitybooking_list :list[Activitybooking] = []
        self.__damage_list : list[DamageItem] = []
    
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

    def mark_items_paid(self, items: list[Union[DamageItem, Residencebooking, Vehiclebooking, Activitybooking]], final_price):
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
        self.__user : User = user
        self.__residence : Residence = residence
        self.__room : Room = room
        self.__time :TimeSlot = time
        self.__price = price
        self.__status = PurchaseStatus.BOOKING
        self.__paid = False
    
    # detail
    def detail(self):
        return {
            "booking_id": self.__id,
            "residence_name": self.__residence.residence_name if self.__residence else "Unknown",
            "room_id": self.__room.room_id,
            "customer": self.__user.user_name,
            "period": (
                f"{self.__time.start_date} to {self.__time.end_date}"
                if self.__time else "No time slot"
            ),
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
        self.__user : User = user
        self.__vehicle : Vehicle = vehicle
        self.__time : TimeSlot = time
        self.__driver : Staff = staff_driver
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
    def __init__(self, activity : Activity, user, time):
        self.__id = f"ab-{uuid.uuid4().hex}"
        self.__user : User = user
        self.__activity : Activity = activity
        self.__time : TimeSlot = time
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

        start = self.__time.start_date if self.__time else None
        end = self.__time.end_date if self.__time else None

        return {
            "booking_id": self.__id,
            "activity_name": self.__activity.__class__.__name__,
            "user": self.__user.user_name,
            "start_date": start,
            "end_date": end,
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

class TimeSlot:
    def __init__(self, start_date, end_date):
        self.__start_date : datetime = start_date
        self.__end_date  : datetime = end_date
    
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
    def __init__(self, description, price):
        self.__damage_id = f"d-{uuid.uuid4().hex}"
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
