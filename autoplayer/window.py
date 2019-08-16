"""Contains some calls to the winapi for window management
"""

import win32gui
import re


def find_window(self, class_name, window_name=None):
    """Find a window by its class_name"""

    self._handle = win32gui.FindWindow(class_name, window_name)


def _window_enum_callback(self, hwnd, wildcard):
    """Pass to win32gui.EnumWindows() to check all the opened windows"""

    if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
        self._handle = hwnd


def find_window_wildcard(self, wildcard):
    """Find a window whose title matches the wildcard regex"""

    self._handle = None
    win32gui.EnumWindows(self._window_enum_callback, wildcard)


def set_foreground(self):
    """Put the window in the foreground"""

    win32gui.SetForegroundWindow(self._handle)
