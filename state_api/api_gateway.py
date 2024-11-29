from flask import Flask, request
import datetime
import docker
import requests
import logging

app = Flask(__name__)

creation_time = f"State initialized at {datetime.datetime.now()}"
trueState = "INIT"
log = [creation_time]


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the .htpasswd file

#dummy responses to test pipeline
@app.route('/state', methods=['GET'])
def get_state():
    return trueState, 200

@app.route('/state', methods=['PUT'])
def set_state():
    global trueState
        
    
    client = docker.from_env()
    containers = client.containers.list()
    nginxContainer = ""
    for container in containers:
        if 'service2'  in container.name:
            nginxContainer = container
    if not nginxContainer:
        logging.error("Nginx container not found")
        return "Nginx container not found", 500
    
    logging.info(f"nginx container: {nginxContainer}")

    prevState = trueState
    state = request.data.decode("utf-8").strip('"')
    logging.info(f"State: {state} (type: {type(state)})")
    logging.info(f"Previous state: {prevState} (type: {type(prevState)})")
    if prevState == state:
        logging.info("State request same as current state")
        return state, 200

    global log

    #Valid states
    logging.info(state not in ["PAUSED", "SHUTDOWN", "INIT", "RUNNING"])
    if state not in ["PAUSED", "SHUTDOWN", "INIT", "RUNNING"]:
        return "Invalid state", 400
    
    client: docker.DockerClient = docker.from_env()
    
    match state:
        case "PAUSED":
                nginxContainer.pause();
        case "SHUTDOWN":
            try:
                logging.info("Sending POST request to /shutdown")
                response = requests.post("http://shutdown:5000/shutdown")
                response.raise_for_status()
                return "System shutdown in progress", 200
            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to shutdown the system {e}")
        case "INIT":
                nginxContainer.restart();
        case "RUNNING":
                nginxContainer.unpause();
    
    trueState = state
    log.append(f"State changed to {trueState} from {prevState} at {datetime.datetime.now()}")
    logging.info(f"State changed to {trueState} from {prevState}")
    return trueState, 200

@app.route('/request', methods=['GET'])
def handle_request():
    try:
        response = requests.get("http://service2:8200")
        response.raise_for_status()
        return response.json(), 200
    except:
        return "Error", 500
       

@app.route('/run-log', methods=['GET'])
def get_run_log():
    return str(log), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8197)