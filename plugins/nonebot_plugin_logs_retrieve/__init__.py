import os.path
from os import walk
from tempfile import TemporaryFile
from zipfile import ZipFile

from nonebot import on_command, require
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot.permission import SUPERUSER
from nonebot.utils import run_sync

require("nonebot_plugin_gocqhttp_cross_machine_upload_file")

from nonebot_plugin_gocqhttp_cross_machine_upload_file import upload_file

logs_matcher = on_command("logs", permission=SUPERUSER)


@run_sync
def pack(f):
    with ZipFile(f, "w") as zf:
        for dirpath, dirnames, filenames in walk("logs"):
            for file in filenames:
                zf.write(os.path.join(dirpath, file))


@logs_matcher.handle()
async def _(bot: Bot, event: MessageEvent):
    with TemporaryFile("wb+") as tmp:
        await pack(tmp)

        tmp.seek(0)

        def iterfile():
            yield from tmp

        await upload_file(bot, event, "logs.zip", iterfile())
