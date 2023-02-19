from datetime import datetime

from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.adapters import Message
from nonebot.internal.matcher import Matcher
from nonebot.params import CommandArg

query_hds = on_command("查询活动室状态", aliases={"hds几", "活动室几"}, priority=5)
update_hds = on_command("活动室", aliases={"hds"}, priority=5)


class HDS:
    count: int  # 应该添加一个每天0：00重置人数为0的操作，但我不知道怎么写
    update_time: datetime

    def __init__(self):
        self.count = 0
        self.update_time = datetime.fromtimestamp(0)

    def set(self, newcount: int):
        if newcount >= 0:
            self.count = newcount
            self.update_time = datetime.now()

        if self.count < 0:
            self.count = 0

    def plus(self, changenum: int):
        if datetime.now().date() != self.update_time.date():
            self.count = 0

        self.update_time = datetime.now()
        self.count = self.count + changenum

        if self.count < 0:
            self.count = 0


hds = HDS()


@query_hds.handle()
async def query_state(bot: Bot, event: Event):
    if hds.update_time.date() != datetime.now().date():
        msg = f"活动室现在0人 (今日未更新数据，更新数据请使用“/活动室3”或“/hds+1”。)"
    else:
        msg = f"活动室现在{hds.count}人 (更新于{hds.update_time.strftime('%H:%M')}，更新数据请使用“/活动室3”或“/hds+1”。)"
    await bot.send(event=event, message=msg)


@update_hds.handle()
async def update_count(bot: Bot, event: Event, matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    try:
        if plain_text[0] == '+':
            n1 = int(plain_text[1:])
            hds.plus(n1)
        elif plain_text[0] == '-':
            n1 = int(plain_text[1:])
            hds.plus(-n1)
        else:
            n1 = int(plain_text)
            hds.set(n1)
    except ValueError:
        await matcher.finish(message="命令格式错误")

    await bot.send(event=event, message="更新成功，现活动室人数为" + str(hds.count))
