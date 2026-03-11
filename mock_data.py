from datetime import date, timedelta

from system import System
from user import Customer, Staff, Manager
from residence import Residence, Room, NormalRoom, KingRoom
from vehicle import Vehicle, Car, Motorcycle
from activity import Driving, Hiking
from booking import Booking, Residencebooking, Vehiclebooking, Activitybooking
from payment import Promotion, Coupon
from state import LogInStatus, PurchaseStatus


def setup_login_mock():

    system = System()

    # ---------------- Customers ----------------
    customer1 = Customer("User1", "user1@gmail.com", "Password123", 25, "Have")
    customer2 = Customer("User2", "user2@gmail.com", "Password456", 30)
    customer3 = Customer("User3", "banned@gmail.com", "Password789", 40, "Have")
    mike_customer = Customer("Mike", "mike@gmail.com", "Password789", 30, "DL003")

    system.add_customer(customer1)
    system.add_customer(customer2)
    system.add_customer(customer3)
    system.add_customer(mike_customer)

    customer3.ban_user()

    system.register("Jane", "jane@gmail.com", "Password456", 22, "DL002")

    system.authenticate(mike_customer)

    mike_customer.ban_user()

    system.authenticate(customer1)
    system.authenticate(customer2)
    system.authenticate(customer3)

    # ---------------- Residence ----------------
    sea_resort = Residence("Sea Resort")

    normal_room = NormalRoom()
    king_room = KingRoom()

    sea_resort.room_list.append(normal_room)
    sea_resort.room_list.append(king_room)

    system.add_residence(sea_resort)

    residence_booking_temp = Residencebooking(customer1)

    # ---------------- Staff ----------------
    driver_a = Staff("DriverA", "Have")
    system.add_staff(driver_a)

    staff_alice = Staff("Alice", "DL111")
    staff_bob = Staff("Bob", "DL222")

    system.add_staff(staff_alice)
    system.add_staff(staff_bob)

    # ---------------- Vehicles ----------------
    car1 = Car()
    bike1 = Motorcycle()

    system.add_vehicle(car1)
    system.add_vehicle(bike1)

    vehicle_booking_temp = Vehiclebooking(customer2)

    # ---------------- Activities ----------------
    driving_activity = Driving()
    hiking_activity = Hiking()

    activity_booking_temp = Activitybooking(customer2)

    # ---------------- Manager ----------------
    boss_manager = Manager("Boss", "Have")
    system.add_manager(boss_manager)

    # ---------------- Dummy booking ----------------
    room = DummyRoom(1)
    vehicle = DummyVehicle(1)
    activity = DummyActivity()

    booking_user1 = Booking(customer1)

    rb = Residencebooking(None, room, customer1, None, 100)
    booking_user1.residencebooking_list.append(rb)

    vb = Vehiclebooking(vehicle, customer1, None, driver_a, 200)
    booking_user1.vehiclebooking_list.append(vb)

    ab = Activitybooking(activity, customer1, None)
    booking_user1.activitybooking_list.append(ab)

    system.add_booking(booking_user1)

    # ---------------- Booking for mike ----------------
    booking_mike = Booking(mike_customer)

    class MockItem:

        def __init__(self, item_id, price):
            self.item_id = item_id
            self.price = price
            self.paid = False

        def mark_paid(self):
            self.paid = True

    item1 = MockItem(1, 1000)
    item2 = MockItem(2, 500)

    booking_mike.add_booking(item1)
    booking_mike.add_booking(item2)

    promo = Promotion(
        0.10,
        500,
        date.today() + timedelta(days=5)
    )

    system.add_promotions(promo)

    coupon = Coupon(
        50,
        date.today() + timedelta(days=5)
    )

    mike_customer.coupons.append(coupon)

    # ---------------- Mock staff booking ----------------
    mock_staff_user = Staff("MockUser", "DL999")
    mock_booking = Booking(mock_staff_user)

    booking_mock = Booking()
    mock_booking._Booking__residencebooking_list.append(booking_mock)

    system.add_booking(mock_booking)

    # ---------------- Completed booking ----------------
    alice_customer = Customer(
        "Alice",
        "a@mail",
        "1234",
        25,
        "DL111"
    )

    alice_customer._Customer__login_status = LogInStatus.ONLINE

    completed_booking = Booking(alice_customer)
    completed_booking._Booking__purchase_status = PurchaseStatus.COMPLETED

    system.add_user(alice_customer)
    system.add_booking(completed_booking)

    return system, alice_customer, completed_booking


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