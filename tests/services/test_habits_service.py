from fastapi.testclient import TestClient

def test_save_and_get_habits(client: TestClient, patient_token: str):
    headers = {"Authorization": f"Bearer {patient_token}"}
    
    # Save today's habits
    response = client.post(
        "/habits/log",
        headers=headers,
        json={
            "smoked_cigarettes": False,
            "ate_sweets": True,
            "brushed_after_meal": True,
            "used_floss": False,
            "used_sensodyne": False
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ate_sweets"] is True
    assert data["used_floss"] is False

    # Get habit history
    history_response = client.get("/habits/history", headers=headers)
    assert history_response.status_code == 200
    history_data = history_response.json()
    
    assert isinstance(history_data, list)
    assert len(history_data) >= 1
    assert history_data[0]["brushed_after_meal"] is True

def test_unauthorized_habits_access(client: TestClient):
    response = client.get("/habits/history")
    assert response.status_code == 401
