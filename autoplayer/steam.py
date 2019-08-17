"""Module contains asserts and GUI elements for steam configuration
"""

import subprocess
import time
import logging as log
from autoplayer.model.exceptions import SteamException, SteamLoginException
from autoplayer.config.system import process_steam
from autoplayer.util.system_utils import is_process_running
from autoplayer.config.system import steam_exe_path, coh2_appid, coh2_launch_params


def login(username, password):
    """Tries to login to Steam"""
    # TODO Make explicit check for launched and logged in Steam in steam module

    log.info("Logging into Steam...")
    from subprocess import check_output
    out = check_output([steam_exe_path, "-login", username, password])
    log.info(out)

    time.sleep(10 + 30)  # Waiting for possible Steam updates

    count = 0
    while count != 5:
        time.sleep(5)
        if is_process_running(process_steam):
            log.info("Login complete.")
            return

    raise SteamLoginException("Failed to launch Steam!")


def launch_coh2():
    """Tries to launch Company of Heroes 2"""

    time.sleep(4)
    log.info("Launching Company of Heroes from Steam...")
    subprocess.call(steam_exe_path + f" -applaunch {coh2_appid} {coh2_launch_params}")


def shutdown():
    """Gracefully shuts down Steam"""

    log.info("Closing Steam...")
    subprocess.call(steam_exe_path + f" -shutdown")
    time.sleep(10)  # Wait for Steam to close
