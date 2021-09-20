"""Contains functions that used to configure and click elements in-game
"""

import time
import pyautogui as pa
import logging as log
import autoplayer.window as wgui
import autoplayer.dst.coordinates as coord
from autoplayer.dst.paths import account_badge
from autoplayer.util.system_utils import is_process_running
from autoplayer.dst.main import process_dst, window_name_dst
from autoplayer.dst.model.exceptions import ApplicationFailedToStart, ApplicationFailedToOpen, MenuIsNotReached


def wait_dst_readiness():
    """Waits certain time and focuses on DST window"""

    log.info("Waiting for game to load...")
    launched = False

    for i in range(5):  # Waiting 5 minutes for small updates
        log.info(f"Waiting {i} minute(s) for game to be ready")
        time.sleep(60)
        if is_process_running(process_dst):
            launched = True
            break

    if not launched:
        raise ApplicationFailedToStart(window_name_dst)

    time.sleep(55)  # Waiting additional time, just in case game was launched recently
    focus_on_game()


def focus_on_game():
    """Focuses on game window"""

    window = wgui.find_window(window_name_dst)
    if window is 0 or None:
        log.error(f"{window_name_dst} was not found!")
        raise ApplicationFailedToOpen(window_name_dst)

    wgui.set_foreground(window)
    time.sleep(10)


def take_present():
    """Takes daily present by simply clicking and waiting"""

    log.info("Hitting blindly 'I understand' for mods message...")
    pa.click(coord.warning_mods_understand_button)
    pa.click(coord.warning_mods_understand_button)
    time.sleep(3)

    log.info("Hitting blindly 'Play' button...")
    pa.click(coord.play_button)
    pa.click(coord.play_button)
    time.sleep(10)

    log.info("Hitting empty space to get loot boxes...")
    for i in range(3):
        pa.click(coord.blank_place)
        pa.click(coord.blank_place)
        time.sleep(5)
        pa.click(coord.blank_place)

    if not menu_visible():
        raise MenuIsNotReached()


def menu_visible():
    """Returns True if current page has account badge visible that means - main menu is accessible"""

    if pa.locateOnScreen(account_badge, confidence=0.7) is not None:
        return True
    else:
        return False
