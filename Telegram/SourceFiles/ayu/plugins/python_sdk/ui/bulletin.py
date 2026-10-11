# -*- coding: utf-8 -*-
import logging
from typing import Any, Callable, Optional

logger = logging.getLogger("ui.bulletin")

# Desktop Bridge callback (set by C++ plugin manager or Python host)
_on_show_bulletin: Optional[Callable[[str, str, Optional[str], Optional[Callable]], None]] = None

def set_bulletin_handler(handler: Callable):
    global _on_show_bulletin
    _on_show_bulletin = handler

class BulletinHelper:
    @staticmethod
    def show(message: str, icon: Any = None):
        logger.info(f"[Bulletin] {message}")
        if _on_show_bulletin:
            _on_show_bulletin("info", str(message), None, None)

    @staticmethod
    def show_info(message: str):
        BulletinHelper.show(message)

    @staticmethod
    def show_error(message: str, exc: Any = None):
        text = str(message)
        if exc:
            text += f": {exc}"
        logger.error(f"[Bulletin Error] {text}")
        if _on_show_bulletin:
            _on_show_bulletin("error", text, None, None)

    @staticmethod
    def show_with_button(message: str, icon: Any = None, button_text: str = "OK", on_click: Optional[Callable] = None):
        logger.info(f"[Bulletin Button] {message} [{button_text}]")
        if _on_show_bulletin:
            _on_show_bulletin("info", str(message), button_text, on_click)
        elif on_click:
            # Fallback in non-gui test environment
            pass
