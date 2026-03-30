from fastapi.testclient import TestClient
from datetime import datetime, timedelta

def test_book_and_get_appointments(client: TestClient, patient_token: str, doctor_token: str):
    headers_patient = {"Authorization": f"Bearer {patient_token}"}
    headers_doctor = {"Authorization": f"Bearer {doctor_token}"}

    # 1. Get List of Doctors
    doc_response = client.get("/auth/doctors")
    assert doc_response.status_code == 200
    doctors = doc_response.json()
    assert len(doctors) > 0
    doctor_id = doctors[0]["id"]

    # 2. Patient books an appointment
    appt_time = (datetime.utcnow() + timedelta(days=2)).isoformat()
    response = client.post(
        "/api/appointments/book",
        headers=headers_patient,
        json={
            "doctor_id": doctor_id,
            "date_time": appt_time,
            "notes": "Need a checkup for cavities"
        }
    )
    assert response.status_code == 200
    appt_data = response.json()
    assert appt_data["doctor_id"] == doctor_id
    assert appt_data["status"] == "pending"
    assert appt_data["notes"] == "Need a checkup for cavities"
    appt_id = appt_data["id"]

    # 3. Patient gets their appointments
    pat_appts = client.get("/api/appointments/my-appointments", headers=headers_patient)
    assert pat_appts.status_code == 200
    assert len(pat_appts.json()) >= 1
    assert any(a["id"] == appt_id for a in pat_appts.json())

    # 4. Doctor gets their appointments
    doc_appts = client.get("/api/appointments/my-appointments", headers=headers_doctor)
    assert doc_appts.status_code == 200
    assert len(doc_appts.json()) >= 1

    # 5. Doctor updates appointment status
    update_res = client.put(
        f"/api/appointments/update/{appt_id}",
        headers=headers_doctor,
        json={"status": "confirmed", "notes": "Confirmed appointment"}
    )
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "confirmed"

def test_unauthorized_appointment_access(client: TestClient):
    response = client.get("/api/appointments/my-appointments")
    assert response.status_code == 401
