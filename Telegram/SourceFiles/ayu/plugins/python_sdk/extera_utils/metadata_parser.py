# -*- coding: utf-8 -*-
import ast
import os
from typing import Any, Dict

def get_metadata(file_path: str) -> Dict[str, Any]:
    """Statically parses plugin metadata constants (__id__, __name__, etc.) using AST."""
    metadata = {}
    allowed_keys = {
        "__id__", "__name__", "__description__", "__author__",
        "__version__", "__min_version__", "__app_version__",
        "__sdk_version__", "__icon__", "__requirements__"
    }
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            tree = ast.parse(f.read(), filename=file_path)
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in allowed_keys:
                        # Extract literal value
                        try:
                            val = ast.literal_eval(node.value)
                            metadata[target.id] = val
                        except Exception:
                            pass
    except Exception as e:
        metadata["__error__"] = str(e)
    return metadata
