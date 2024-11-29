import requests
from requests.auth import HTTPBasicAuth
#API url
#Automated tests for the pipeline
BASE_URL = "http://docker:8197"

def test_set_state(param, username, password):
    headers = {
        'Content-Type': 'text/plain'
    }
    response = requests.put(
        f"{BASE_URL}/state",
        data=param,
        headers=headers,
        auth=HTTPBasicAuth(username, password)
    )
    assert response.status_code == 200, "Failed to set state"
    assert response.text == param, "Failed to set state"


def test_get_state():
    response = requests.get(f"{BASE_URL}/state")
    assert response.status_code == 200, "Failed to get state"
    assert response.text in ["INIT", "PAUSED", "RUNNING", "SHUTDOWN"], "Test response not in list"
    
def test_handle_request():
    response = requests.get(f"{BASE_URL}/request")
    assert response.status_code == 200, "Failed to handle request"

def test_get_run_log():
    response = requests.get(f"{BASE_URL}/run-log")
    assert response.status_code == 200, "Failed to access log"
    assert response.text.startswith("['State initialized at"), "Failed to access log"

if __name__ == "__main__":
    print("Running tests")
    test_set_state("PAUSED", "user1", "devops")
    test_get_state("RUNNING", "user1", "devops")

    test_handle_request()
    test_get_run_log()
    test_set_state("INIT", "user1", "devops")
    test_set_state("SHUTDOWN", "user1", "devops")
    print("All tests passed");