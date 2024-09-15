cd $(dirname $0)
if docker-compose pull; then
    COMPOSE_HTTP_TIMEOUT=300 QQ_ACCOUNT=$(cat qq.txt) docker-compose up -d
    echo 'y' | docker image prune
fi
