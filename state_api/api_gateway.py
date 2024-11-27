from flask import Flask
import datetime

app = Flask(__name__)

state = "INIT"
log = []

@app.route('/state', methods=['GET'])
def get_state():
    return state, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8197)