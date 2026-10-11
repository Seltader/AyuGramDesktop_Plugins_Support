# -*- coding: utf-8 -*-
from typing import Any, Callable, Dict, List, Optional

class AlertDialogBuilder:
    def __init__(self, context=None):
        self._title = ""
        self._message = ""
        self._positive_text = "OK"
        self._positive_callback = None
        self._negative_text = "Cancel"
        self._negative_callback = None

    def setTitle(self, title: str):
        self._title = str(title)
        return self

    def setMessage(self, message: str):
        self._message = str(message)
        return self

    def setPositiveButton(self, text: str, listener: Optional[Callable] = None):
        self._positive_text = str(text)
        self._positive_callback = listener
        return self

    def setNegativeButton(self, text: str, listener: Optional[Callable] = None):
        self._negative_text = str(text)
        self._negative_callback = listener
        return self

    def show(self):
        # Trigger desktop message box
        return self

    def create(self):
        return self
