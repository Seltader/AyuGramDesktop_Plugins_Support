# -*- coding: utf-8 -*-
from java import JavaClassProxy

R = JavaClassProxy("org.telegram.messenger.R")
ApplicationLoader = JavaClassProxy("org.telegram.messenger.ApplicationLoader")
AndroidUtilities = JavaClassProxy("org.telegram.messenger.AndroidUtilities")
MessagesController = JavaClassProxy("org.telegram.messenger.MessagesController")
FileLoader = JavaClassProxy("org.telegram.messenger.FileLoader")
LocaleController = JavaClassProxy("org.telegram.messenger.LocaleController")

__all__ = ["R", "ApplicationLoader", "AndroidUtilities", "MessagesController", "FileLoader", "LocaleController"]
