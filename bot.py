#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from nonebot.adapters.qqguild import Adapter as QQGuildAdapter
from nonebot.adapters.kaiheila import Adapter as KaiheilaAdapter
from nonebot.log import logger, default_format

# 配置logger
logger.add("logs/{time}.log",
           rotation="04:00",
           retention="10 days",
           diagnose=False,
           level="DEBUG",
           format=default_format)

# 初始化nonebot
nonebot.init()
app = nonebot.get_asgi()

# 注册adapter
driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)
driver.register_adapter(QQGuildAdapter)
driver.register_adapter(KaiheilaAdapter)

# 加载插件
nonebot.load_from_toml("pyproject.toml")
nonebot.load_plugins("plugins")

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
