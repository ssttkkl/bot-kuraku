from datetime import datetime

from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.adapters import Message
from nonebot.internal.matcher import Matcher
from nonebot.params import CommandArg


class Place:
    count: int
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


for place_name, place_shortname in {("活动室", "hds"), ("三元亭", "syt")}:
    place = Place()

    query_place = on_command(f"查询{place_name}状态",
                             aliases={f"{place_shortname}几", f"{place_name}几"},
                             priority=5)
    update_place = on_command(place_name, aliases={place_shortname}, priority=5)

    @query_place.handle()
    async def query_state(bot: Bot, event: Event):
        if place.update_time.date() != datetime.now().date():
            msg = f"{place_name}现在0人 (今日未更新数据，更新数据请使用“/{place_name}3”或“/{place_shortname}+1”。)"
        else:
            msg = f"{place_name}现在{place.count}人 (更新于{place.update_time.strftime('%H:%M')}，更新数据请使用“/{place_name}3”或“/{place_shortname}+1”。)"
        await bot.send(event=event, message=msg)

    @update_place.handle()
    async def update_count(bot: Bot, event: Event, matcher: Matcher, args: Message = CommandArg()):
        plain_text = args.extract_plain_text()
        try:
            if plain_text[0] == '+':
                n1 = int(plain_text[1:])
                place.plus(n1)
            elif plain_text[0] == '-':
                n1 = int(plain_text[1:])
                place.plus(-n1)
            else:
                n1 = int(plain_text)
                place.set(n1)
        except ValueError:
            await matcher.finish(message="命令格式错误")

        await bot.send(event=event, message=f"更新成功，现{place_name}人数为{place.count}")
