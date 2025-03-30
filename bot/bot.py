#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
nonebot.load_plugins("plugins")

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
