"""Contains some calls to the winapi for window management
"""

import win32gui, win32com.client
import logging as log


def find_window(window_name):
    """Find a window by its class_name"""

    log.info(f"Finding '{window_name}' window")
    return win32gui.FindWindow(None, window_name)


def set_foreground(handle):
    """Put the window in the foreground"""

    log.info(f"Settings {handle} to foreground")
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(handle)
