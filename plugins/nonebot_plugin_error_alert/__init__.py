from nonebot import require

require("nonebot_plugin_apscheduler")
require("nonebot_plugin_saa")
require("nonebot_plugin_datastore")

MODULE_NAME = __name__.split(".")[-1]

from . import alert
from . import matcher
from . import subscribe
