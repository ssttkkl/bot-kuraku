from cachetools import TTLCache
from nonebot import on_request, logger, on_fullmatch
from nonebot.adapters.onebot.v11 import Bot, GroupRequestEvent, Event, Message, MessageSegment, PrivateMessageEvent, \
    FriendRequestEvent, ActionFailed
from nonebot.internal.matcher import Matcher

from .config import conf
from .utils import get_reply_message_id
from .utils import map_user, map_group

context = TTLCache[int, Event](4096, 86400 * 3)
latest_request = TTLCache[str, Event](4096, 86400 * 3)


# ========== Friend Add ==========
def _friend_add_request(event: Event) -> bool:
    return isinstance(event, FriendRequestEvent)


friend_add = on_request(_friend_add_request)

if conf.qq_monitor_auto_approve_friend_add_request:
    @friend_add.handle()
    async def auto_approve_friend_add(bot: Bot, event: FriendRequestEvent, matcher: Matcher):
        await event.approve(bot)
        logger.success(f"auto approved {event}")
        await matcher.finish()

if conf.qq_monitor_forward_request:
    @friend_add.handle()
    async def forward_friend_add(bot: Bot, event: FriendRequestEvent):
        msg = Message(MessageSegment.text(f"收到来自用户{await map_user(event.user_id)}的好友申请。回复“同意”或“拒绝”处理此申请。"))
        send_result = await bot.send_private_msg(user_id=conf.qq_monitor_forward_to, message=msg)
        logger.success(f"forwarded request {event}")

        context[send_result["message_id"]] = event
        latest_request[bot.self_id] = event


# ========== Group Invite ==========
def _group_invite_request(event: Event) -> bool:
    return isinstance(event, GroupRequestEvent) and event.sub_type == "invite"


group_invite = on_request(_group_invite_request)

if conf.qq_monitor_auto_approve_group_invite_request:
    @group_invite.handle()
    async def auto_approve_group_invite(bot: Bot, event: GroupRequestEvent, matcher: Matcher):
        await event.approve(bot)
        logger.success(f"auto approved {event}")
        await matcher.finish()

if conf.qq_monitor_forward_request:
    @group_invite.handle()
    async def forward_group_invite(bot: Bot, event: GroupRequestEvent):
        msg = Message(MessageSegment.text(f"收到来自群{await map_group(event.group_id)}的入群邀请。回复“同意”或“拒绝”处理此申请。"))
        send_result = await bot.send_private_msg(user_id=conf.qq_monitor_forward_to, message=msg)
        logger.success(f"forwarded request {event}")

        context[send_result["message_id"]] = event
        latest_request[bot.self_id] = event

# ========== Operation ==========
if conf.qq_monitor_forward_request:
    def make_operation_handler(for_approve: bool):
        async def handler(bot: Bot, event: PrivateMessageEvent, matcher: Matcher):
            request = None

            message_id = get_reply_message_id(event)
            if message_id is not None and message_id in context:
                request = context[message_id]
                del context[message_id]
                if bot.self_id in latest_request and latest_request[bot.self_id] == request:
                    del latest_request[bot.self_id]
            elif bot.self_id in latest_request:
                request = latest_request[bot.self_id]
                del latest_request[bot.self_id]

            if request is None:
                await matcher.finish("没有收到请求")

            try:
                if for_approve:
                    await request.approve(bot)
                    logger.success(f"approved {request}")
                    await matcher.send("成功同意请求")
                else:
                    await request.reject(bot)
                    logger.success(f"rejected {request}")
                    await matcher.send("成功拒绝请求")
            except ActionFailed as e:
                await matcher.send("请求处理失败，或许是因为你已经处理过该请求")
            except Exception as e:
                await matcher.send(f"内部错误：{type(e)}{str(e)}")

        return handler


    def _forward_to_only(event: PrivateMessageEvent):
        return event.user_id == conf.qq_monitor_forward_to


    approve_matcher = on_fullmatch("同意", permission=_forward_to_only)
    approve_matcher.handle()(make_operation_handler(True))

    reject_matcher = on_fullmatch("拒绝", permission=_forward_to_only)
    reject_matcher.handle()(make_operation_handler(False))
