from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime, date as datetime_date
import uuid

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

class DailyHabitLog(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    date: datetime_date = Field(default_factory=datetime_date.today, index=True)
    smoked_cigarettes: bool = Field(default=False)
    ate_sweets: bool = Field(default=False)
    brushed_after_meal: bool = Field(default=False)
    used_floss: bool = Field(default=False)
    used_sensodyne: bool = Field(default=False)

class GenAIFeedback(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    prompt: str
    gemini_response: str
    is_helpful: bool
    user_correction: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
