from io import StringIO
from typing import Optional

import nonebot
from nonebot import logger
from nonebot.plugin import PluginMetadata

from .config import help_conf
from .utils import default_cmd_start


def _get_metadata(plugin_name: str) -> Optional[PluginMetadata]:
    if plugin_name in help_conf.kuraku_custom_plugin_metadata:
        return help_conf.kuraku_custom_plugin_metadata[plugin_name]
    else:
        plugin = nonebot.plugin.get_plugin(plugin_name)
        if plugin is not None:
            return plugin.metadata
        else:
            return None


_plugin_name_mapping = None


def _get_real_plugin_name(raw: str) -> Optional[str]:
    global _plugin_name_mapping

    if _plugin_name_mapping is None:
        logger.trace("build plugin name mapping...")
        mapping = {}
        for plugin in nonebot.plugin.get_loaded_plugins():
            metadata = _get_metadata(plugin.name)
            if metadata is None:
                continue

            mapping[metadata.name] = plugin.name
            mapping[plugin.name] = plugin.name

        _plugin_name_mapping = mapping

    return _plugin_name_mapping.get(raw, None)


def _build_general_help_text():
    logger.trace("building general help text...")

    plugin_metadata = []
    for plugin in nonebot.plugin.get_loaded_plugins():
        metadata = _get_metadata(plugin.name)
        if metadata is None:
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


_general_help_text_cache = None


def general_help_text() -> str:
    global _general_help_text_cache

    if _general_help_text_cache is None:
        _general_help_text_cache = _build_general_help_text()
    return _general_help_text_cache


def _build_plugin_help_text(plugin_name: str) -> Optional[str]:
    logger.trace(f"building help text of plugin {plugin_name}...")

    metadata = _get_metadata(plugin_name)
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


def plugin_help_text(plugin_name: str) -> Optional[str]:
    plugin_name = _get_real_plugin_name(plugin_name)
    if plugin_name is None:
        return None

    if plugin_name in _plugin_help_text_cache:
        return _plugin_help_text_cache[plugin_name]

    text = _build_plugin_help_text(plugin_name)
    if text is not None:
        _plugin_help_text_cache[plugin_name] = text
    return text


__all__ = ("general_help_text", "plugin_help_text")