from flask import Flask
import datetime

app = Flask(__name__)

state = "INIT"
log = []
#dummy responses to test pipeline
@app.route('/state', methods=['GET'])
def get_state():
    return state, 200

@app.route('/state', methods=['PUT'])
def set_state():
    return state, 200

@app.route('/request', methods=['GET'])
def handle_request():
    return state, 200

@app.route('/run-log', methods=['GET'])
def get_run_log():
    return str(log), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8197)