from typing import List, Optional

from nonebot import get_driver
from pydantic import BaseSettings, root_validator


class Config(BaseSettings):
    qq_monitor_ignore: List[str] = ["notice.notify.poke", "notice.notify.honor"]

    qq_monitor_auto_approve_friend_add_request: bool = False
    qq_monitor_auto_approve_group_invite_request: bool = False

    qq_monitor_forward_to: Optional[int] = None
    qq_monitor_forward_request: bool = False
    qq_monitor_forward_notice: bool = False

    @root_validator(allow_reuse=True)
    def validate_forward(cls, values):
        if not values["qq_monitor_forward_to"]:
            if values["qq_monitor_forward_request"]:
                raise ValueError("qq_monitor_forward_to is None but qq_monitor_forward_request is True")
            if values["qq_monitor_forward_notice"]:
                raise ValueError("qq_monitor_forward_to is None but qq_monitor_forward_notice is True")
        return values

    class Config:
        extra = "ignore"


conf = Config(**get_driver().config.dict())

__all__ = ("conf", "Config")
