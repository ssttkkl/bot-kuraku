from typing import Optional

from nonebot import get_driver
from pydantic import BaseSettings


class Config(BaseSettings):
    error_alert_send_to: Optional[int] = None
    error_alert_cron: str = '0 0 * * *'

    class Config:
        extra = "ignore"


conf = Config(**get_driver().config.dict())

__all__ = ("conf", "Config")
