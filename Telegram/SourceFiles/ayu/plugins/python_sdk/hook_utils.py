# -*- coding: utf-8 -*-
"""
hook_utils module for exteraGram/AyuGram plugins.
Provides reflection helpers and class finding.
"""

from typing import Any, Optional
from java import jclass

def find_class(class_name: str) -> Any:
    """Finds or resolves a class by its fully qualified name."""
    try:
        return jclass(class_name)
    except Exception:
        return None

def get_private_field(obj: Any, field_name: str) -> Any:
    """Retrieves field value by name."""
    if obj is None:
        return None
    return getattr(obj, field_name, None)

def set_private_field(obj: Any, field_name: str, value: Any):
    """Sets field value by name."""
    if obj is not None:
        setattr(obj, field_name, value)

def get_private_method(obj: Any, method_name: str) -> Any:
    if obj is None:
        return None
    return getattr(obj, method_name, None)
