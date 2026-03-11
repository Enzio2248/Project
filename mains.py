#main

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime

from mock_data import test_mockup_data 

app = FastAPI()

system = test_mockup_data()


class LoginRequest(BaseModel):
    email: str = Field(..., example="testuser@gmail.com")
    password: str = Field(..., example="Password123")

class RegisterRequest(BaseModel):
    user_name: str = Field(..., example="TestUser")
    email: str = Field(..., example="testuser@gmail.com")
    password: str = Field(..., example="Password123")
    age: int = Field(..., example="25")
    driver_license: str = Field(..., example="DL100")

class CreateBookingRequest(BaseModel):
    user_id: str  = Field(..., example="U002")

class ResidenceBookingRequest(BaseModel):
    user_id: str = Field(..., example="U002")
    booking_id: str = Field(..., example="booking-f419c6c60fdd4bbf922f2d82cd19b18d")
    residence_id: str = Field(..., example="R001")
    room_id: str = Field(..., example="RM001")
    start_date: datetime = Field(..., example="2026-04-01T12:00:00")
    end_date: datetime = Field(..., example="2026-04-05T12:00:00")

class VehicleBookingRequest(BaseModel):
    user_id: str = Field(..., example="U002")
    booking_id: str = Field(..., example="booking-f419c6c60fdd4bbf922f2d82cd19b18d")
    vehicle_id: str = Field(..., example="V001")
    driver_id: str | None = Field(..., example="S001")
    start_date: datetime = Field(..., example="2026-04-01T10:00:00")
    end_date: datetime = Field(..., example="2026-04-01T18:00:00")

class ActivityBookingRequest(BaseModel):
    user_id: str = Field(..., example="U002")
    activity_id: str = Field(..., example="A001")
    booking_id: str = Field(..., example="booking-f419c6c60fdd4bbf922f2d82cd19b18d")
    start_date: datetime = Field(..., example="2026-04-03T09:00:00")
    end_date: datetime = Field(..., example="2026-04-03T11:00:00")

class CancelBookingRequest(BaseModel):
    booking_id: str = Field(..., example="booking-f419c6c60fdd4bbf922f2d82cd19b18d")
    requester_id: str = Field(..., example="U002")

class PaymentRequest(BaseModel):
    user_id: str = Field(..., example="U002")
    booking_id: str = Field(..., example="booking-f419c6c60fdd4bbf922f2d82cd19b18d")

class CouponRequest(BaseModel):
    user_id: str = Field(..., example="U002")
    booking_id: str = Field(..., example="booking-f419c6c60fdd4bbf922f2d82cd19b18d")
    coupon_code: str = Field(..., example="DISCOUNT10")

class SlipRequest(BaseModel):
    user_id: str = Field(..., example="U002")
    booking_id: str = Field(..., example="booking-f419c6c60fdd4bbf922f2d82cd19b18d")
    slip: str = Field(..., example="OK123456789")

class ConfirmRequest(BaseModel):
    staff_id: str = Field(..., example="S001")
    booking_id: str = Field(..., example="booking-f419c6c60fdd4bbf922f2d82cd19b18d")

class StartInspectionRequest(BaseModel):
    booking_id: str = Field(..., example="booking-f419c6c60fdd4bbf922f2d82cd19b18d")

class DamageRequest(BaseModel):
    booking_id: str = Field(..., example="booking-f419c6c60fdd4bbf922f2d82cd19b18d")
    description: str = Field(..., example="Broken lamp in the room")
    price: float = Field(..., example=500)

class ConfirmInspectionRequest(BaseModel):
    booking_id: str = Field(..., example="booking-f419c6c60fdd4bbf922f2d82cd19b18d")
    damaged: bool = Field(..., example=True)

class ReviewRequest(BaseModel):
    user_id: str = Field(..., example="U002")
    booking_id: str = Field(..., example="booking-f419c6c60fdd4bbf922f2d82cd19b18d")
    rating: int = Field(..., example=5)
    comment: str = Field(..., example="The stay was excellent and the staff were very helpful.")

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