"""Module contains methods to assert game before start
"""

import platform
import psutil
import sys
import pyautogui as pa
import logging as log
from autoplayer.util.system_utils import is_process_running
from autoplayer.steam import process_steam
from autoplayer.dst.main import process_dst

screen_resolution = (1366, 768)


class Asserter:
    """Contains all asserts required to launch scripts"""

    def __init__(self):
        self.is_dst_running = True
        self.is_steam_running = True

    def assert_preload(self):
        """Asserts before launch of the application"""

        if platform.system() != "Windows":
            log.error("Current script is designed for Windows only.")
            sys.exit(1)

        local_processes = [p.name() for p in psutil.process_iter()]

        if not is_process_running(process_steam, local_processes):
            log.warning("Steam is not launched! Will try to handle it!")
            self.is_steam_running = False
            self.is_dst_running = False
        elif not is_process_running(process_dst, local_processes):
            log.warning("Don't Starve Together is not launched! Will try to launch it with Steam!")
            self.is_dst_running = False
        else:
            log.info("Don't Starve Together is launched!")

    @staticmethod
    def assert_game_setup():
        """Asserts match configuration"""

        log.info("Checking match setup...")
        if pa.size() != screen_resolution:
            log.error(f"Screen size is not {screen_resolution} it is {pa.size()}!")
            sys.exit(1)

        log.warning("Make sure that game is launched if full screen (configured manually through settings). "
                    "Otherwise, it may not work.")
