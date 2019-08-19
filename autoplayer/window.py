"""Contains some calls to the winapi for window management
"""

import win32gui
import logging as log


def find_window(class_name=None, window_name=None):
    """Find a window by its class_name"""

    log.info(f"Finding '{window_name}' window")
    return win32gui.FindWindow(class_name, window_name)


def set_foreground(handle):
    """Put the window in the foreground"""

    log.info(f"Settings {handle} to foreground")
    win32gui.SetForegroundWindow(handle)
