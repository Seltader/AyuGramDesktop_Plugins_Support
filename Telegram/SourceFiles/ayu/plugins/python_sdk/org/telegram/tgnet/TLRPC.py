# -*- coding: utf-8 -*-
"""
TLRPC class definitions and entity structures for Telegram plugins.
"""

class _TL_Object:
    def __init__(self, **kwargs):
        self.flags = 0
        self.offset = 0
        self.length = 0
        self.__dict__.update(kwargs)

    def __repr__(self):
        fields = ", ".join(f"{k}={v}" for k, v in self.__dict__.items() if not k.startswith("_"))
        return f"<{self.__class__.__name__} {fields}>"


class TL_messageEntityBlockquote(_TL_Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collapsed = False

class TL_messageEntityBold(_TL_Object): pass
class TL_messageEntityItalic(_TL_Object): pass
class TL_messageEntityCode(_TL_Object): pass
class TL_messageEntityPre(_TL_Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = ""

class TL_messageEntityTextUrl(_TL_Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = ""

class TL_messageEntityMention(_TL_Object): pass
class TL_messageEntityHashtag(_TL_Object): pass
class TL_messageEntityBotCommand(_TL_Object): pass
class TL_messageEntityUrl(_TL_Object): pass
class TL_messageEntityEmail(_TL_Object): pass
class TL_messageEntityStrike(_TL_Object): pass
class TL_messageEntityUnderline(_TL_Object): pass
class TL_messageEntitySpoiler(_TL_Object): pass
class TL_messageEntityCustomEmoji(_TL_Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.document_id = 0


class _TLRPC_Meta(type):
    def __getattr__(cls, name: str):
        # Dynamically create any TL_* class if requested
        if name.startswith("TL_"):
            new_cls = type(name, (_TL_Object,), {})
            setattr(cls, name, new_cls)
            return new_cls
        raise AttributeError(f"TLRPC has no attribute {name}")


class TLRPC(metaclass=_TLRPC_Meta):
    # Explicitly bound common types
    TL_messageEntityBlockquote = TL_messageEntityBlockquote
    TL_messageEntityBold = TL_messageEntityBold
    TL_messageEntityItalic = TL_messageEntityItalic
    TL_messageEntityCode = TL_messageEntityCode
    TL_messageEntityPre = TL_messageEntityPre
    TL_messageEntityTextUrl = TL_messageEntityTextUrl
    TL_messageEntityStrike = TL_messageEntityStrike
    TL_messageEntityUnderline = TL_messageEntityUnderline
    TL_messageEntitySpoiler = TL_messageEntitySpoiler
    TL_messageEntityCustomEmoji = TL_messageEntityCustomEmoji
