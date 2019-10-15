""" Module contains custom exception used in the code
"""

import pyautogui
import time
from autoplayer.config.settings import temp_dir


class Error(Exception):
    """Base class for other exceptions"""
    pass


class SteamLoginException(Error):
    """Raised when code failed to login to Steam account"""
    pass


class CredentialsNotSet(Error):
    """Raised when credentials for Steam account are not defined"""
    pass


class GuiElementNotFound(Error):
    """Raised when element wasn't found by respective screenshot"""

    def __init__(self, element):
        self.element = element
        pyautogui.screenshot(temp_dir + "gui_element_notfound_" + str(time.time()) + ".png")


class PointsLimitReached(Error):
    """Raised if points limit was reached"""
    pass


class ApplicationFailedToStart(Error):
    """Raised when check for running application failed"""

    def __init__(self, application):
        self.application = application
