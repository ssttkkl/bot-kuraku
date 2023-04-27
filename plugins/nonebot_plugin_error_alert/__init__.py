import traceback
from datetime import datetime
from io import StringIO
from typing import Optional, Text, NamedTuple, Type, List

import nonebot
from apscheduler.triggers.cron import CronTrigger
from nonebot import logger, require, on_command
from nonebot.adapters.onebot.v11 import Bot
from nonebot.internal.adapter import Event
from nonebot.log import default_format
from nonebot.permission import SUPERUSER

from .config import conf

require("nonebot_plugin_saa")
from nonebot_plugin_saa import AggregatedMessageFactory, MessageFactory, TargetQQPrivate, PlatformTarget, extract_target

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler

MODULE_NAME = __name__.split(".")[-1]


class ErrorAlert(NamedTuple):
    summary: str
    exc_type: Optional[Type[BaseException]]


async def to_error_alert(msg):
    record = msg.record

    with StringIO() as sio:
        if record["message"]:
            sio.write(f"{record['message']}\n")

        sio.write("\n")

        sio.write(f"时间：{record['time'].strftime('%Y-%m-%d %H:%M:%S')}\n")
        sio.write(f"日志记录位置：File {record['file'].path}, line {record['line']}, in {record['function']}\n")

        if record["exception"] is not None:
            event: Optional[Event] = None
            plugins = []
            last_frame = None

            tb = record["exception"].traceback
            for frame, line_no in traceback.walk_tb(tb):
                last_frame = frame
                if "event" in frame.f_locals and isinstance(frame.f_locals["event"], Event):
                    event = frame.f_locals["event"]

                plugin = nonebot.get_plugin_by_module_name(frame.f_globals["__name__"])
                if plugin is not None and (len(plugins) == 0 or plugin != plugins[-1]):
                    plugins.append(plugin)

            e = record["exception"].value
            sio.write(f"异常：<{type(e).__qualname__}> {e}\n")

            if last_frame is not None:
                summary = traceback.extract_stack(last_frame)[-1]
                sio.write(f"异常抛出位置：File {summary.filename}, line {summary.lineno}, in {summary.name}\n")
                sio.write(f"    {summary.line}\n")

            if plugins is not None:
                sio.write(f"插件：{'->'.join(map(lambda p: p.name, plugins))}\n")

            if event is not None:
                sio.write(f"事件：{event.get_event_description()}\n")

        if record["thread"].name != 'MainThread':
            sio.write(f"线程：{record['thread'].name} (tid: {record['thread'].id})\n")

        if record["process"].name != 'MainProcess':
            sio.write(f"进程：{record['process'].name} (tid: {record['process'].id})\n")

        return ErrorAlert(summary=sio.getvalue().strip(),
                          exc_type=type(record["exception"].value) if record["exception"] is not None else None)


last_fetch: datetime = datetime.now()
pending: List[ErrorAlert] = []


async def handler(msg):
    text = await to_error_alert(msg)
    pending.append(text)


logger.add(handler,
           level="ERROR",
           # 不处理本插件抛出的异常，避免无限套娃
           filter=lambda r: r["name"] != MODULE_NAME,
           format=default_format)


async def send(bot: Bot, target: PlatformTarget, *, silently: bool = False):
    global last_fetch

    data = pending.copy()
    pending.clear()

    last_fetch_ = last_fetch
    last_fetch = datetime.now()

    with StringIO() as sio:
        sio.write(last_fetch_.strftime('%Y-%m-%d %H:%M'))
        sio.write("至今")

        if len(data) == 0:
            sio.write("无新增报错")
        else:
            sio.write(f"新增{len(data)}次报错\n")

            grouped = {}
            for x in data:
                if x.exc_type not in grouped:
                    grouped[x.exc_type] = []
                grouped[x.exc_type].append(x)

            groups = [(k, grouped[k]) for k in grouped]
            groups = sorted(groups,
                            key=lambda g: len(g[1]),
                            reverse=True)

            for i in range(0, min(len(groups), 10)):
                exc_type, li = groups[i]

                if exc_type is not None:
                    sio.write(f"<{exc_type.__qualname__}>")
                else:
                    sio.write("<非异常>")

                sio.write(f" {len(li)}次\n")

            if len(groups) > 10:
                sio.write("……")

        if len(data) > 0 or not silently:
            summary = sio.getvalue().strip()
            await MessageFactory(Text(summary)).send_to(bot=bot, target=target)

    factories = list(map(lambda x: MessageFactory(Text(x.summary)), data))
    for i in range(0, len(factories), 99):
        await AggregatedMessageFactory(factories[i:min(len(factories), i + 50)]).send_to(bot=bot, target=target)


@scheduler.scheduled_job(id="nonebot_plugin_apscheduler.alert",
                         trigger=CronTrigger.from_crontab(conf.error_alert_cron))
async def alert():
    bot = nonebot.get_bot()
    if bot is not None:
        await send(bot=nonebot.get_bot(), target=TargetQQPrivate(user_id=conf.error_alert_send_to), silently=True)
    else:
        logger.warning("no bot was found")


@on_command("error_insight", permission=SUPERUSER).handle()
async def _(bot: Bot, event: Event):
    await send(bot=bot, target=extract_target(event))
