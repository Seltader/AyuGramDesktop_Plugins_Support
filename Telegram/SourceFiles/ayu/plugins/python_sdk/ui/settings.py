# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union

@dataclass
class Header:
    text: str
    icon: Optional[str] = None
    subtext: Optional[str] = None

@dataclass
class Switch:
    key: str
    text: str
    default: bool = False
    subtext: Optional[str] = None
    icon: Optional[str] = None

@dataclass
class Input:
    key: str
    text: str
    default: str = ""
    subtext: Optional[str] = None
    icon: Optional[str] = None
    input_type: Optional[str] = None

@dataclass
class Text:
    text: str
    subtext: Optional[str] = None
    icon: Optional[str] = None
    on_click: Optional[Callable] = None

@dataclass
class Select:
    key: str
    text: str
    options: List[str] = field(default_factory=list)
    default: str = ""
    subtext: Optional[str] = None
    icon: Optional[str] = None

@dataclass
class Radio:
    key: str
    text: str
    options: List[str] = field(default_factory=list)
    default: str = ""
    subtext: Optional[str] = None
    icon: Optional[str] = None

@dataclass
class CustomSetting:
    key: Optional[str] = None
    view: Any = None
