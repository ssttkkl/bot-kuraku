from nonebot import on_command
from nonebot.internal.adapter import Event
from nonebot.internal.matcher import Matcher

from .help_text import *

help_matcher = on_command("help", priority=1, aliases={"帮助"})


@help_matcher.handle()
async def _(matcher: Matcher, event: Event):
    args = event.get_message().extract_plain_text().split()
    cmd, args = args[0], args[1:]

    if len(args) == 0:
        await matcher.send(general_help_text())
    else:
        text = plugin_help_text(args[0])
        if text is not None:
            await matcher.send(text)
        else:
            await matcher.send("没有找到这样的插件")
