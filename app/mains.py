from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from pydantic import BaseModel, Field
from datetime import datetime

from mock_data import test_mockup_data 

app = FastAPI()

system = test_mockup_data()

# =========================
# Request Models
# =========================

class LoginRequest(BaseModel):
    email: str = Field(..., example="john@gmail.com")
    password: str = Field(..., example="Password123")


class RegisterRequest(BaseModel):
    user_name: str = Field(..., example="New User")
    email: str = Field(..., example="newuser@gmail.com")
    password: str = Field(..., example="Password123")
    age: int = Field(..., example=25)
    driver_license: str = Field(..., example="DL8888")


class CreateBookingRequest(BaseModel):
    user_id: str = Field(..., example="U001")


class ResidenceBookingRequest(BaseModel):
    user_id: str = Field(..., example="U001")
    booking_id: str = Field(..., example="B001")
    residence_id: str = Field(..., example="RES001")
    room_id: str = Field(..., example="RM001")
    start_date: datetime = Field(..., example="2026-07-01T14:00:00")
    end_date: datetime = Field(..., example="2026-07-03T12:00:00")


class VehicleBookingRequest(BaseModel):
    user_id: str = Field(..., example="U001")
    booking_id: str = Field(..., example="B001")
    vehicle_id: str = Field(..., example="CAR001")
    driver_id: str | None = Field(None, example="S001")
    start_date: datetime = Field(..., example="2026-07-01T09:00:00")
    end_date: datetime = Field(..., example="2026-07-02T18:00:00")


class ActivityBookingRequest(BaseModel):
    user_id: str = Field(..., example="U001")
    booking_id: str = Field(..., example="B001")
    activity_id: str = Field(..., example="A001")
    start_date: datetime = Field(..., example="2026-07-02T08:00:00")
    end_date: datetime = Field(..., example="2026-07-02T17:00:00")


class CancelBookingRequest(BaseModel):
    booking_id: str = Field(..., example="B001")
    requester_id: str = Field(..., example="U001")


class PaymentRequest(BaseModel):
    user_id: str = Field(..., example="U001")
    booking_id: str = Field(..., example="B001")


class CouponRequest(BaseModel):
    user_id: str = Field(..., example="U001")
    booking_id: str = Field(..., example="B001")
    coupon_code: str = Field(..., example="DISC100")


class SlipRequest(BaseModel):
    user_id: str = Field(..., example="U001")
    booking_id: str = Field(..., example="B001")
    slip: str = Field(..., example="OK123456789")


class ConfirmRequest(BaseModel):
    staff_id: str = Field(..., example="S001")
    booking_id: str = Field(..., example="B001")


class StartInspectionRequest(BaseModel):
    booking_id: str = Field(..., example="B001")


class DamageRequest(BaseModel):
    booking_id: str = Field(..., example="B001")
    description: str = Field(..., example="Broken lamp")
    price: float = Field(..., example=500.0)


class ConfirmInspectionRequest(BaseModel):
    booking_id: str = Field(..., example="B001")
    damaged: bool = Field(..., example=True)


class ReviewRequest(BaseModel):
    user_id: str = Field(..., example="U001")
    booking_id: str = Field(..., example="B001")
    rating: int = Field(..., example=5)
    comment: str = Field(..., example="Very good service and clean room")


class BanUserRequest(BaseModel):
    manager_id: str = Field(..., example="M001")
    user_id: str = Field(..., example="U002")


class UnbanUserRequest(BaseModel):
    manager_id: str = Field(..., example="M001")
    user_id: str = Field(..., example="U002")


# =========================
# AUTH
# =========================

@app.post("/login")
def login(data: LoginRequest):
    return system.authenticate(data.email, data.password)


@app.post("/register")
def register(data: RegisterRequest):
    return system.register(
        data.user_name,
        data.email,
        data.password,
        data.age,
        data.driver_license
    )


# =========================
# BOOKING
# =========================

@app.post("/create-booking")
def create_booking(data: CreateBookingRequest):
    return system.create_booking(data.user_id)


@app.post("/book-residence")
def book_residence(data: ResidenceBookingRequest):
    return system.create_residencebooking(
        data.user_id,
        data.booking_id,
        data.residence_id,
        data.room_id,
        data.start_date,
        data.end_date
    )


@app.post("/book-vehicle")
def book_vehicle(data: VehicleBookingRequest):
    return system.create_vehiclebooking(
        data.user_id,
        data.booking_id,
        data.vehicle_id,
        data.driver_id,
        data.start_date,
        data.end_date
    )


@app.post("/book-activity")
def book_activity(data: ActivityBookingRequest):
    return system.create_activitybooking(
        data.user_id,
        data.booking_id,
        data.activity_id,
        data.start_date,
        data.end_date
    )


@app.post("/cancel-booking")
def cancel_booking(data: CancelBookingRequest):
    return system.cancel_booking(
        data.booking_id,
        data.requester_id
    )


# =========================
# PAYMENT
# =========================

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


# =========================
# STAFF
# =========================

@app.post("/confirm-booking")
def confirm_booking(data: ConfirmRequest):
    return system.confirm_booking(
        data.staff_id,
        data.booking_id
    )


@app.post("/start-inspection")
def start_inspection(data: StartInspectionRequest):
    return system.start_room_inspection(data.booking_id)


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


# =========================
# REVIEW
# =========================

@app.post("/write-review")
def write_review(data: ReviewRequest):
    return system.create_review(
        data.user_id,
        data.booking_id,
        data.rating,
        data.comment
    )


# =========================
# ADMIN
# =========================

@app.post("/ban-user")
def ban_user(data: BanUserRequest):
    return system.ban_user(data.manager_id, data.user_id)


@app.post("/unban-user")
def unban_user(data: UnbanUserRequest):
    return system.unban_user(data.manager_id, data.user_id)


# =========================
# LIST DATA
# =========================

@app.get("/residences")
def list_residences():
    result = []

    for r in system._System__residence_list:
        result.append({
            "residence_id": r.residence_id,
            "rooms": [room.room_id for room in r.room_list]
        })

    return result


@app.get("/vehicles")
def list_vehicles():
    return [
        {"vehicle_id": v.vehicle_id}
        for v in system._System__vehicle_list
    ]


@app.get("/activities")
def list_activities():
    return [
        {"activity_id": a.activity_id}
        for a in system._System__activity_list
    ]