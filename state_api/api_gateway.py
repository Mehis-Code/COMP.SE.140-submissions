from flask import Flask, request
import datetime
import docker
import requests
import logging
import base64
from passlib.apache import HtpasswdFile

app = Flask(__name__)

#Initialise variables to store the state and log
creation_time = f"State initialized at {datetime.datetime.now()}"
trueState = "INIT"
log = [creation_time]

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#Get the htpasswd file
htpasswd = HtpasswdFile('/etc/nginx/.htpasswd')

#Get the credentials from the request
def get_credentials():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_type, auth_info = auth_header.split(None, 1)
        if auth_type.lower() == 'basic':
            username, password = base64.b64decode(auth_info).decode('utf-8').split(':', 1)
            return username, password
    return None, None
#Check if the credentials are correct
def verify_credentials(username, password):
    if htpasswd.check_password(username, password):
        return True
    return False

#Getting the state
@app.route('/state', methods=['GET'])
def get_state():
    return trueState, 200

#Changing the state
@app.route('/state', methods=['PUT'])
def set_state():
    global trueState
    global log

    #When the state is INIT, the user must provide credentials
    if trueState == "INIT":
        if not request.headers.get('Authorization'):
            return "No Authorization was provided. System in INIT state", 401
        username, password = get_credentials()
        if not verify_credentials(username, password):
            return "Unauthorized, wrong credentials", 401  
    #Searching for containers    
    service2Container = ""
    nginxContainer = ""
    client = docker.from_env()
    containers = client.containers.list()
    for container in containers:
        if 'service2' in container.name:
            service2Container = container
        if 'nginx' in container.name:
            nginxContainer = container

    #If no containers, return error
    if not service2Container:
        logging.error("Service2 container not found")
        return "Service2 container not found", 500
    if not nginxContainer:
        logging.error("Nginx container not found")
        return "Nginx Container not found", 500
    logging.info(f"nginx container: {service2Container}")

    #Getting the state from the request, and checking if same
    state = request.data.decode("utf-8").strip('"')
    logging.info(f"State: {state} (type: {type(state)})")
    logging.info(f"Previous state: {trueState} (type: {type(trueState)})")
    if trueState == state:
        logging.info("State request same as current state")
        return state, 200

    #Valid states
    logging.info(state not in ["PAUSED", "SHUTDOWN", "INIT", "RUNNING"])
    if state not in ["PAUSED", "SHUTDOWN", "INIT", "RUNNING"]:
        return "Invalid state", 400
    
    client: docker.DockerClient = docker.from_env()
    
    #Based on the state, the containers are paused, unpaused, restarted or shutdown
    match state:
        case "PAUSED":
                service2Container.pause();
        case "SHUTDOWN":
            try:
                logging.info("Sending POST request to /shutdown")
                response = requests.post("http://shutdown:5000/shutdown")
                response.raise_for_status()
                return "System shutdown in progress", 200
            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to shutdown the system {e}")
        case "INIT":
                service2Container.restart();    
                nginxContainer.restart();
        case "RUNNING":
                if trueState != "INIT":
                    service2Container.unpause();
    #Adding to the log and changing the state if all went well
    log.append(f"State changed to {state} from {trueState} at {datetime.datetime.now()}")
    logging.info(f"State changed to {state} from {trueState}")
    trueState = state

    return trueState, 200

#Getting info from services
@app.route('/request', methods=['GET'])
def handle_request():
    try:
        response = requests.get("http://service2:8200")
        response.raise_for_status()
        return response.json(), 200
    except:
        return "Error", 500
       
#Getting the log
@app.route('/run-log', methods=['GET'])
def get_run_log():
    return str(log), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8197)