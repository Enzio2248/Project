# data / mock_data

from datetime import date, timedelta

# LOGIN
from Login import System as LoginSystem, Customer as LoginCustomer

# REGISTER
from Register import System as RegisterSystem, Customer as RegisterCustomer

# CREATE BOOKING
from CreateBooking import System as BookingSystem, Customer as BookingCustomer

# RESIDENCE
from BookResidence import (
    System as ResidenceSystem,
    Customer as ResidenceCustomer,
    Residence,
    NormalRoom,
    KingRoom,
    Booking as ResidenceBooking
)

# VEHICLE
from BookVehicle import (
    System as VehicleSystem,
    Customer as VehicleCustomer,
    Staff as VehicleStaff,
    Car,
    Motorcycle,
    Booking as VehicleBooking
)

# ACTIVITY
from BookActivity import (
    System as ActivitySystem,
    Customer as ActivityCustomer,
    Driving,
    Hiking,
    Booking as ActivityBooking
)

# CANCEL BOOKING
from CancelBooking import (
    System as CancelSystem,
    Booking as CancelBooking,
    Residencebooking,
    Vehiclebooking,
    Activitybooking,
    Staff as CancelStaff,
    Room,
    Vehicle
)

# PAYMENT
from MakePayment import (
    System as PaymentSystem,
    Booking as PaymentBooking,
    Promotion,
    Coupon,
    Customer as PaymentCustomer
)

from ConfirmBooking import System as ConfirmSystem, Staff, Booking

from StartInspection import System as InspectionSystem
from StartInspection import Booking as InspectionBooking
from StartInspection import Staff
from StartInspection import MockResidenceBooking

from WriteReview import System, Customer, Booking

from state import LogInStatus, PurchaseStatus

def setup_login_mock():

    system = LoginSystem()

    user1 = LoginCustomer("User1", "U001", "user1@gmail.com", "Password123", 25, "Have")
    user2 = LoginCustomer("User2", "U002", "user2@gmail.com", "Password456", 30, "None")
    user3 = LoginCustomer("User3", "U003", "banned@gmail.com", "Password789", 40, "Have")

    user3._Customer__is_banned = True

    system.add_user(user1)
    system.add_user(user2)
    system.add_user(user3)

    return system

def setup_register_mock():

    system = RegisterSystem()

    system._System__user_list = [
        RegisterCustomer("John", "U001", "john@gmail.com", "Password123", 25, "DL001"),
        RegisterCustomer("Jane", "U002", "jane@gmail.com", "Password456", 22, "DL002")
    ]

    return system

def setup_booking_mock():

    system = BookingSystem()

    user1 = BookingCustomer("John", "U001", "john@gmail.com", "Password123", 25, "DL001")
    user2 = BookingCustomer("Jane", "U002", "jane@gmail.com", "Password456", 22, "DL002")
    user3 = BookingCustomer("Mike", "U003", "mike@gmail.com", "Password789", 30, "DL003")

    user1.login_status = LogInStatus.ONLINE

    user3.login_status = LogInStatus.ONLINE
    user3.ban_user()

    system._System__user_list = [user1, user2, user3]

    return system

def setup_residence_mock():

    system = ResidenceSystem()

    user1 = ResidenceCustomer("U001")
    user2 = ResidenceCustomer("U002")
    user3 = ResidenceCustomer("U003")

    user1.login_status = LogInStatus.ONLINE

    user3.login_status = LogInStatus.ONLINE
    user3.ban_user()

    system._System__user_list = [user1, user2, user3]

    res1 = Residence("R001", "Sea Resort")

    room1 = NormalRoom("RM01")
    room2 = KingRoom("RM02")

    res1.room_list.append(room1)
    res1.room_list.append(room2)

    system._System__residence_list = [res1]

    booking = ResidenceBooking("B001", user1)

    return system, booking

