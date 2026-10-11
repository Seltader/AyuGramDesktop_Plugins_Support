# -*- coding: utf-8 -*-
"""
AyuGram Desktop Plugin Host & Dispatcher.
Manages plugin lifecycles, setting stores, and dispatches events to/from C++ host.
"""

import importlib.util
import json
import logging
import os
import sys
import traceback
from typing import Any, Dict, List, Optional, Tuple

from base_plugin import BasePlugin, HookResult, HookStrategy
from extera_utils.metadata_parser import get_metadata
import ui.bulletin
import android_utils
import client_utils

logging.basicConfig(level=logging.INFO, format="[%(name)s] %(levelname)s: %(message)s")
logger = logging.getLogger("AyuPluginHost")

class OutgoingMessageParams:
    """Mock/wrapper for params passed to on_send_message_hook."""
    def __init__(self, message: str = "", entities: Any = None, reply_to_msg_id: int = 0):
        self.message = message
        self.entities = entities if entities is not None else []
        self.reply_to_msg_id = reply_to_msg_id

    def __repr__(self):
        return f"<OutgoingMessageParams message={self.message!r} entities_count={len(self.entities)}>"


class PluginEntry:
    def __init__(self, file_path: str, metadata: Dict[str, Any], instance: Optional[BasePlugin] = None):
        self.file_path = file_path
        self.metadata = metadata
        self.instance = instance
        self.is_enabled = False
        self.error: Optional[str] = None


class AyuPluginHost:
    def __init__(self, plugins_dir: Optional[str] = None, settings_file: Optional[str] = None):
        self.plugins_dir = plugins_dir or os.path.join(os.environ.get("APPDATA", "."), "AyuGram", "plugins")
        self.settings_file = settings_file or os.path.join(self.plugins_dir, "plugins_settings.json")
        self.plugins: Dict[str, PluginEntry] = {}
        self.global_settings: Dict[str, Dict[str, Any]] = {}
        self._load_saved_settings()

    def _load_saved_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    self.global_settings = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load settings file: {e}")

    def save_settings(self):
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(self.global_settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")

    def scan_and_load_all(self, directory: Optional[str] = None):
        scan_dir = directory or self.plugins_dir
        if not os.path.exists(scan_dir):
            os.makedirs(scan_dir, exist_ok=True)
            return

        for fname in os.listdir(scan_dir):
            if fname.endswith(".plugin") or fname.endswith(".py"):
                fpath = os.path.join(scan_dir, fname)
                self.load_plugin(fpath)

    def load_plugin(self, file_path: str) -> Optional[PluginEntry]:
        meta = get_metadata(file_path)
        plugin_id = meta.get("__id__", os.path.splitext(os.path.basename(file_path))[0])
        entry = PluginEntry(file_path=file_path, metadata=meta)
        self.plugins[plugin_id] = entry

        try:
            module_name = f"ayu_plugin_{plugin_id}"
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if not spec or not spec.loader:
                raise RuntimeError("Failed to create module spec")
            module = importlib.util.module_module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            # Find BasePlugin subclass
            plugin_cls = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, BasePlugin) and attr is not BasePlugin:
                    plugin_cls = attr
                    break

            if not plugin_cls:
                raise RuntimeError(f"No BasePlugin subclass found in {file_path}")

            instance = plugin_cls()
            instance._plugin_id = plugin_id

            # Initialize settings
            plugin_saved = self.global_settings.get(plugin_id, {})
            instance._init_settings(plugin_saved)

            # Call on_plugin_load
            instance.on_plugin_load()

            entry.instance = instance
            entry.is_enabled = True
            logger.info(f"Loaded plugin [{plugin_id}]: {meta.get('__name__', plugin_id)} v{meta.get('__version__', '1.0')}")
            return entry

        except Exception as e:
            err_msg = traceback.format_exc()
            entry.error = err_msg
            logger.error(f"Error loading plugin {plugin_id}: {e}\n{err_msg}")
            return entry

    def unload_plugin(self, plugin_id: str):
        entry = self.plugins.get(plugin_id)
        if entry and entry.instance:
            try:
                entry.instance.on_plugin_unload()
            except Exception as e:
                logger.error(f"Error unloading {plugin_id}: {e}")
            entry.is_enabled = False

    def on_send_message(self, account: int, text: str, entities: Optional[List[Any]] = None, reply_to: int = 0) -> Tuple[bool, str, List[Any]]:
        """
        Dispatches outgoing message through all active on_send_message_hooks.
        Returns: (is_allowed, final_text, final_entities)
        """
        params = OutgoingMessageParams(message=text, entities=entities, reply_to_msg_id=reply_to)

        for plugin_id, entry in self.plugins.items():
            if not entry.is_enabled or not entry.instance:
                continue
            if not entry.instance._active_hooks.get("send_message", False):
                continue

            try:
                result: HookResult = entry.instance.on_send_message_hook(account, params)
                if result and result.strategy == HookStrategy.CANCEL:
                    logger.info(f"Message cancelled by plugin {plugin_id}")
                    return False, text, entities or []
                elif result and result.strategy == HookStrategy.MODIFY:
                    if result.params:
                        params = result.params
            except Exception as e:
                logger.error(f"Error in on_send_message_hook ({plugin_id}): {e}", exc_info=True)

        return True, str(params.message), list(params.entities)

    def get_settings_schema(self, plugin_id: str) -> List[Dict[str, Any]]:
        """Extracts settings schema for rendering in C++ Qt settings UI."""
        entry = self.plugins.get(plugin_id)
        if not entry or not entry.instance:
            return []
        try:
            widgets = entry.instance.create_settings()
            serialized = []
            for w in widgets:
                item = {
                    "type": w.__class__.__name__,
                    "text": getattr(w, "text", ""),
                    "subtext": getattr(w, "subtext", ""),
                    "icon": getattr(w, "icon", ""),
                }
                if hasattr(w, "key"):
                    item["key"] = w.key
                    item["default"] = getattr(w, "default", None)
                    item["value"] = entry.instance.get_setting(w.key, getattr(w, "default", None))
                serialized.append(item)
            return serialized
        except Exception as e:
            logger.error(f"Error generating settings schema for {plugin_id}: {e}")
            return []

    def set_plugin_setting(self, plugin_id: str, key: str, value: Any):
        entry = self.plugins.get(plugin_id)
        if entry and entry.instance:
            entry.instance.set_setting(key, value)
            if plugin_id not in self.global_settings:
                self.global_settings[plugin_id] = {}
            self.global_settings[plugin_id][key] = value
            self.save_settings()
