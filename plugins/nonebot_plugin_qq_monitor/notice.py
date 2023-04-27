from nonebot import on_notice, logger
from nonebot.adapters.onebot.v11 import NoticeEvent, Message, MessageSegment, GroupAdminNoticeEvent, \
    GroupDecreaseNoticeEvent, GroupIncreaseNoticeEvent, GroupBanNoticeEvent, GroupRecallNoticeEvent, \
    PokeNotifyEvent, LuckyKingNotifyEvent, HonorNotifyEvent, FriendAddNoticeEvent, Bot

from nonebot_plugin_onebot_monitor.config import conf
from nonebot_plugin_onebot_monitor.utils import map_group, map_user


async def map_notice_forward_message(notice: NoticeEvent):
    msg = None
    if isinstance(notice, GroupAdminNoticeEvent):
        if notice.sub_type == 'set':
            msg = f"Bot被设置为群聊{await map_group(notice.group_id)}的管理员"
        else:
            msg = f"Bot被取消群聊{await map_group(notice.group_id)}的管理员"
    elif isinstance(notice, GroupDecreaseNoticeEvent):
        if notice.sub_type == 'leave':
            msg = f"Bot主动退出群聊{await map_group(notice.group_id)}"
        else:
            msg = f"Bot被踢出群聊{await map_group(notice.group_id)}（操作人：{await map_user(notice.operator_id)}）"
    elif isinstance(notice, GroupIncreaseNoticeEvent):
        msg = f"Bot加入群聊{await map_group(notice.group_id)}"
    elif isinstance(notice, GroupBanNoticeEvent):
        if notice.sub_type == 'ban':
            msg = f"Bot在群聊{await map_group(notice.group_id)}被禁言{notice.duration / 60}分钟（操作人：{await map_user(notice.operator_id)}）"
        else:
            msg = f"Bot在群聊{await map_group(notice.group_id)}被解除禁言"
    elif isinstance(notice, GroupRecallNoticeEvent):
        if notice.operator_id == notice.self_id:
            msg = f"Bot在群聊{await map_group(notice.group_id)}主动撤回一条消息"
        else:
            msg = f"Bot在群聊{await map_group(notice.group_id)}被撤回一条消息（操作人：{await map_user(notice.operator_id)}）"
    elif isinstance(notice, FriendAddNoticeEvent):
        msg = f"Bot添加了新的好友{await map_user(notice.user_id)}"
    elif isinstance(notice, PokeNotifyEvent):
        if notice.group_id is not None:
            msg = f"Bot在群聊{await map_group(notice.group_id)}被戳一戳（操作人：{await map_user(notice.user_id)}）"
        else:
            msg = f"Bot在私聊中被{await map_user(notice.user_id)}戳一戳"
    elif isinstance(notice, LuckyKingNotifyEvent):
        msg = f"Bot在群聊{await map_group(notice.group_id)}成为红包运气王"
    elif isinstance(notice, HonorNotifyEvent):
        if notice.honor_type == 'talkative':
            msg = f"Bot在群聊{await map_group(notice.group_id)}成为龙王"
        elif notice.honor_type == 'performer':
            msg = f"Bot在群聊{await map_group(notice.group_id)}获得群聊之火"
        elif notice.honor_type == 'emotion':
            msg = f"Bot在群聊{await map_group(notice.group_id)}成为群聊之火"

    if msg is not None:
        return Message(MessageSegment.text(msg))
    else:
        return None


def _notice(event: NoticeEvent):
    # FriendAddNoticeEvent单独判断
    return ((event.is_tome() or isinstance(event, FriendAddNoticeEvent))
            and event.get_event_name() not in conf.qq_monitor_ignore)


monitor_notice_matcher = on_notice(rule=_notice, priority=1)

if conf.qq_monitor_forward_notice:
    @monitor_notice_matcher.handle()
    async def forward_notice(bot: Bot, event: NoticeEvent):
        msg = await map_notice_forward_message(event)
        await bot.send_private_msg(user_id=conf.qq_monitor_forward_to, message=msg)
        logger.success(f"forwarded notice {event}")
