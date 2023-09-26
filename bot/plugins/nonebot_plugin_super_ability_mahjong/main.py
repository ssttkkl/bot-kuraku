import json
import random

from nonebot import on_command, get_driver
from nonebot.adapters import Bot, Event
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot_plugin_htmlrender import md_to_pic
from nonebot_plugin_saa import MessageFactory, Image

data = []


@get_driver().on_startup
def load_data():
    with open('./data/super_ability_mahjong/superMahjongData.json', 'r') as json_file:
        data.extend(json.load(json_file))


@on_command("sid", aliases={"查牌", "id"}, priority=5).handle()
async def select_by_id(bot: Bot, event: Event, args: Message = CommandArg()):
    target_id = args.extract_plain_text()
    for element in data:
        if element["id"] == target_id:
            await bot.send(event=event, message=f"{element['id']}. {element['name']}: {element['details']}")
            break


@on_command("sname", aliases={"查牌名", "sn"}, priority=5).handle()
async def select_by_name(bot: Bot, event: Event, args: Message = CommandArg()):
    target_name = args.extract_plain_text()
    for element in data:
        if element["name"] == target_name:
            await bot.send(event=event, message=f"{element['id']}. {element['name']}: {element['details']}")
            break


@on_command("新建超能力对局", aliases={"随机超能力牌组", "sam"}, priority=5).handle()
async def rand_12_cards():
    random_ids = random.sample(range(1, 50), 12)
    east, south, west, north = [], [], [], []
    for random_id in random_ids:
        element = next(
            (item for item in data if item["id"] == str(random_id)), None)
        if element:
            if len(east) < 3:
                east.append(element)
            elif len(south) < 3:
                south.append(element)
            elif len(west) < 3:
                west.append(element)
            else:
                north.append(element)

    output = f"## 东家抽到的牌组为：" \
             "\n" \
             f"- **{east[0]['id']}. {east[0]['name']}**：{east[0]['details']}\n" \
             f"- **{east[1]['id']}. {east[1]['name']}**：{east[1]['details']}\n" \
             f"- **{east[2]['id']}. {east[2]['name']}**：{east[2]['details']}\n" \
             "\n" \
             f"## 南家抽到的牌组为：" \
             "\n" \
             f"- **{south[0]['id']}. {south[0]['name']}**：{south[0]['details']}\n" \
             f"- **{south[1]['id']}. {south[1]['name']}**：{south[1]['details']}\n" \
             f"- **{south[2]['id']}. {south[2]['name']}**：{south[2]['details']}\n" \
             "\n" \
             f"## 西家抽到的牌组为：" \
             "\n" \
             f"- **{west[0]['id']}. {west[0]['name']}**：{west[0]['details']}\n" \
             f"- **{west[1]['id']}. {west[1]['name']}**：{west[1]['details']}\n" \
             f"- **{west[2]['id']}. {west[2]['name']}**：{west[2]['details']}\n" \
             "\n" \
             f"## 北家抽到的牌组为：" \
             "\n" \
             f"- **{north[0]['id']}. {north[0]['name']}**：{north[0]['details']}\n" \
             f"- **{north[1]['id']}. {north[1]['name']}**：{north[1]['details']}\n" \
             f"- **{north[2]['id']}. {north[2]['name']}**：{north[2]['details']}。\n" \
             "\n" \
             f"请各家在抽到的牌组中选择一张牌作为本局技能。"

    image = await md_to_pic(output)
    await MessageFactory(Image(image)).send()
