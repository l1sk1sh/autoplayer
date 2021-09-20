"""Contains some calls to the winapi for window management
"""
from ctypes import windll

import win32con
import win32gui, win32com.client
import logging as log

user32 = windll.user32
full_screen_rect = (0, 0, user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))


def find_window(window_name):
    """Find a window by its class_name"""

    log.info(f"Finding '{window_name}' window...")
    return win32gui.FindWindow(None, window_name)


def set_foreground(window):
    """Put the window in the foreground"""

    log.info(f"Setting {window} to foreground...")
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(window)


def set_maximized(window):
    """Make specific window maximized"""

    log.info(f"Setting {window} maximized...")
    win32gui.ShowWindow(window, win32con.SW_MAXIMIZE)


def is_windowed(window):
    """Verifies if window is fullscreen"""

    fullscreen = False
    try:
        rect = win32gui.GetWindowRect(window)
        fullscreen = (full_screen_rect == rect)
        log.info(f"Actual resolution {rect} vs screen resolution {full_screen_rect}")
    except Exception as e:
        log.warning(f"Failed to determine if window is in fullscreen {e}")

    log.info(f"Window {window} is fullscreen: {fullscreen}")

    return fullscreen
