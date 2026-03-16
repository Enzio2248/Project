from otherclass import TimeSlot
from datetime import datetime, timedelta, date

from system import System
from user import Customer, Staff, Manager
from residence import Residence, Room, NormalRoom, KingRoom
from vehicle import Vehicle, Car, Motorcycle
from activity import Driving, Hiking
from booking import Booking, Residencebooking, Vehiclebooking, Activitybooking
from payment import Promotion, Coupon


def test_mockup_data():
    system = System()

    # ---------------- MANAGER ----------------
    manager = Manager("Alice Manager","aliceince@gmail.com","Alice_445","DL9999")
    system.add_manager(manager)

    # ---------------- STAFF ----------------
    staff1 = Staff("Bob Driver","Bobsocool@gmail.com","BobBobbo_1","DL9009")
    staff2 = Staff("Charlie Staff","charlie@gmail.com","Charlie_123","")
    system.add_staff(staff1)
    system.add_staff(staff2)

    # ---------------- CUSTOMER ----------------
    c1 = Customer("John Doe", "john@gmail.com", "Password123", 30, "DL7777")
    c2 = Customer("Jane Smith", "jane@gmail.com", "Password123", 22, "")
    
    system.add_customer(c1)
    system.add_customer(c2)

    # ---------------- COUPON ----------------
    coupon1 = Coupon("DISC100", 100, date.today() + timedelta(days=30))
    coupon2 = Coupon("DISC200", 200, date.today() + timedelta(days=30))

    c1.add_coupon(coupon1)
    c1.add_coupon(coupon2)

    # ---------------- PROMOTION ----------------
    promo1 = Promotion(0.10, 2000, date.today() + timedelta(days=30))
    promo2 = Promotion(0.20, 5000, date.today() + timedelta(days=30))

    system.add_promotion(promo1)
    system.add_promotion(promo2)

    # ---------------- RESIDENCE ----------------
    res1 = Residence("RES001", "Sea View Hotel")

    room1 = NormalRoom("RM001")
    room2 = KingRoom("RM002")


    # try:
    res1.add_room_list(room1)
    res1.add_room_list(room2)
    system.add_residence(res1, manager.staff_id)
    # except:
    #     pass

    # ---------------- VEHICLE ----------------
    car1 = Car("CAR001")
    bike1 = Motorcycle("BIKE001")

    system.add_vehicle(car1, manager.staff_id)
    system.add_vehicle(bike1, manager.staff_id)

    # ---------------- ACTIVITY ----------------
    activity1 = Driving()
    activity2 = Hiking()

    system.add_activity(manager.staff_id, activity1)
    system.add_activity(manager.staff_id, activity2)

    return system