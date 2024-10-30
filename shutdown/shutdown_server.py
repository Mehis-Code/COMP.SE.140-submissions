import docker
from flask import Flask, request
import os
import threading
import logging

app = Flask(__name__)

#genius solution from online
#my initial idea was to try to use docker compose down as a script, but i could not make it work
@app.route('/shutdown', methods=['POST'])
def shutdown():
    logging.info('Shutdown service called')
    client = docker.from_env()
    containers = client.containers.list()
    for container in containers:
        if 'shutdown' not in container.name:
            container.kill()

    def shut():
        import time
        time.sleep(1)  
        os._exit(0)
    threading.Thread(target=shut).start()
    return 'System shutdown in progress'

if __name__ == '__main__':
    print("Flask server starting..")
    app.run(host='0.0.0.0', port=5000)