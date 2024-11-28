import requests

#API url
#Automated tests for the pipeline
BASE_URL = "http://localhost:8197"
def test_set_state():
    response = requests.put(f"{BASE_URL}/state", data="RUNNING", headers={"Content-Type": "text/plain"})
    assert response.status_code == 200, "Failed to set state"

def test_get_state():
    response = requests.get(f"{BASE_URL}/state")
    assert response.status_code == 200, "Failed to get state"
def test_handle_request():
    response = requests.get(f"{BASE_URL}/request")
    assert response.status_code == 200, "Failed to handle request"

def test_get_run_log():
    response = requests.get(f"{BASE_URL}/run-log")
    assert response.status_code == 200, "Failed to access log"

if __name__ == "__main__":
    print("Running tests")
    test_set_state()
    test_get_state()
    test_handle_request()
    test_get_run_log()
    print("All tests passed");