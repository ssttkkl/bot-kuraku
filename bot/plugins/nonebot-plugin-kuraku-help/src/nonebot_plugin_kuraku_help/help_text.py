import json
import os
from io import StringIO
from pathlib import Path
from typing import Optional

import nonebot
import yaml
from nonebot import logger, Bot, Adapter
from nonebot.internal.adapter import Event
from nonebot.plugin import PluginMetadata

from nonebot_plugin_access_control_api.service import get_plugin_service
from .config import help_conf
from .utils import default_cmd_start

_metadata = {}


@nonebot.get_driver().on_startup
def prepare_metadata():
    # 兼容格式：https://github.com/bot-ssttkkl/nonebot_plugin_llm_plugins_call?tab=readme-ov-file#%E4%BF%AE%E6%94%B9%E6%8F%92%E4%BB%B6metadata%E4%B8%BA%E8%87%AA%E5%AE%9A%E4%B9%89%E5%86%85%E5%AE%B9
    metadata_mixin_file = Path(os.getcwd()) / "data" / "metadata_mixin.yaml"
    metadata_mixin = {}

    if metadata_mixin_file.exists():
        with open(metadata_mixin_file, "r", encoding="utf-8") as f:
            for metadata in yaml.load(f, Loader=yaml.CLoader):
                plugin_name = metadata["module_name"]
                del metadata["module_name"]

                if "config" in metadata:
                    metadata["config"] = eval(metadata["config"])
                if "supported_adapters" in metadata:
                    metadata["supported_adapters"] = set(metadata["supported_adapters"])
                metadata_mixin[plugin_name] = metadata
                logger.opt(colors=True).success(f"Loaded metadata mixin for plugin \"<y>{plugin_name}</y>\"")

    for plugin in nonebot.get_loaded_plugins():
        if plugin.name in help_conf.kuraku_help_ignore_plugin or plugin.name == "nonebot_plugin_kuraku_help":
            continue

        metadata = plugin.metadata
        if metadata is None:
            metadata = PluginMetadata(name=plugin.name, description="", usage="")

        if plugin.name in metadata_mixin:
            metadata = dict(name=metadata.name, description=metadata.description, usage=metadata.usage,
                            type=metadata.type, homepage=metadata.homepage,
                            config=metadata.config, supported_adapters=metadata.supported_adapters,
                            extra=metadata.extra)
            for k, v in metadata_mixin[plugin.name].items():
                metadata[k] = v
            metadata = PluginMetadata(**metadata)

        if metadata.type == "application":
            _metadata[plugin.name] = metadata


_plugin_name_mapping = None


def _get_real_plugin_name(raw: str) -> Optional[str]:
    global _plugin_name_mapping

    if _plugin_name_mapping is None:
        logger.trace("build plugin name mapping...")
        mapping = {}
        for plugin in nonebot.plugin.get_loaded_plugins():
            metadata = _metadata.get(plugin.name)
            if metadata is None:
                continue

            mapping[metadata.name] = plugin.name
            mapping[plugin.name] = plugin.name

        _plugin_name_mapping = mapping

    return _plugin_name_mapping.get(raw, None)


def _is_adapter_supported(plugin_name: str, adapter: Adapter):
    adapter_module = adapter.__module__.removesuffix(".adapter")

    metadata = _metadata.get(plugin_name)
    if metadata is None:
        return False
    return metadata.supported_adapters is None or (
            adapter_module.replace("nonebot.adapters.", "~") in metadata.supported_adapters
            or
            adapter_module in metadata.supported_adapters
    )


async def general_help_text(bot: Bot, event: Event) -> str:
    plugin_metadata = []
    for plugin in nonebot.plugin.get_loaded_plugins():
        metadata = _metadata.get(plugin.name)
        if metadata is None:
            continue

        plugin_service = get_plugin_service(plugin.name)
        if plugin_service is not None and not await plugin_service.check(bot, event, acquire_rate_limit_token=False):
            continue

        if not _is_adapter_supported(plugin.name, bot.adapter):
            continue

        plugin_metadata.append(metadata)

    plugin_metadata.sort(key=lambda x: x.name)

    with StringIO() as sio:
        if help_conf.kuraku_general_help_header:
            sio.write(help_conf.kuraku_general_help_header)
            sio.write('\n')

        sio.write("【已加载插件】\n")
        for metadata in plugin_metadata:
            sio.write(f"- {metadata.name}：{metadata.description}\n")

        sio.write("\n")
        sio.write(f"使用“{default_cmd_start}help <插件名>”以查询插件用法\n")

        if help_conf.kuraku_general_help_footer:
            sio.write(help_conf.kuraku_general_help_footer)
            sio.write('\n')

        return sio.getvalue().strip()


def _build_plugin_help_text(plugin_name: str) -> Optional[str]:
    logger.trace(f"building help text of plugin {plugin_name}...")

    metadata = _metadata.get(plugin_name)
    if metadata is None:
        return None

    with StringIO() as sio:
        if help_conf.kuraku_plugin_help_header:
            sio.write(help_conf.kuraku_plugin_help_header)
            sio.write('\n')

        sio.write(f"【{metadata.name}】{metadata.description}\n")
        sio.write(metadata.usage)

        if help_conf.kuraku_plugin_help_footer:
            sio.write(help_conf.kuraku_plugin_help_footer)
            sio.write('\n')

        return sio.getvalue().strip()


_plugin_help_text_cache = {}


async def plugin_help_text(plugin_name: str, bot: Bot, event: Event) -> Optional[str]:
    plugin_name = _get_real_plugin_name(plugin_name)
    if plugin_name is None:
        return None

    plugin_service = get_plugin_service(plugin_name)
    if plugin_service is not None and not await plugin_service.check(bot, event, acquire_rate_limit_token=False):
        return None

    if not _is_adapter_supported(plugin_name, bot.adapter):
        return None

    if plugin_name in _plugin_help_text_cache:
        return _plugin_help_text_cache[plugin_name]

    text = _build_plugin_help_text(plugin_name)
    if text is not None:
        _plugin_help_text_cache[plugin_name] = text
    return text


__all__ = ("general_help_text", "plugin_help_text")
