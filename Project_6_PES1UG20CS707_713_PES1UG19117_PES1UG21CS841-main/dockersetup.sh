cd users-docker
docker build . --tag users-docker


cd ..
cd orders-docker
docker build . --tag orders-docker

cd ..
cd products-docker
docker build . --tag products-docker

cd ..

docker network create --driver bridge mongodb


