# -*- coding: utf-8 -*-
"""
Emulation of java.util classes in Python.
"""

class ArrayList(list):
    """Python emulation of java.util.ArrayList."""
    def size(self) -> int:
        return len(self)

    def get(self, index: int):
        return self[index]

    def add(self, *args):
        if len(args) == 1:
            self.append(args[0])
        elif len(args) == 2:
            self.insert(args[0], args[1])

    def remove(self, item_or_index):
        if isinstance(item_or_index, int):
            return self.pop(item_or_index)
        else:
            return super().remove(item_or_index)

    def isEmpty(self) -> bool:
        return len(self) == 0

    def clear(self):
        super().clear()


class HashMap(dict):
    """Python emulation of java.util.HashMap."""
    def put(self, key, value):
        self[key] = value

    def get(self, key):
        return super().get(key, None)

    def size(self) -> int:
        return len(self)

    def containsKey(self, key) -> bool:
        return key in self
