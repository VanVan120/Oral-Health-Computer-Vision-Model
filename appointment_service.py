from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from database import get_session
from models import User, Appointment
from auth_service import get_current_user
from auth_core import get_password_hash
import os
import requests

# -- DTOs --
class AppointmentCreate(BaseModel):
    doctor_id: int
    # patient_id is not needed, we infer from logged in user
    date_time: datetime
    notes: Optional[str] = None

class AppointmentRead(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    date_time: datetime
    status: str
    notes: Optional[str]
    doctor_name: Optional[str] = None
    patient_name: Optional[str] = None

class AppointmentUpdate(BaseModel):
    doctor_id: Optional[int] = None
    date_time: Optional[datetime] = None
    notes: Optional[str] = None
    status: Optional[str] = None

# -- Email Logic --
def send_appointment_email(email: str, subject: str, content: str):
    sender_email = os.getenv("EMAIL_SENDER")
    api_key = os.getenv("BREVO_API_KEY")
    if not sender_email or not api_key:
        print(f"Simulation: Email to {email} | {subject}")
        return

    try:
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        }
        payload = {
            "sender": {"name": "Oral AI Appointments", "email": sender_email},
            "to": [{"email": email}],
            "subject": subject,
            "htmlContent": content
        }
        requests.post(url, json=payload, headers=headers)
    except Exception as e:
        print(f"Email Error: {e}")

# -- Router --
router = APIRouter(prefix="/api/appointments", tags=["appointments"])

@router.post("/book", response_model=Appointment)
def book_appointment(
    appt: AppointmentCreate, 
    background_tasks: BackgroundTasks, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # 1. Verify users exist
    doctor = session.get(User, appt.doctor_id)
    if not doctor or doctor.role != "doctor":
         raise HTTPException(status_code=400, detail="Invalid doctor selected")
    
    # 2. Save to DB (Use current user as Patient)
    db_appt = Appointment(
        doctor_id=doctor.id,
        patient_id=current_user.id,
        date_time=appt.date_time,
        notes=appt.notes
    )
    
    session.add(db_appt)
    session.commit()
    session.refresh(db_appt)

    # 3. Notification
    msg = f"<html><body><p>Dear {current_user.name},</p><p>Dr. {doctor.name} has scheduled a checkup for {appt.date_time}.</p></body></html>"
    background_tasks.add_task(send_appointment_email, current_user.email, "Appointment Confirmed", msg)

    return db_appt

@router.get("/my-appointments", response_model=List[AppointmentRead])
def get_my_appointments(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    statement = None
    
    if current_user.role == "doctor":
        # Doctor sees ALL their appointments
        statement = select(Appointment).where(Appointment.doctor_id == current_user.id)
    else:
        # Patient sees only THEIR appointments
        statement = select(Appointment).where(Appointment.patient_id == current_user.id)

    results = session.exec(statement).all()
    
    # Enrich with names
    enriched = []
    for r in results:
        doc = session.get(User, r.doctor_id)
        pat = session.get(User, r.patient_id)
        enriched.append(AppointmentRead(
            id=r.id,
            doctor_id=r.doctor_id,
            patient_id=r.patient_id,
            date_time=r.date_time,
            status=r.status,
            notes=r.notes,
            doctor_name=doc.name if doc else "Unknown",
            patient_name=pat.name if pat else "Unknown"
        ))
    return enriched

@router.put("/update/{appointment_id}", response_model=AppointmentRead)
def update_appointment(
    appointment_id: int,
    appt_update: AppointmentUpdate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Get the appointment
    appointment = session.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Check authorization - only the patient who created it or the assigned doctor can update
    if current_user.role == "patient" and appointment.patient_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this appointment")
    if current_user.role == "doctor" and appointment.doctor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this appointment")
    
    # Update fields if provided
    if appt_update.doctor_id is not None:
        doctor = session.get(User, appt_update.doctor_id)
        if not doctor or doctor.role != "doctor":
            raise HTTPException(status_code=400, detail="Invalid doctor selected")
        appointment.doctor_id = appt_update.doctor_id
    
    if appt_update.date_time is not None:
        appointment.date_time = appt_update.date_time
    
    if appt_update.notes is not None:
        appointment.notes = appt_update.notes
    
    if appt_update.status is not None:
        appointment.status = appt_update.status
    
    session.add(appointment)
    session.commit()
    session.refresh(appointment)
    
    # Send notification
    doctor = session.get(User, appointment.doctor_id)
    patient = session.get(User, appointment.patient_id)
    
    if current_user.role == "patient":
        # Notify doctor about patient's update
        msg = f"<html><body><p>Dear Dr. {doctor.name},</p><p>{patient.name} has updated their appointment to {appointment.date_time}.</p></body></html>"
        background_tasks.add_task(send_appointment_email, doctor.email, "Appointment Updated", msg)
    else:
        # Notify patient about doctor's update
        msg = f"<html><body><p>Dear {patient.name},</p><p>Dr. {doctor.name} has updated your appointment to {appointment.date_time}.</p></body></html>"
        background_tasks.add_task(send_appointment_email, patient.email, "Appointment Updated", msg)
    
    # Return enriched data
    return AppointmentRead(
        id=appointment.id,
        doctor_id=appointment.doctor_id,
        patient_id=appointment.patient_id,
        date_time=appointment.date_time,
        status=appointment.status,
        notes=appointment.notes,
        doctor_name=doctor.name if doctor else "Unknown",
        patient_name=patient.name if patient else "Unknown"
    )

@router.post("/seed_users")
def seed_users(session: Session = Depends(get_session)):
    # Helper to create mock users for testing
    if not session.exec(select(User)).first():
        u1 = User(
            email="dr.smith@oralai.com", 
            name="Dr. Smith", 
            role="doctor",
            password_hash=get_password_hash("password123")
        )
        u2 = User(
            email="jane@test.com", 
            name="Jane Doe", 
            role="patient",
            password_hash=get_password_hash("password123")
        )
        session.add(u1)
        session.add(u2)
        session.commit()
        return {"message": "Users seeded with password 'password123'", "users": [u1.email, u2.email]}
    return {"message": "Users already exist"}
