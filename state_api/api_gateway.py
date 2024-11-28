from flask import Flask, request
import datetime
import docker
import requests
from docker.models.containers import Container
import logging

app = Flask(__name__)

creation_time = f"State initialized at {datetime.datetime.now()}"
state = "INIT"
log = [creation_time]


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


#dummy responses to test pipeline
@app.route('/state', methods=['GET'])
def get_state():
    return state, 200

@app.route('/state', methods=['PUT'])
def set_state():
    global state
        
    client = docker.from_env()
    containers = client.containers.list()
    nginxContainer = ""
    for container in containers:
        if 'nginx'  in container.name:
            nginxContainer = container
    if not nginxContainer:
        logging.error("Nginx container not found")
        return "Nginx container not found", 500
    
    logging.info(f"nginx container: {nginxContainer}")

    prevState = state
    state = request.data.decode("utf-8")
    if prevState == state:
        return state, 200
    logging.info(f"State:{state}")
    global log

    #Valid states
    
    if state in ["PAUSED", "SHUTDOWN", "INIT", "RUNNING"]:
        print("Valid state")
    else:
        return "Invalid state", 400
    
    client: docker.DockerClient = docker.from_env()
    
    match state:
        case "PAUSED":
            nginxContainer.pause();
        case "SHUTDOWN":
            requests.post("http://localhost:8198/shutdown/")
        case "INIT":
            nginxContainer.restart();
        case "RUNNING":
            nginxContainer.unpause();
    log.append(f"State changed to {state} from {prevState} at {datetime.datetime.now()}")
    container.pause();

    return state, 200

@app.route('/request', methods=['GET'])
def handle_request():
    return state, 200

@app.route('/run-log', methods=['GET'])
def get_run_log():
    return str(log), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8197)