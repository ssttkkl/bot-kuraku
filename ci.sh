if docker-compose pull; then
    docker-compose up -d
    echo 'y' | docker image prune
fi
