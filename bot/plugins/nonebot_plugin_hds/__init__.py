from datetime import datetime

from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.adapters import Message
from nonebot.internal.matcher import Matcher
from nonebot.params import CommandArg


class Place:
    count: int
    update_time: datetime

    def __init__(self, place_name: str, place_shortname: str):
        self.place_name = place_name
        self.place_shortname = place_shortname

        self.count = 0
        self.update_time = datetime.fromtimestamp(0)

        query_place = on_command(f"查询{place_name}状态",
                                 aliases={f"{place_shortname}几",
                                          f"{place_name}几"},
                                 priority=5)
        query_place.append_handler(self.query_state)

        update_place = on_command(place_name,
                                  aliases={place_shortname},
                                  priority=5)
        update_place.append_handler(self.update_count)

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

    async def query_state(self, bot: Bot, event: Event):
        if self.update_time.date() != datetime.now().date():
            msg = f"{self.place_name}现在0人 (今日未更新数据，更新数据请使用“/{self.place_name}3”或“/{self.place_shortname}+1”。)"
        else:
            msg = f"{self.place_name}现在{self.count}人 (更新于{self.update_time.strftime('%H:%M')}，更新数据请使用“/{self.place_name}3”或“/{self.place_shortname}+1”。)"
        await bot.send(event=event, message=msg)

    async def update_count(self, bot: Bot, event: Event, matcher: Matcher, args: Message = CommandArg()):
        plain_text = args.extract_plain_text()
        try:
            if plain_text[0] == '+':
                n1 = int(plain_text[1:])
                self.plus(n1)
            elif plain_text[0] == '-':
                n1 = int(plain_text[1:])
                self.plus(-n1)
            else:
                n1 = int(plain_text)
                self.set(n1)
        except ValueError:
            await matcher.finish(message="命令格式错误")

        await bot.send(event=event, message=f"更新成功，现{self.place_name}人数为{self.count}")


hds = Place("活动室", "hds")
syt = Place("三元亭", "syt")
