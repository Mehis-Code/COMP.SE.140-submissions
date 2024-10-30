1. Clone this with git clone
2. docker-compose up --build
   OR
3. docker compose up --build
   Wait a little bit, I tried to optimize the build a little bit, but I hope it's not too bad
4. go to http://localhost:8198
   Request should work, and it can be seen from logs that they come from different service1 instances
   Stop should work, but it can take some time to work. Logs in chat when instances are shut down
   I guess as in the instructions, this type of functionality is not common practice
