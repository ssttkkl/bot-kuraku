#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot

# 初始化nonebot
nonebot.init()
app = nonebot.get_asgi()

from nonebot_adapter_onebot_pretender import init_onebot_pretender, create_ob11_adapter_pretender

init_onebot_pretender()

from nonebot.adapters.red import Adapter as RedAdapter
from nonebot.adapters.kaiheila import Adapter as KaiheilaAdapter
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from nonebot.adapters.onebot.v12 import Adapter as ONEBOT_V12Adapter
from nonebot.adapters.qqguild import Adapter as QQGuildAdapter
from nonebot.adapters.telegram import Adapter as TelegramAdapter

# 注册adapter
driver = nonebot.get_driver()
driver.register_adapter(create_ob11_adapter_pretender(RedAdapter))
driver.register_adapter(ONEBOT_V11Adapter)
driver.register_adapter(ONEBOT_V12Adapter)
driver.register_adapter(QQGuildAdapter)
driver.register_adapter(TelegramAdapter)
driver.register_adapter(KaiheilaAdapter)

if driver.env == 'dev':
    from nonebot.adapters.console import Adapter as ConsoleAdapter

    driver.register_adapter(ConsoleAdapter)

# 加载插件
nonebot.load_from_toml("pyproject.toml")
nonebot.load_plugins("plugins")

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
