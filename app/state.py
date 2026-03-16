from enum import Enum

# -------------------------------------------------- 
class LogInStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"

class OperationalStatus(Enum):
    READY = "ready"
    REPAIR = "repair"
    CLEANING = "cleaning"

class ServiceStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class StaffStatus(Enum):
    FREE = "free"
    BUSY = "busy"

class PurchaseStatus(Enum):
    BOOKING = "booking"
    INSPECTING = "inspecting"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    EXPIRED = "expired"
