from typing import Optional, Dict

from nonebot import get_driver
from nonebot.plugin import PluginMetadata
from pydantic import BaseSettings, Field


class HelpConfig(BaseSettings):
    kuraku_general_help_header: Optional[str]
    kuraku_general_help_footer: Optional[str]
    kuraku_plugin_help_header: Optional[str]
    kuraku_plugin_help_footer: Optional[str]

    kuraku_custom_plugin_metadata: Dict[str, PluginMetadata] = Field(default_factory=dict)

    class Config:
        extra = "ignore"


help_conf = HelpConfig(**get_driver().config.dict())

__all__ = ("HelpConfig", "help_conf")
