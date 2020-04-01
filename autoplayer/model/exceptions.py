""" Module contains custom exception used in the code
"""

import pyautogui
import time
from autoplayer.config import settings


class Error(Exception):
    """Base class for other exceptions"""
    pass


class SteamLoginException(Error):
    """Raised when code failed to login to Steam account"""
    pass


class GuiElementNotFound(Error):
    """Raised when element wasn't found by respective screenshot"""

    def __init__(self, element):
        self.element = element
        pyautogui.screenshot(settings.get_temp_dir() + "gui_element_notfound_" + str(time.time()) + ".png")


class PointsLimitReached(Error):
    """Raised if points limit was reached"""
    pass


class ApplicationFailedToStart(Error):
    """Raised when check for running application failed"""

    def __init__(self, application):
        self.application = application


class ApplicationFailedToOpen(Error):
    """Raised when focus on app has failed"""

    def __init__(self, application):
        self.application = application
