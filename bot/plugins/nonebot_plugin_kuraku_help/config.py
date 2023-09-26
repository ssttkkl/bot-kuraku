from typing import Optional, List

from nonebot import get_driver
from pydantic import BaseSettings, Field


class HelpConfig(BaseSettings):
    kuraku_general_help_header: Optional[str]
    kuraku_general_help_footer: Optional[str]
    kuraku_plugin_help_header: Optional[str]
    kuraku_plugin_help_footer: Optional[str]

    kuraku_help_ignore_plugin: List[str] = Field(default_factory=list)

    class Config:
        extra = "ignore"


help_conf = HelpConfig(**get_driver().config.dict())

__all__ = ("HelpConfig", "help_conf")
