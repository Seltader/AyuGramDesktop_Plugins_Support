# -*- coding: utf-8 -*-
import os
import tempfile

def get_plugins_dir() -> str:
    app_data = os.environ.get("APPDATA", "")
    if app_data:
        p = os.path.join(app_data, "AyuGram", "plugins")
    else:
        p = os.path.expanduser("~/.local/share/AyuGram/plugins")
    os.makedirs(p, exist_ok=True)
    return p

def get_cache_dir() -> str:
    p = os.path.join(tempfile.gettempdir(), "AyuGramCache")
    os.makedirs(p, exist_ok=True)
    return p

def get_files_dir() -> str:
    return get_plugins_dir()
