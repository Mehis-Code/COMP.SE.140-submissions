from flask import Flask, request
import os
import subprocess

app = Flask(__name__)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    # Verify if the request has a valid token or comes from a trusted source (optional)
    if request.method == 'POST':
        # Trigger Docker Compose down command to stop containers
        subprocess.call(['docker-compose', 'down'])
        return "Shutdown signal received. Shutting down containers.", 200
    return "Invalid request", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)