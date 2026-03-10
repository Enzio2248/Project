#main

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

from mock_data import (
    setup_login_mock, setup_register_mock, setup_booking_mock,
    setup_residence_mock, setup_vehicle_mock, setup_activity_mock,
    setup_cancel_mock, setup_payment_mock, setup_confirm_mock,
    setup_inspection_mock, setup_review_mock
)

app = FastAPI()

# mock data
login_system = setup_login_mock()
register_system = setup_register_mock()
booking_system = setup_booking_mock()
residence_system, booking = setup_residence_mock()
vehicle_system, vehicle_booking = setup_vehicle_mock()
activity_system, activity_booking = setup_activity_mock()
cancel_system = setup_cancel_mock()
payment_system, payment_user, payment_booking = setup_payment_mock()
confirm_system, confirm_booking = setup_confirm_mock()
inspection_system, inspection_booking = setup_inspection_mock()
review_system, review_user, review_booking = setup_review_mock()

# request models
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    user_name: str
    user_id: str
    email: str
    password: str
    age: int
    driver_license: str

class CreateBookingRequest(BaseModel):
    user_id: str

class ResidenceBookingRequest(BaseModel):
    user_id: str
    residence_id: str
    room_id: str
    start_date: datetime
    end_date: datetime

class VehicleBookingRequest(BaseModel):
    user_id: str
    vehicle_id: str
    driver_id: str | None = None
    start_date: datetime
    end_date: datetime

class ActivityBookingRequest(BaseModel):
    user_id: str
    activity_id: str
    start_date: datetime
    end_date: datetime

class CancelBookingRequest(BaseModel):
    booking_id: str
    requester_id: str

class PaymentRequest(BaseModel):
    user_id: str
    booking_id: str


class CouponRequest(BaseModel):
    user_id: str
    booking_id: str
    coupon_code: str


class SlipRequest(BaseModel):
    user_id: str
    booking_id: str
    slip: str

class ConfirmRequest(BaseModel):
    staff_id: str

class StartInspectionRequest(BaseModel):
    booking_id: str

class DamageRequest(BaseModel):
    booking_id: str
    damage_id: str
    description: str
    price: float

class ConfirmInspectionRequest(BaseModel):
    booking_id: str
    damaged: bool

class ReviewRequest(BaseModel):

    review_id: str
    user_id: str
    booking_id: str
    rating: int
    comment: str

# API endpoints
@app.post("/login")
def login(data: LoginRequest):
    return login_system.authenticate(
        data.email,
        data.password
    )

@app.post("/register")
def register(data: RegisterRequest):
    return register_system.register(
        data.user_name,
        data.user_id,
        data.email,
        data.password,
        data.age,
        data.driver_license
    )

@app.post("/create-booking")
def create_booking(data: CreateBookingRequest):
    return booking_system.create_booking(
        data.user_id
    )

@app.post("/book-residence")
def book_residence(data: ResidenceBookingRequest):

    result = residence_system.create_residencebooking(
        data.user_id,
        booking,
        data.residence_id,
        data.room_id,
        data.start_date,
        data.end_date
    )

    return result

@app.post("/book-vehicle")
def book_vehicle(data: VehicleBookingRequest):

    result = vehicle_system.create_vehiclebooking(
        data.user_id,
        vehicle_booking,
        data.vehicle_id,
        data.driver_id,
        data.start_date,
        data.end_date
    )

    return result

@app.post("/book-activity")
def book_activity(data: ActivityBookingRequest):

    result = activity_system.create_activitybooking(
        data.user_id,
        activity_booking,
        data.activity_id,
        data.start_date,
        data.end_date
    )

    return result

@app.post("/cancel-booking")
def cancel_booking(data: CancelBookingRequest):

    return cancel_system.cancel_booking(
        data.booking_id,
        data.requester_id
    )

@app.post("/cancel-booking")
def cancel_booking(data: CancelBookingRequest):

    result = cancel_system.cancel_booking(
        data.booking_id,
        data.requester_id
    )

    return result

@app.post("/request-payment")
def request_payment(data: PaymentRequest):

    return payment_system.request_payment(
        data.user_id,
        data.booking_id
    )


@app.post("/select-coupon")
def select_coupon(data: CouponRequest):

    return payment_system.select_coupon(
        payment_user,
        payment_booking,
        data.coupon_code
    )


@app.post("/submit-payment")
def submit_payment(data: SlipRequest):

    return payment_system.submit_slip_number(
        payment_user,
        payment_booking,
        data.slip
    )

@app.post("/confirm-booking")
def confirm_booking(data: ConfirmRequest):

    return confirm_system.confirm_booking(
        data.staff_id,
        confirm_booking
    )

@app.post("/start-inspection")
def start_inspection(data: StartInspectionRequest):

    return inspection_system.start_room_inspection(
        data.booking_id
    )


@app.post("/add-damage")
def add_damage(data: DamageRequest):

    return inspection_system.add_damage(
        data.booking_id,
        data.damage_id,
        data.description,
        data.price
    )


@app.post("/confirm-inspection")
def confirm_inspection(data: ConfirmInspectionRequest):

    return inspection_system.confirm_inspection_complete(
        data.booking_id,
        data.damaged
    )

@app.post("/write-review")
def write_review(data: ReviewRequest):

    return review_system.create_review(
        data.review_id,
        data.user_id,
        data.booking_id,
        data.rating,
        data.comment
    )