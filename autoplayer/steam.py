"""Module contains asserts and GUI elements for steam configuration
"""

import subprocess
import time
import logging as log
from autoplayer.coh2.model.exceptions import SteamLoginException
from autoplayer.util.system_utils import is_process_running

process_steam = "Steam.exe"
steam_exe_path = "C:\\Program Files (x86)\\Steam\\Steam.exe"


def login(username, password):
    """Tries to login to Steam"""

    log.info("Logging into Steam...")
    subprocess.Popen([steam_exe_path, "-login", username, password], stdout=None, stdin=None, stderr=None)

    time.sleep(10 + 20)  # Waiting for possible Steam updates

    count = 0
    while count != 12:
        count += 1
        time.sleep(5)
        if is_process_running(process_steam):
            log.info("Login complete.")
            return

    raise SteamLoginException("Failed to launch Steam!")


def launch_game(appid, launch_params):
    """Tries to launch specified game"""

    time.sleep(4)
    log.info(f"Launching game with AppID {appid} from Steam...")
    subprocess.call(steam_exe_path + f" -applaunch {appid} {launch_params}")


def shutdown():
    """Gracefully shuts down Steam"""

    log.info("Closing Steam...")
    subprocess.call(steam_exe_path + f" -shutdown")
    time.sleep(10)  # Wait for Steam to close
