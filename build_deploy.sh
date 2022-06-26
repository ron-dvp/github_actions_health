#!/bin/sh

# MAKING SURE DOCKER SWARM IS INITALIZED
SWARM_STATUS=$(docker info --format '{{.Swarm.LocalNodeState}}')

MYIP=$(hostname -I | awk '{print $1}')

if [ "$SWARM_STATUS" != active ]; then
    echo Setting up "$MYIP" as node manager
    docker swarm init
fi
# BUILDING IMAGE 
docker build . -t github_status

# DEPLOYING SERVICE AS BABY NODE
docker stack deploy --compose-file docker-compose.swarm.yml health

exit 0