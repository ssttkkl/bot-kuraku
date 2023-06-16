from typing import Optional

from nonebot import logger
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.internal.matcher import current_bot


def get_reply_message_id(event: MessageEvent) -> Optional[int]:
    message_id = None
    for seg in event.original_message:
        if seg.type == "reply":
            message_id = int(seg.data["id"])
            break
    return message_id


async def map_group(group_id: int):
    bot = current_bot.get()
    try:
        group_info = await bot.get_group_info(group_id=group_id)
        return f"{group_info['group_name']} ({group_id})"
    except Exception as e:
        logger.exception(e)
        return str(group_id)


async def map_user(user_id: int):
    bot = current_bot.get()
    try:
        user_info = await bot.get_stranger_info(user_id=user_id)
        return f"{user_info['nickname']} ({user_id})"
    except Exception as e:
        logger.exception(e)
        return str(user_id)
