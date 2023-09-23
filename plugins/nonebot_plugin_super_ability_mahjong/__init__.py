from nonebot import require
from nonebot.plugin import PluginMetadata
from ssttkkl_nonebot_utils.nonebot import default_command_start

require("ssttkkl_nonebot_utils")
require("nonebot_plugin_htmlrender")
require("nonebot_plugin_saa")

__usage__ = f"""
- {default_command_start}新建超能力对局：为四家生成超能力麻将技能牌组
- {default_command_start}查牌 <id>：根据超能力麻将技能牌ID查询
- {default_command_start}查牌名 <name>：根据超能力麻将技能牌名查询
""".strip()

__plugin_meta__ = PluginMetadata(
    name="超能力麻将",
    description="超能力麻将牌组生成器",
    usage=__usage__,
    type="application"
)

from . import main
