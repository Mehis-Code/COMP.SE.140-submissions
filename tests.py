import requests

#API url
BASE_URL = "http://localhost:8197"

def test_set_state():
    response = requests.put(f"{BASE_URL}/state", data="RUNNING", headers={"Content-Type": "text/plain"})
    assert response.status_code == 200
    assert response.text == "State is RUNNING", "Failed to set state to RUNNING"

def test_get_state():
    response = requests.get(f"{BASE_URL}/state")
    assert response.status_code == 200
    assert response.text == "RUNNING", "Failed to get state"

def test_handle_request():
    response = requests.get(f"{BASE_URL}/request")
    assert response.status_code == 200
    assert response.text == "Request handled", "Failed to handle request"

def test_get_run_log():
    response = requests.get(f"{BASE_URL}/log")
    assert response.status_code == 200
    assert "RUNNING" in response.text, "Failed to get run log"

def test_nginx_service()
    response = requests.get(f"http://localhost:8198")
    assert response.status_code == 200
    assert response.text == "Nginx service is running", "Failed to get nginx service"

if __name__ == "__main__":
    print("Running tests")
    test_set_state()
    test_get_state()
    test_handle_request()
    test_get_run_log()
    print("All tests passed");