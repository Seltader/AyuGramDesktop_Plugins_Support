# -*- coding: utf-8 -*-
import logging
import threading
from typing import Any, Callable, Optional

logger = logging.getLogger("android_utils")

_clipboard_text = ""
_on_clipboard_copy: Optional[Callable[[str], None]] = None

def set_clipboard_handler(handler: Callable[[str], None]):
    global _on_clipboard_copy
    _on_clipboard_copy = handler

def copy_to_clipboard(text: str):
    """Copies text to desktop clipboard."""
    global _clipboard_text
    _clipboard_text = str(text)
    logger.info(f"[Clipboard] Copied: {_clipboard_text[:50]}...")
    if _on_clipboard_copy:
        _on_clipboard_copy(_clipboard_text)

def get_from_clipboard() -> str:
    return _clipboard_text

def run_on_ui_thread(func: Callable, delay: int = 0):
    """Executes a function on the main UI thread."""
    if delay > 0:
        timer = threading.Timer(delay / 1000.0, func)
        timer.daemon = True
        timer.start()
    else:
        try:
            func()
        except Exception as e:
            logger.error(f"Error in run_on_ui_thread: {e}", exc_info=True)

def toast(text: str, duration: int = 0):
    from ui.bulletin import BulletinHelper
    BulletinHelper.show(text)

def get_last_fragment():
    """Mock Android fragment."""
    return None
