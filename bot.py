#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from nonebot.adapters.qqguild import Adapter as QQGuildAdapter
from nonebot.adapters.telegram import Adapter as TelegramAdapter
from nonebot.adapters.kaiheila import Adapter as KaiheilaAdapter

# 初始化nonebot
nonebot.init()
app = nonebot.get_asgi()

# 注册adapter
driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)
driver.register_adapter(QQGuildAdapter)
driver.register_adapter(TelegramAdapter)
driver.register_adapter(KaiheilaAdapter)

# 加载插件
nonebot.load_from_toml("pyproject.toml")
nonebot.load_plugins("plugins")

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
