from flask import Flask
import datetime
import docker
import requests
from docker.models.containers import Container

app = Flask(__name__)

creation_time = f"State initialized at {datetime.datetime.now()}"
state = "INIT"
log = [creation_time]

#dummy responses to test pipeline
@app.route('/state', methods=['GET'])
def get_state():
    return state, 200

@app.route('/state', methods=['PUT'])
def set_state():

    prevState = state
    #Valid states
    if state in ["PAUSED", "SHUTDOWN", "INIT", "RUNNING"]:
        state = request.data.decode('utf-8')
    else:
        return "Invalid state", 400
    
    client: docker.DockerClient = docker.from_env()
    container: Container = client.containers.get('devops-nginx-1')
    match state:
        case "PAUSED":
            container.pause();
        case "SHUTDOWN":
            requests.post("http://docker:8198/shutdown/")
        case "INIT":
            container.start();
        case "RUNNING":
            container.start();
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