#WriteReview

from fastapi import FastAPI , HTTPException
from datetime import datetime, date
from abc import ABC, abstractmethod

from state import LogInStatus, PurchaseStatus

class System:
    def __init__(self):
        self.__reviews = [] 
        self.__user_list = []
        self.__bookings = []   

    def add_user(self, user):
        self.__user_list.append(user)

    def add_booking(self, booking):
        self.__bookings.append(booking)

    def create_review(self, review_id, user_id, booking_id, rating, comment):
        user = next((u for u in self.__user_list if u.user_id == user_id), None)
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

        review = Review(review_id, user_id, booking_id, rating, comment)
        self.__reviews.append(review)
        return {"message": "Review created successfully", "review_id": review_id}
    
    def _get_booking(self, booking_id):
        for booking in self.__bookings:
            if booking.booking_id == booking_id:
                return booking
        return None

class Review:
    def __init__(self, review_id, user_id, booking_id, rating, comment):
        self.__review_id = review_id
        self.__user_id = user_id
        self.__booking_id = booking_id
        self.__rating = rating      
        self.__comment = comment
        self.__created_at = datetime.now()

    @property
    def booking_id(self):
        return self.__booking_id

class Booking:
    def __init__(self, booking_id, user):
        self.__booking_id = booking_id
        self.__user = user
        self.__purchase_status = PurchaseStatus.BOOKING

    @property
    def user_id(self):
        return self.__user.user_id

    @property
    def purchase_status(self):
        return self.__purchase_status
    
    @property
    def booking_id(self):
        return self.__booking_id

class User(ABC):
    def __init__(self, user_name, user_id, driver_license):
        self._user_name = user_name
        self._user_id = user_id
        self._driver_license = driver_license

    @property
    def user_id(self):
        return self._user_id

class Customer(User):
    def __init__(self, user_name, user_id, user_mail, password, age, driver_license):
        super().__init__(user_name, user_id, driver_license)
        self.__login_status = LogInStatus.OFFLINE

    @property
    def login_status(self):
        return self.__login_status
    
# def setup_mock_data():
#     print("\n========== SETUP MOCK DATA ==========")

#     system = System()

#     user = Customer("Alice","U001","a@mail","1234",25,"DL111")

#     # force login
#     user._Customer__login_status = LogInStatus.ONLINE

#     booking = Booking("B001", user)

#     # make booking completed
#     booking._Booking__purchase_status = PurchaseStatus.COMPLETED

#     system.add_user(user)
#     system.add_booking(booking)

#     return system, user, booking

# def test_create_review_success(system,user,booking):
#     try:
#         result = system.create_review(
#             "R001",
#             user.user_id,
#             booking.booking_id,
#             5,
#             "Excellent service"
#         )
#         print("SUCCESS")
#         print(result)

#     except HTTPException as e:
#         print("FAILED")
#         print(e.detail)

# def test_user_not_found(system,booking):
#     try:

#         result = system.create_review(
#             "R002",
#             "U999",
#             booking.booking_id,
#             4,
#             "Nice"
#         )

#         print("SUCCESS")
#         print(result)

#     except HTTPException as e:
#         print("FAILED")
#         print(e.detail)

# def test_user_not_logged_in(system,user,booking):
#     try:

#         user._Customer__login_status = LogInStatus.OFFLINE

#         result = system.create_review(
#             "R003",
#             user.user_id,
#             booking.booking_id,
#             4,
#             "Good"
#         )

#         print("SUCCESS")
#         print(result)

#     except HTTPException as e:
#         print("FAILED")
#         print(e.detail)

# def test_booking_not_found(system,user):
#     try:

#         result = system.create_review(
#             "R004",
#             user.user_id,
#             "B999",
#             4,
#             "Nice"
#         )

#         print("SUCCESS")
#         print(result)

#     except HTTPException as e:
#         print("FAILED")
#         print(e.detail)

# def test_booking_not_completed(system,user,booking):
#     try:

#         booking._Booking__purchase_status = PurchaseStatus.BOOKING

#         result = system.create_review(
#             "R005",
#             user.user_id,
#             booking.booking_id,
#             4,
#             "Nice"
#         )

#         print("SUCCESS")
#         print(result)

#     except HTTPException as e:
#         print("FAILED")
#         print(e.detail)

# def test_not_your_booking(system,user,booking):
#     try:

#         other_user = Customer("Bob","U002","b@mail","1234",30,"DL222")
#         other_user._Customer__login_status = LogInStatus.ONLINE

#         system.add_user(other_user)

#         result = system.create_review(
#             "R006",
#             other_user.user_id,
#             booking.booking_id,
#             4,
#             "Nice"
#         )

#         print("SUCCESS")
#         print(result)

#     except HTTPException as e:
#         print("FAILED")
#         print(e.detail)

# def test_duplicate_review(system,user,booking):
#     try:

#         system.create_review(
#             "R007",
#             user.user_id,
#             booking.booking_id,
#             5,
#             "Great"
#         )

#         result = system.create_review(
#             "R008",
#             user.user_id,
#             booking.booking_id,
#             4,
#             "Good"
#         )

#         print("SUCCESS")
#         print(result)

#     except HTTPException as e:
#         print("FAILED")
#         print(e.detail)

# def test_invalid_rating(system,user,booking):
#     try:

#         result = system.create_review(
#             "R009",
#             user.user_id,
#             booking.booking_id,
#             10,
#             "Bad rating"
#         )

#         print("SUCCESS")
#         print(result)

#     except HTTPException as e:
#         print("FAILED")
#         print(e.detail)

# print("\n========== TEST WRITE REVIEW ==========")

# system,user,booking = setup_mock_data()
# print("\n[TEST 1] Create Review Success")
# test_create_review_success(system,user,booking)

# system,user,booking = setup_mock_data()
# print("\n[TEST 2] User Not Found")
# test_user_not_found(system,booking)

# system,user,booking = setup_mock_data()
# print("\n[TEST 3] User Not Logged In")
# test_user_not_logged_in(system,user,booking)

# system,user,booking = setup_mock_data()
# print("\n[TEST 4] Booking Not Found")
# test_booking_not_found(system,user)

# system,user,booking = setup_mock_data()
# print("\n[TEST 5] Booking Not Completed")
# test_booking_not_completed(system,user,booking)

# system,user,booking = setup_mock_data()
# print("\n[TEST 6] Not Your Booking")
# test_not_your_booking(system,user,booking)

# system,user,booking = setup_mock_data()
# print("\n[TEST 7] Duplicate Review")
# test_duplicate_review(system,user,booking)

# system,user,booking = setup_mock_data()
# print("\n[TEST 8] Invalid Rating")
# test_invalid_rating(system,user,booking)