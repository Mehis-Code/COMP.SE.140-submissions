import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket 
import json
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        # Log the first request
        logging.info(f"Received GET request from {self.client_address[0]}:{self.client_address[1]} for {self.path}")
        # Using socket and subprocess libraries to access needed info, found info on internet
        hostname = socket.gethostname()
        IP = socket.gethostbyname(hostname)
        processInfo = subprocess.check_output(['ps', 'ax']).decode('utf-8').split('\n')
        diskSpaceInfo = subprocess.check_output(['df', '-h']).decode('utf-8').split('\n')

        # Very janky formatting for ProcessInfo, but works, needed a little copilot head-bashing for help
        processes = {}
        for process in processInfo[1:]:
            if process.strip():
                columns = process.split(None, 4)
                if len(columns) >= 4:
                    pid, tty, time, cmd = columns[:4]
                    cmd = columns[3] + " " + columns[4]
                    processes[pid] = { "TTY": tty, "TIME": time, "CMD": cmd }

        # Reading time since booted, found snipped online
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = f"{int(uptime_seconds // 3600)} hours, {int((uptime_seconds % 3600) // 60)} minutes"

        response_data = {
            "IP Address": IP,
            "Running Processes": processes,
            "Available Disk Space": diskSpaceInfo,
            "Time since last booted": uptime_string,
        }
        # Turning data to JSON format
        response_json = json.dumps(response_data, indent=4)

        # Sending response back
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response_json.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Server, port=8200):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    logging.info(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()