#main

from pydantic import BaseModel
from datetime import datetime
from fastmcp import FastMCP

from mock_data import test_mockup_data 

system = test_mockup_data()

mcp = FastMCP("TravelerSystem")

# request models
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


@mcp.tool()
def login(data: LoginRequest):
    """
    เป็นระบบที่ใช้สำหรับการตรวจสอบข้อมูลผู้ใช้งานเมื่อมีการเข้าสู่ระบบ โดยจะรับข้อมูลอีเมลและรหัสผ่านจากผู้ใช้งาน 
    และทำการตรวจสอบกับข้อมูลที่มีอยู่ในระบบว่าตรงกันหรือไม่ และเช็คว่าโดนแบนหรือไม่
    หากตรงกันจะอนุญาตให้เข้าสู่ระบบได้ และหากไม่ตรงกันจะปฏิเสธการเข้าสู่ระบบ
    """
    return system.authenticate(
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
    return system.register(
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
    return system.create_booking(
        data.user_id
    )

@mcp.tool()
def book_residence(data: ResidenceBookingRequest):
    """
    เป็นระบบที่ใช้สำหรับการจองที่พัก โดยจะรับข้อมูลผู้ใช้งานและรายละเอียดการจองจากผู้ใช้งาน 
    และทำการสร้างการจองที่พักใหม่ในระบบ
    """
    result = system.create_residencebooking(
        data.user_id,
        data.booking_id,
        data.residence_id,
        data.room_id,
        data.start_date,
        data.end_date
    )

    return result

@mcp.tool()
def book_vehicle(data: VehicleBookingRequest):
    """
    เป็นระบบที่ใช้สำหรับการจองยานพาหนะ โดยจะรับข้อมูลผู้ใช้งานและรายละเอียดการจองจากผู้ใช้งาน 
    และทำการสร้างการจองยานพาหนะใหม่ในระบบ
    """
    result = system.create_vehiclebooking(
        data.user_id,
        data.booking_id,
        data.vehicle_id,
        data.driver_id,
        data.start_date,
        data.end_date
    )

    return result

@mcp.tool()
def book_activity(data: ActivityBookingRequest):
    """
    เป็นระบบที่ใช้สำหรับการจองกิจกรรม โดยจะรับข้อมูลผู้ใช้งานและรายละเอียดการจองจากผู้ใช้งาน 
    และทำการสร้างการจองกิจกรรมใหม่ในระบบ
    """
    result = system.create_activitybooking(
        data.user_id,
        data.booking_id,
        data.activity_id,
        data.start_date,
        data.end_date
    )

    return result


@mcp.tool()
def cancel_booking(data: CancelBookingRequest):
    """
    เป็นระบบที่ใช้สำหรับการยกเลิกการจอง โดยจะรับข้อมูลการจองและผู้ที่ทำการยกเลิกจากผู้ใช้งาน 
    และทำการยกเลิกการจองนั้นในระบบ โดยจะตรวจสอบว่าผู้ที่ทำการยกเลิกเป็นผู้ที่มีสิทธิ์ในการยกเลิกการจองนั้นหรือไม่ 
    และทำการอัปเดตสถานะของการจองในระบบให้เป็น "ยกเลิก" เพื่อให้สามารถติดตามและจัดการการจองได้อย่างถูกต้องในอนาคต
    """
    result = system.cancel_booking(
        data.booking_id,
        data.requester_id
    )

    return result

@mcp.tool()
def request_payment(data: PaymentRequest):
    """
    เป็นระบบที่ใช้สำหรับการขอชำระเงิน โดยจะรับข้อมูลผู้ใช้งานและการจองจากผู้ใช้งาน และทำการสร้างคำขอชำระเงินใหม่ในระบบ
    โดยจะเชื่อมโยงคำขอชำระเงินนี้กับผู้ใช้งานและการจองที่เกี่ยวข้อง และบันทึกข้อมูลคำขอชำระเงินลงในระบบเพื่อให้สามารถติดตามและจัดการคำขอชำระเงินได้ในอนาคต
    """
    return system.request_payment(
        data.user_id,
        data.booking_id
    )


@mcp.tool()
def select_coupon(data: CouponRequest):
    """
    เป็นระบบที่ใช้สำหรับการเลือกคูปอง โดยจะรับข้อมูลผู้ใช้งานและการจองจากผู้ใช้งาน และทำการเลือกคูปองที่เหมาะสมเพื่อใช้ในการชำระเงิน
    """
    return system.select_coupon(
        data.user_id,
        data.booking_id,
        data.coupon_code
    )


@mcp.tool()
def submit_payment(data: SlipRequest):
    """
    เป็นระบบที่ใช้สำหรับการส่ง slip ชำระเงิน โดยจะรับข้อมูลผู้ใช้งานและการจองจากผู้ใช้งาน และทำการส่ง slip ชำระเงินใหม่ในระบบ
    """
    return system.submit_slip_number(
        data.user_id,
        data.booking_id,
        data.slip
    )

@mcp.tool()
def confirm_booking(data: ConfirmRequest):
    """
    เป็นระบบที่ใช้สำหรับการยืนยันการจอง โดยจะรับข้อมูลผู้ใช้งานและ ID ของการจองจากผู้ใช้งาน 
    และทำการยืนยันการจองนั้นในระบบ
    โดยจะตรวจสอบว่าผู้ที่ทำการยืนยันเป็นผู้ที่มีสิทธิ์ในการยืนยันการจองนั้นหรือไม่ 
    และทำการอัปเดตสถานะของการจองในระบบให้เป็น "ยืนยัน" เพื่อให้สามารถติดตามและจัดการการจองได้อย่างถูกต้องในอนาคต
    """
    return system.confirm_booking(
        data.staff_id,
        data.booking_id
    )

@mcp.tool()
def start_inspection(data: StartInspectionRequest):
    """
    เป็นระบบที่ใช้สำหรับการเริ่มต้นการตรวจสอบห้องพัก โดยจะรับข้อมูล ID ของการจองจากผู้ใช้งาน 
    และทำการเริ่มต้นกระบวนการตรวจสอบห้องพักในระบบ
    """
    return system.start_room_inspection(
        data.booking_id
    )

@mcp.tool()
def add_damage(data: DamageRequest):
    """
    เป็นระบบที่ใช้สำหรับการเพิ่มข้อมูลความเสียหายของห้องพัก โดยจะรับข้อมูล ID ของการจองและรายละเอียดความเสียหายจากผู้ใช้งาน 
    และทำการเพิ่มข้อมูลความเสียหายลงในระบบ
    """
    return system.add_damage(
        data.booking_id,
        data.description,
        data.price
    )


@mcp.tool()
def confirm_inspection(data: ConfirmInspectionRequest):
    """
    เป็นระบบที่ใช้สำหรับการยืนยันการตรวจสอบห้องพัก โดยจะรับข้อมูล ID ของการจองและสถานะความเสียหายจากผู้ใช้งาน 
    และทำการยืนยันการตรวจสอบห้องพักในระบบ
    """
    return system.confirm_inspection_complete(
        data.booking_id,
        data.damaged
    )

@mcp.tool()
def write_review(data: ReviewRequest):
    """
    เป็นระบบที่ใช้สำหรับการเขียนรีวิว โดยจะรับข้อมูลผู้ใช้งานและการจองจากผู้ใช้งาน และทำการสร้างรีวิวใหม่ในระบบ
    โดยจะเชื่อมโยงรีวิวนี้กับผู้ใช้งานและการจองที่เกี่ยวข้องให้คะแนน 1 - 5 และบันทึกข้อมูลรีวิวลงในระบบเพื่อให้สามารถติดตามและจัดการรีวิวได้ในอนาคต
    """
    return system.create_review(
        data.user_id,
        data.booking_id,
        data.rating,
        data.comment
    )

if __name__ == "__main__":
    mcp.run()