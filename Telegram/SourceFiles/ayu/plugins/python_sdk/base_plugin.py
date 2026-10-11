# -*- coding: utf-8 -*-
"""
exteraGram & AyuGram Plugin SDK Compatibility Layer for AyuGram Desktop.
Provides base classes, hooks, lifecycle management, and setting access.
"""

import logging
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union

# Strategy for handling hook result
class HookStrategy(Enum):
    NONE = 0
    MODIFY = 1
    CANCEL = 2

class HookResult:
    def __init__(self, strategy: HookStrategy = HookStrategy.NONE, params: Any = None):
        self.strategy = strategy
        self.params = params

    def __repr__(self):
        return f"<HookResult strategy={self.strategy} params={self.params}>"

class MethodHookParam:
    """Represents parameters passed to hooked methods."""
    def __init__(self, this_object=None, args=None, result=None, method=None):
        self.thisObject = this_object
        self.args = list(args) if args is not None else []
        self._result = result
        self.method = method
        self.is_cancelled = False

    def getResult(self):
        return self._result

    def setResult(self, result):
        self._result = result

    def setThrowable(self, throwable):
        self._throwable = throwable

    def getThrowable(self):
        return getattr(self, "_throwable", None)


class MethodHook:
    """Base class for Java / Method hooks."""
    def before_hooked_method(self, param: MethodHookParam):
        pass

    def after_hooked_method(self, param: MethodHookParam):
        pass


class PyMethodHook(MethodHook):
    def __init__(self, before: Optional[Callable] = None, after: Optional[Callable] = None):
        self._before = before
        self._after = after

    def before_hooked_method(self, param: MethodHookParam):
        if self._before:
            return self._before(param)

    def after_hooked_method(self, param: MethodHookParam):
        if self._after:
            return self._after(param)


class XposedHook:
    def __init__(self, target, hook_obj):
        self.target = target
        self.hook_obj = hook_obj
        self.is_active = True

    def unhook(self):
        self.is_active = False


class PluginMetadata:
    def __init__(self, plugin_id: str, name: str, description: str = "", author: str = "",
                 version: str = "1.0.0", icon: str = "", min_version: str = "", sdk_version: str = ""):
        self.id = plugin_id
        self.name = name
        self.description = description
        self.author = author
        self.version = version
        self.icon = icon
        self.min_version = min_version
        self.sdk_version = sdk_version


class BasePlugin:
    """
    Main base class for all exteraGram / AyuGram plugins.
    """
    __slots__ = ("_plugin_id", "_settings", "_hooks", "logger", "_active_hooks")

    def __init__(self):
        self._plugin_id = getattr(self.__class__, "__id__", self.__class__.__name__)
        self._settings: Dict[str, Any] = {}
        self._hooks: List[Any] = []
        self._active_hooks: Dict[str, bool] = {
            "send_message": False,
            "receive_message": False,
        }
        self.logger = logging.getLogger(f"Plugin.{self._plugin_id}")

    def on_plugin_load(self):
        """Called when plugin is loaded/initialized."""
        pass

    def on_plugin_unload(self):
        """Called when plugin is unloaded or disabled."""
        pass

    def create_settings(self) -> List[Any]:
        """Returns a list of settings widgets from ui.settings."""
        return []

    def on_settings_changed(self, key: Optional[str] = None, value: Optional[Any] = None):
        """Called whenever a setting is updated by the user."""
        pass

    # --- Setting management ---
    def get_setting(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)

    def set_setting(self, key: str, value: Any):
        self._settings[key] = value
        self.on_settings_changed(key, value)

    def _init_settings(self, initial_dict: Dict[str, Any]):
        self._settings = dict(initial_dict)

    # --- High-level hooks ---
    def add_on_send_message_hook(self):
        self._active_hooks["send_message"] = True

    def on_send_message_hook(self, account: int, params: Any) -> HookResult:
        return HookResult()

    def add_on_message_hook(self):
        self._active_hooks["receive_message"] = True

    def on_message_hook(self, account: int, params: Any) -> HookResult:
        return HookResult()

    # --- Low-level / Reflection Hooks ---
    def hook_method(self, method_or_name: Any, hook: Union[MethodHook, Callable] = None, before: Optional[Callable] = None, after: Optional[Callable] = None, priority: int = 50) -> Any:
        if hook is None:
            hook = PyMethodHook(before=before, after=after)
        h = XposedHook(method_or_name, hook)
        self._hooks.append(h)
        return h

    def hook_all_methods(self, clazz: Any, method_name: str, hook: Any) -> Any:
        h = XposedHook(f"{clazz}.{method_name}", hook)
        self._hooks.append(h)
        return h

    def unhook_method(self, hook: Any):
        if hasattr(hook, "unhook"):
            hook.unhook()
        if hook in self._hooks:
            self._hooks.remove(hook)
