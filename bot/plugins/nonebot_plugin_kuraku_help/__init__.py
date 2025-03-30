from nonebot import require
from nonebot.plugin import PluginMetadata

from . import matcher
from .utils import default_cmd_start

require("nonebot_plugin_access_control")

help_text = f"""
- {default_cmd_start}help：查看帮助信息
- {default_cmd_start}help <插件名>：查询插件用法
""".strip()

__plugin_meta__ = PluginMetadata(
    name="帮助",
    description="获取帮助信息",
    usage=help_text,
    type="application"
)
