# Trip.oop.com - Travel Booking System

## ภาพรวมของระบบ

ระบบ **Trip.oop.com** เป็นระบบบริหารจัดการการท่องเที่ยวแบบครบวงจรที่ถูกออกแบบมาเพื่อรองรับการดำเนินงานของธุรกิจท่องเที่ยวที่ให้บริการหลายประเภทภายใต้ผู้ให้บริการรายเดียว โดยระบบนี้มีวัตถุประสงค์เพื่ออำนวยความสะดวกให้ลูกค้าสามารถทำการจองบริการด้านการท่องเที่ยวได้ในแพลตฟอร์มเดียว พร้อมทั้งช่วยให้ผู้ดูแลระบบสามารถบริหารจัดการทรัพยากร บุคลากร การเงิน และข้อมูลทางธุรกิจได้อย่างมีประสิทธิภาพ

ระบบรองรับการจองบริการหลายประเภท เช่น

* ที่พัก (Residence)
* ยานพาหนะ (Vehicle)
* กิจกรรมท่องเที่ยว (Activity)

โดยพัฒนาด้วยแนวคิด **Object-Oriented Programming (OOP)** และใช้ **FastMCP** สำหรับการทดสอบการทำงานของระบบผ่าน MCP Tools

---

## เทคโนโลยีที่ใช้

* Python
* FastMCP
* Docker
* Pydantic

---

## โครงสร้างโปรเจกต์

```
Project
│
├── app
│   ├── activity.py
│   ├── booking.py
│   ├── payment.py
│   ├── system.py
│   ├── testmcp.py
│   └── ...
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## วิธีรันระบบด้วย Docker

1. Build Docker Image

```
docker build -t app .
```

2. Run Container

```
docker run -it --rm app
```

เมื่อรันสำเร็จ ระบบ MCP Server จะเริ่มทำงาน

---

## ผู้พัฒนา

Project สำหรับการศึกษาในรายวิชา Object-Oriented Programming
