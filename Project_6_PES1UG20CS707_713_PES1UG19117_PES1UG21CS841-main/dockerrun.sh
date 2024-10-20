
# Description: This script is used to run the docker containers. It is used to run the containers in the correct order and with the correct network settings.
docker run -d -p 27017:27017 -v $(pwd)/data:/data/db --name mymongodb --network mongodb -e ALLOW_EMPTY_PASSWORD=yes bitnami/mongodb:latest


docker run -d -p 5000:5000 --link mymongodb:mongo --network mongodb orders-docker 
docker run -d -p 5050:5000 --link mymongodb:mongo --network mongodb products-docker 
docker run -d -p 5100:5000 --link mymongodb:mongo --network mongodb users-docker 


