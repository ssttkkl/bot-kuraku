# bot-kuraku

```shell
docker run --network bot-net -v /etc/pixivbot/.env.prod:/app/.env.prod --name bot -e HOST=0.0.0.0 -e PORT=8080 -d ssttkkl/bot-kuraku:main
```