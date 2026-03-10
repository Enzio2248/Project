# data / mock_data

from datetime import date, timedelta

# LOGIN
from system import System
from user  import Customer , Staff , Manager
from residence import Residence , Room  , NormalRoom , KingRoom
from vehicle import Vehicle , Car , Motorcycle
from activity import Driving , Hiking
from booking import Booking , Residencebooking , Vehiclebooking , Activitybooking
from payment import Promotion , Coupon
from state import LogInStatus, PurchaseStatus

def setup_login_mock():

    system = System()

    user1 = Customer("User1", "user1@gmail.com", "Password123", 25, "Have")
    user2 = Customer("User2", "user2@gmail.com", "Password456", 30)
    user3 = Customer("User3", "banned@gmail.com", "Password789", 40, "Have")
    user4 = Customer("John", "john@gmail.com", "Password123", 25, "DL001")
    user5 = Customer("Jane", "jane@gmail.com", "Password456", 22, "DL002")
    user6 = Customer("Mike", "mike@gmail.com", "Password789", 30, "DL003")

    system.add_customer(user1)
    system.add_customer(user2)
    system.add_customer(user3)
    system.add_customer(user4)
    system.add_customer(user5)
    system.add_customer(user6)

    user3.ban_user()

    system.register("John", "john@gmail.com", "Password123", 25, "DL001")
    system.register("Jane", "jane@gmail.com", "Password456", 22, "DL002")

    system.authenticate(user4)
    system.authenticate(user6)
    
    user6.ban_user()
    
    system.authenticate(user1)
    system.authenticate(user2)
    system.authenticate(user3)

    res1 = Residence("Sea Resort")

    room1 = NormalRoom()
    room2 = KingRoom()

    res1.room_list.append(room1)
    res1.room_list.append(room2)

    system.add_residence(res1)

    booking = Residencebooking(user1)

    staff1 = Staff("DriverA","Have") 

    system.add_staff(staff1)

    car1 = Car()
    bike1 = Motorcycle()

    system.add_vehicle(car1)
    system.add_vehicle(bike1)

    booking = Vehiclebooking(user2)

    act1 = Driving()
    act2 = Hiking()

    booking = Activitybooking(user2)

    user0 = Staff("John",  "Have")
    driver = Staff("Driver",  "Have")
    manager = Manager("Boss",  "Have")

    system.add_manager(manager)

    room = DummyRoom()
    vehicle = DummyVehicle()
    activity = DummyActivity()

    booking = Booking(user1)

    rb = Residencebooking( None, room, user1, None, 100)
    booking.residencebooking_list.append(rb)

    vb = Vehiclebooking( vehicle, user1, None, driver, 200)
    booking.vehiclebooking_list.append(vb)

    ab = Activitybooking( activity, user1, None)
    booking.activitybooking_list.append(ab)

    system.add_booking(booking)


    booking = Booking(user4)

    class MockItem:

        def __init__(self,item_id,price):
            self.item_id = item_id
            self.price = price
            self.paid = False

        def mark_paid(self):
            self.paid = True

    item1 = MockItem(1000)
    item2 = MockItem(500)

    booking.add_booking(item1)
    booking.add_booking(item2)

    promo = Promotion(
        0.10,
        500,
        date.today()+timedelta(days=5)
    )

    system.add_promotions(promo)

    coupon = Coupon(
        50,
        date.today()+timedelta(days=5)
    )

    user4.coupons.append(coupon)

    staff1 = Staff("Alice", "DL111")
    staff2 = Staff("Bob", "DL222")

    system.add_staff(staff1)
    system.add_staff(staff2)

    user = Staff("MockUser", "DL999")

    booking = Booking(user)

    staff = Staff("Alice", "DL111")

    user = Staff("MockUser", "DL999")

    booking = Booking( user)

    residence = Booking()

    booking._Booking__residencebooking_list.append(residence)
    
    system.add_booking(booking)

    user = Customer(
        "Alice",
        "a@mail",
        "1234",
        25,
        "DL111"
    )

    # force login
    user._Customer__login_status = LogInStatus.ONLINE

    booking = Booking( user)

    # make booking completed
    booking._Booking__purchase_status = PurchaseStatus.COMPLETED

    system.add_user(user)
    system.add_booking(booking)

    return system, user, booking

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