def setup_vehicle_mock():

    system = VehicleSystem()

    user1 = VehicleCustomer("John","U001","john@mail","123",25,"Have")
    user2 = VehicleCustomer("Jane","U002","jane@mail","123",25,"None")

    user1.login_status = LogInStatus.ONLINE
    user2.login_status = LogInStatus.ONLINE

    system._System__user_list = [user1,user2]

    staff1 = VehicleStaff("DriverA","S001","Have")   # แก้ตรงนี้

    system._System__staff_list = [staff1]

    car1 = Car("V001")
    bike1 = Motorcycle("V002")

    system._System__vehicle_list = [car1,bike1]

    booking = VehicleBooking("B001",user1)

    return system, booking


# =========================
# ACTIVITY MOCK
# =========================
def setup_activity_mock():

    system = ActivitySystem()

    user1 = ActivityCustomer("Alice","U001","alice@mail","123",30,True)
    user2 = ActivityCustomer("Bob","U002","bob@mail","123",20,False)

    user1.login()
    user2.login()

    system._System__user_list = [user1,user2]

    act1 = Driving("A001")
    act2 = Hiking("A002")

    system._System__activity_list = [act1,act2]

    booking = ActivityBooking("B001",user1)

    return system, booking

class DummyActivity:

    def __init__(self):
        self.price = 100

    def remove_booking(self, booking):
        pass


class DummyRoom(Room):

    def __init__(self, room_id):
        super().__init__(room_id, 2)


class DummyVehicle(Vehicle):

    def __init__(self, vehicle_id):
        super().__init__(vehicle_id, 4)


def setup_cancel_mock():

    system = CancelSystem()

    user1 = CancelStaff("John", "U001", "Have")
    driver = CancelStaff("Driver", "U002", "Have")
    manager = CancelStaff("Boss", "M001", "Have")

    system._CancelSystem__manager_list = [manager]

    room = DummyRoom("R001")
    vehicle = DummyVehicle("V001")
    activity = DummyActivity()

    booking = CancelBooking("B001", user1)

    rb = Residencebooking("RB001", None, room, user1, None, 100)
    booking.residencebooking_list.append(rb)

    vb = Vehiclebooking("VB001", vehicle, user1, None, driver, 200)
    booking.vehiclebooking_list.append(vb)

    ab = Activitybooking("AB001", activity, user1, None)
    booking.activitybooking_list.append(ab)

    system._CancelSystem__booking_list = [booking]

    return system

def setup_payment_mock():

    system = PaymentSystem()

    user = PaymentCustomer("John","U001","mail","123",25,"Have")

    booking = PaymentBooking("B001", user)

    class MockItem:

        def __init__(self,item_id,price):
            self.item_id = item_id
            self.price = price
            self.paid = False

        def mark_paid(self):
            self.paid = True

    item1 = MockItem("R001",1000)
    item2 = MockItem("V001",500)

    booking._Booking__residencebooking_list.append(item1)
    booking._Booking__vehiclebooking_list.append(item2)

    promo = Promotion(
        0.10,
        500,
        date.today()+timedelta(days=5)
    )

    system._PaymentSystem__promotions = [promo]

    coupon = Coupon(
        "SALE50",
        50,
        date.today()+timedelta(days=5)
    )

    user.coupons.append(coupon)

    return system, user, booking

def setup_confirm_mock():

    system = ConfirmSystem()

    staff1 = Staff("Alice", "S001", "DL111")
    staff2 = Staff("Bob", "S002", "DL222")

    system.add_staff(staff1)
    system.add_staff(staff2)

    user = Staff("MockUser", "U001", "DL999")

    booking = Booking("B001", user)

    return system, booking

def setup_inspection_mock():

    inspection_system = InspectionSystem()

    staff = Staff("Alice", "S001", "DL111")

    user = Staff("MockUser", "U001", "DL999")

    booking = InspectionBooking("B001", user)

    residence = MockResidenceBooking("R001")

    booking._Booking__residencebooking_list.append(residence)
    
    inspection_system.add_booking(booking)

    return inspection_system, booking

def setup_review_mock():

    system = System()

    user = Customer(
        "Alice",
        "U001",
        "a@mail",
        "1234",
        25,
        "DL111"
    )

    # force login
    user._Customer__login_status = LogInStatus.ONLINE

    booking = Booking("B001", user)

    # make booking completed
    booking._Booking__purchase_status = PurchaseStatus.COMPLETED

    system.add_user(user)
    system.add_booking(booking)

    return system, user, booking