# -*- coding: utf-8 -*-
from java import JavaClassProxy

DialogCell = JavaClassProxy("org.telegram.ui.Cells.DialogCell")
ProfileSearchCell = JavaClassProxy("org.telegram.ui.Cells.ProfileSearchCell")
ChatMessageCell = JavaClassProxy("org.telegram.ui.Cells.ChatMessageCell")

__all__ = ["DialogCell", "ProfileSearchCell", "ChatMessageCell"]
