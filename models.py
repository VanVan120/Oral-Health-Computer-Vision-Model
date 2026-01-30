from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str # Storing hashed password
    name: str
    role: str # 'doctor' or 'patient'

class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    doctor_id: int = Field(foreign_key="user.id")
    patient_id: int = Field(foreign_key="user.id")
    date_time: datetime
    status: str = Field(default="pending") # 'confirmed', 'pending'
    notes: Optional[str] = None
