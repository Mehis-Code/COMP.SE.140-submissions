from flask import Flask
import datetime
import docker
import requests
from docker.models.containers import Container

app = Flask(__name__)

state = "INIT"
log = ["INIT"]
#dummy responses to test pipeline
@app.route('/state', methods=['GET'])
def get_state():
    return state, 200

@app.route('/state', methods=['PUT'])
def set_state():
    #Testing pausing
    client: docker.DockerClient = docker.from_env()
    container: Container = client.containers.get('devops-nginx-1')
    state = "PAUSED";
    prevState = log[-1]
    log.append(f"State changed to {state} from {prevState} at {datetime.datetime.now()}")
    container.pause();
    container.unpause();
    #requests.post("http://docker:8198/shutdown/")
    return state, 200

@app.route('/request', methods=['GET'])
def handle_request():
    return state, 200

@app.route('/run-log', methods=['GET'])
def get_run_log():
    return str(log), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8197)