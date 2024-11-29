1. Clone this with git clone
2. docker-compose up --build
   OR
3. docker compose up --build
   Takes a while to load up
4. go to http://localhost:8198
   LOGIN INFO in login.txt
   Requests should be in working condition
   when visiting the site
5. The API on http://localhost:8197
   can be tested with commands in this way:
   curl -X PUT -d "RUNNING" localhost:8197/state -H "Content-Type: text/plain" -u user1:devops
   curl -X PUT -d "INIT" localhost:8197/state -H "Content-Type: text/plain" -u user1:devops
   curl -X PUT -d "SHUTDOWN" localhost:8197/state -H "Content-Type: text/plain" -u user1:devops
   curl -X PUT -d "PAUSED" localhost:8197/state -H "Content-Type: text/plain" -u user1:devops
   curl -X GET localhost:8197/state
   curl -X GET localhost:8197/request
   curl -X GET localhost:8197/run-log
6. The state command requires credentials as per spec, and others don't
7. The tests in /tests are only for the use of the pipeline
8. Note that Shutdown shuts down the entire system and all containers
