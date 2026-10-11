# -*- coding: utf-8 -*-
"""
Chaquopy Java Interop Emulation Layer for Desktop.
Allows plugins using `from java import jclass` to work seamlessly.
"""

from typing import Any, Dict

_class_cache: Dict[str, Any] = {}

class JavaFieldProxy:
    def __init__(self, name: str):
        self.name = name

    def setAccessible(self, accessible: bool):
        pass

    def get(self, obj: Any) -> Any:
        return getattr(obj, self.name, None)

    def set(self, obj: Any, value: Any):
        setattr(obj, self.name, value)

    def setBoolean(self, obj: Any, value: bool):
        setattr(obj, self.name, bool(value))

    def getBoolean(self, obj: Any) -> bool:
        return bool(getattr(obj, self.name, False))


class JavaMethodProxy:
    def __init__(self, name: str):
        self.name = name

    def getName(self) -> str:
        return self.name

    def setAccessible(self, accessible: bool):
        pass

    def __call__(self, *args, **kwargs):
        return None


class ChaquopyReflector:
    def __init__(self, clazz):
        self.clazz = clazz

    def getMethods(self, name: str = None):
        if name:
            return [JavaMethodProxy(name)]
        return [JavaMethodProxy("defaultMethod")]


class JavaObjectProxy:
    def __init__(self, class_name: str, **kwargs):
        self._class_name = class_name
        self.__dict__.update(kwargs)

    def getClass(self):
        return jclass(self._class_name)

    def getId(self):
        return getattr(self, "id", None)

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        # Return a mock callable or nested object
        return JavaObjectProxy(f"{self._class_name}.{name}")

    def __call__(self, *args, **kwargs):
        return None

    def __repr__(self):
        return f"<JavaObject {self._class_name}>"


class JavaClassProxy:
    def __init__(self, full_name: str):
        self.__name__ = full_name
        self._chaquopy_reflector = ChaquopyReflector(self)

    def forName(self, name: str):
        return jclass(name)

    def getDeclaredField(self, field_name: str):
        return JavaFieldProxy(field_name)

    def getDeclaredMethods(self):
        return [
            JavaMethodProxy("setDialog"),
            JavaMethodProxy("checkBotOpenButton"),
            JavaMethodProxy("setData"),
            JavaMethodProxy("setOpenButton"),
            JavaMethodProxy("fillItems"),
            JavaMethodProxy("getName"),
        ]

    def getSuperclass(self):
        return JavaClassProxy("java.lang.Object")

    def __call__(self, *args, **kwargs):
        # Create an instance of this mock class
        return JavaObjectProxy(self.__name__, **kwargs)

    def __getattr__(self, name):
        # Handle static fields/subclasses
        return JavaObjectProxy(f"{self.__name__}.{name}")

    def __repr__(self):
        return f"<JavaClass {self.__name__}>"


def jclass(class_name: str) -> Any:
    """Emulates Chaquopy's jclass(...)"""
    # Special handling for known classes
    if class_name == "java.lang.Class":
        return JavaClassProxy("java.lang.Class")
    if class_name == "java.util.ArrayList":
        from java.util import ArrayList
        return ArrayList
    if class_name == "org.telegram.tgnet.TLRPC":
        from org.telegram.tgnet import TLRPC
        return TLRPC

    if class_name not in _class_cache:
        _class_cache[class_name] = JavaClassProxy(class_name)
    return _class_cache[class_name]

def jarray(element_type):
    return list
