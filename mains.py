#main

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

from mock_data import test_mockup_data 

app = FastAPI()

system = test_mockup_data()


class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    user_name: str
    email: str
    password: str
    age: int
    driver_license: str

class CreateBookingRequest(BaseModel):
    user_id: str

class ResidenceBookingRequest(BaseModel):
    user_id: str
    residence_id: str
    booking_id: str
    room_id: str
    start_date: datetime
    end_date: datetime

class VehicleBookingRequest(BaseModel):
    user_id: str
    vehicle_id: str
    booking_id: str
    driver_id: str | None 
    start_date: datetime
    end_date: datetime

class ActivityBookingRequest(BaseModel):
    user_id: str
    activity_id: str
    booking_id: str
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
    booking_id: str

class StartInspectionRequest(BaseModel):
    booking_id: str

class DamageRequest(BaseModel):
    booking_id: str
    description: str
    price: float

class ConfirmInspectionRequest(BaseModel):
    booking_id: str
    damaged: bool

class ReviewRequest(BaseModel):
    user_id: str
    booking_id: str
    rating: int
    comment: str

# API endpoints
@app.post("/login")
def login(data: LoginRequest):
    return system.authenticate(
        data.email,
        data.password
    )

@app.post("/register")
def register(data: RegisterRequest):
    return system.register(
        data.user_name,
        data.email,
        data.password,
        data.age,
        data.driver_license
    )

@app.post("/create-booking")
def create_booking(data: CreateBookingRequest):
    return system.create_booking(
        data.user_id
    )

@app.post("/book-residence")
def book_residence(data: ResidenceBookingRequest):

    result = system.create_residencebooking(
        data.user_id,
        data.booking_id,
        data.residence_id,
        data.room_id,
        data.start_date,
        data.end_date
    )

    return result

@app.post("/book-vehicle")
def book_vehicle(data: VehicleBookingRequest):

    result = system.create_vehiclebooking(
        data.user_id,
        data.booking_id,
        data.vehicle_id,
        data.driver_id,
        data.start_date,
        data.end_date
    )

    return result

@app.post("/book-activity")
def book_activity(data: ActivityBookingRequest):

    result = system.create_activitybooking(
        data.user_id,
        data.booking_id,
        data.activity_id,
        data.start_date,
        data.end_date
    )

    return result

@app.post("/cancel-booking")
def cancel_booking(data: CancelBookingRequest):

    result = system.cancel_booking(
        data.booking_id,
        data.requester_id
    )

    return result

@app.post("/request-payment")
def request_payment(data: PaymentRequest):

    return system.request_payment(
        data.user_id,
        data.booking_id
    )


@app.post("/select-coupon")
def select_coupon(data: CouponRequest):

    return system.select_coupon(
        data.user_id,
        data.booking_id,
        data.coupon_code
    )


@app.post("/submit-payment")
def submit_payment(data: SlipRequest):

    return system.submit_slip_number(
        data.user_id,
        data.booking_id,
        data.slip
    )

@app.post("/confirm-booking")
def confirm_booking(data: ConfirmRequest):

    return system.confirm_booking(
        data.staff_id,
        data.booking_id
    )

@app.post("/start-inspection")
def start_inspection(data: StartInspectionRequest):

    return system.start_room_inspection(
        data.booking_id
    )


@app.post("/add-damage")
def add_damage(data: DamageRequest):

    return system.add_damage(
        data.booking_id,
        data.description,
        data.price
    )


@app.post("/confirm-inspection")
def confirm_inspection(data: ConfirmInspectionRequest):

    return system.confirm_inspection_complete(
        data.booking_id,
        data.damaged
    )

@app.post("/write-review")
def write_review(data: ReviewRequest):

    return system.create_review(
        data.user_id,
        data.booking_id,
        data.rating,
        data.comment
    )