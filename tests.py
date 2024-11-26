import requests

#API url
BASE_URL = "http://localhost:8197"

def test_set_state():
    response = requests.put(f"{BASE_URL}/state", data="RUNNING", headers={"Content-Type": "text/plain"})
    assert response.status_code == 200
    assert response.text == "State is RUNNING"

def test_get_state():
    response = requests.get(f"{BASE_URL}/state")
    assert response.status_code == 200
    assert response.text == "RUNNING"

def test_handle_request():
    response = requests.get(f"{BASE_URL}/request")
    assert response.status_code == 200
    assert response.text == "Request handled"

def test_get_run_log():
    response = requests.get(f"{BASE_URL}/log")
    assert response.status_code == 200
    assert "RUNNING" in response.text