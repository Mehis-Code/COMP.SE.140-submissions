const http = require('http');
const { execSync } = require('child_process');
const fs = require('fs');

const server = http.createServer((req, res) => {
    if (req.method === 'GET') {
        try {
            //Useful node library for this task
            const IP = execSync('hostname -i').toString().trim();
            //Help from copilot with this one. I had trouble with refactoring to node-alpine
            //because ps -ax does not work on that version
            const processInfo = execSync('ps -o pid,tty,stat,time,args').toString().split('\n');
            const diskSpaceInfo = execSync('df -h').toString().split('\n');

            // Read uptime from /proc/uptime
            const uptimeSeconds = fs.readFileSync('/proc/uptime', 'utf8').split(' ')[0];
            const uptimeString = `${Math.floor(uptimeSeconds / 3600)} hours, ${Math.floor((uptimeSeconds % 3600) / 60)} minutes`;


            const processes = {};
            //A very janky match, I struggled to format the ps-command output, 
            //got help from copilot
            processInfo.slice(1).forEach(line => {
                const columns = line.trim().match(/^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.+)$/);
                if (columns) {
                    const [_, pid, tty, stat, time, args] = columns;
                    processes[pid] = { TTY: tty, STAT: stat, TIME: time, CMD: args };
                }
            });
            //Formatting for S1 data
            const responseData = {
                "Service1 Data": {
                    "IP address": IP,
                    "List of processes running": processes,
                    "Disk space available": diskSpaceInfo,
                    "Time since last booted": uptimeString
                }
            };
            //Directions for get request
            const directions = {
                hostname: 'service2',
                port: 8200,
                path: '/',
                method: 'GET'
            };
            //Getting data from Service2
            const request = http.request(directions, (response) => {
                let data = '';
                response.on('data', (chunk) => {
                    data += chunk;
                });
                response.on('end', () => {
                    let service2Data = JSON.parse(data);
                    //Appending S2data to responseData
                    responseData["Service2 Data"] = service2Data;
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify(responseData, null, 4));
                });
            });
            //Error handling for the get request
            request.on('error', (error) => {
                console.error(`Issue found in Get Request: ${error.message}`);
                responseData["Service2 Data"] = { error: 'Failed to get service2' };
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify(responseData, null, 4));
            });
            request.end();
        } catch (error) {
            // Catch for the big try-catch spoon
            console.error('Error found:', error);
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Error found' }, null, 4));
        }
    }
});

server.listen(8199, () => {
    console.log('Server running at http://localhost:8199/ (This one is accessible!)');
});