if docker-compose pull; then
      QQ_ACCOUNT=$(cat qq.txt) docker-compose up -d
    echo 'y' | docker image prune
fi
