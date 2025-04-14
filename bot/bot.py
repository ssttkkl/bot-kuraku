#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# hook方式解决[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1010)
import ssl

context = ssl.create_default_context()
context.set_ciphers(
    "@SECLEVEL=2:ECDH+AESGCM:ECDH+CHACHA20:ECDH+AES:DHE+AES:AESGCM:!aNULL:!eNULL:!aDSS:!SHA1:!AESCCM:!PSK"
)

# 设置为全局默认上下文
def new_create_default_context(*args, **kwargs):
    return context

ssl.create_default_context = new_create_default_context


import nonebot

# 初始化nonebot
nonebot.init()
app = nonebot.get_asgi()

from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from nonebot.adapters.qq import Adapter as QQAdapter

# 注册adapter
driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)
driver.register_adapter(QQAdapter)

# 加载插件
nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
