#main

from pydantic import BaseModel
from datetime import datetime
from fastmcp import FastMCP

from SequenceDiagram.CancelBooking import System as CancelSystem
from mock_data import setup_login_mock, setup_register_mock, setup_booking_mock, setup_residence_mock, setup_vehicle_mock, setup_activity_mock, setup_cancel_mock, setup_payment_mock, setup_confirm_mock, setup_inspection_mock, setup_review_mock


# mock data
login_system = setup_login_mock()
register_system = setup_register_mock()
booking_system = setup_booking_mock()
residence_system, booking = setup_residence_mock()
vehicle_system, vehicle_booking = setup_vehicle_mock()
activity_system, activity_booking = setup_activity_mock()
cancel_system = setup_cancel_mock()
payment_system, payment_user, payment_booking = setup_payment_mock()
confirm_system, confirm_booking_obj = setup_confirm_mock()

mcp = FastMCP("TravelerSystem")

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


@mcp.tool()
def login(data: LoginRequest):
    """
    เป็นระบบที่ใช้สำหรับการตรวจสอบข้อมูลผู้ใช้งานเมื่อมีการเข้าสู่ระบบ โดยจะรับข้อมูลอีเมลและรหัสผ่านจากผู้ใช้งาน 
    และทำการตรวจสอบกับข้อมูลที่มีอยู่ในระบบว่าตรงกันหรือไม่ และเช็คว่าโดนแบนหรือไม่
    หากตรงกันจะอนุญาตให้เข้าสู่ระบบได้ และหากไม่ตรงกันจะปฏิเสธการเข้าสู่ระบบ
    """
    return login_system.authenticate(
        data.email,
        data.password
    )


@mcp.tool()
def register(data: RegisterRequest):
    """
    เป็นระบบที่ใช้สำหรับการลงทะเบียนผู้ใช้งานใหม่ โดยจะรับข้อมูลต่างๆ 
    เช่น ชื่อผู้ใช้งาน, อีเมล, รหัสผ่าน, อายุ และใบขับขี่ จากผู้ใช้งาน 
    และทำการบันทึกข้อมูลเหล่านี้ลงในระบบเพื่อให้ผู้ใช้งานสามารถเข้าสู่ระบบและใช้บริการต่างๆ ได้ในอนาคต
    """
    return register_system.register(
        data.user_name,
        data.email,
        data.password,
        data.age,
        data.driver_license
    )


@mcp.tool()
def create_booking(data: CreateBookingRequest):
    """
    เป็นระบบที่ใช้สำหรับการสร้างการจองใหม่ โดยจะรับข้อมูลผู้ใช้งานจากผู้ใช้งาน และทำการสร้างการจองใหม่ในระบบ 
    โดยจะเชื่อมโยงการจองนี้กับผู้ใช้งานที่ทำการจอง และบันทึกข้อมูลการจองลงในระบบเพื่อให้สามารถติดตามและจัดการการจองได้ในอนาคต
    """
    return booking_system.create_booking(
        data.user_id
    )

@mcp.tool()
def book_residence(data: ResidenceBookingRequest):

    result = residence_system.create_residencebooking(
        data.user_id,
        booking,
        "RB001",
        data.residence_id,
        data.room_id,
        data.start_date,
        data.end_date
    )

    return {
        "message": "Residence booking successful"
    }

@mcp.tool()
def book_vehicle(data: VehicleBookingRequest):

    vehicle_system.create_vehiclebooking(
        data.user_id,
        vehicle_booking,
        "VB001",
        data.vehicle_id,
        data.driver_id,
        data.start_date,
        data.end_date
    )

    return {"message": "Vehicle booking successful"}

@mcp.tool()
def book_activity(data: ActivityBookingRequest):

    activity_system.create_activitybooking(
        data.user_id,
        activity_booking,
        "AB001",
        data.activity_id,
        data.start_date,
        data.end_date
    )

    return {"message": "Activity booking successful"}

@mcp.tool()
def cancel_booking(data: CancelBookingRequest):

    result = cancel_system.cancel_booking(
        data.booking_id,
        data.requester_id
    )

    return result

@mcp.tool()
def cancel_booking(data: CancelBookingRequest):

    result = cancel_system.cancel_booking(
        data.booking_id,
        data.requester_id
    )

    return result

@mcp.tool()
def request_payment(data: PaymentRequest):

    return payment_system.request_payment(
        payment_user,
        payment_booking
    )


@mcp.tool()
def select_coupon(data: CouponRequest):

    return payment_system.select_coupon(
        payment_user,
        payment_booking,
        data.coupon_code
    )


@mcp.tool()
def submit_payment(data: SlipRequest):

    return payment_system.submit_slip_number(
        payment_user,
        payment_booking,
        data.slip
    )

if __name__ == "__main__":
    mcp.run()