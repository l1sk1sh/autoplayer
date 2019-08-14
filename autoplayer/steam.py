"""Module contains asserts and GUI elements for steam configuration
"""

import subprocess
import pyautogui as pa
import time
import autoplayer.config.paths as paths
from autoplayer.config.system import process_steam
from autoplayer.util.system_utils import is_process_running
from autoplayer.config.system import steam_exe_path, coh2_appid, coh2_launch_params


def play_coh2():
    """Tries to launch Company of Heroes 2"""

    subprocess.call(steam_exe_path + f" -applaunch {coh2_appid} {coh2_launch_params}")

    # TODO Check if login is successful

    # GUI Launch of CoH2
    # close_news()
    # open_library()
    # select_coh2()
    #
    # pa.click(pa.locateCenterOnScreen(paths.steam_play_button))


def login(username, password):
    """Tries to login to Steam"""

    subprocess.Popen([steam_exe_path, "-login", username, password], stdout=None, stdin=None, stderr=None)

    count = 0
    while count != 5:
        time.sleep(5)
        if is_process_running(process_steam):
            return

    raise Exception("Failed to launch Steam!")
    # TODO Check if login is successful

    # GUI Login variant
    # login_window = pa.locateOnScreen(paths.steam_login_title)
    # if login_window:
    #     pa.click(login_window)
    # else:
    #     raise Exception("login_steam() wasn't able to find Steam Login screen")
    #
    # pa.typewrite(password)
    # pa.press("enter")


def shutdown():
    """Shuts down Steam"""

    subprocess.call(steam_exe_path + f" -shutdown")


def open_library():
    """GUI check if library opened, and if not - opens it"""

    unselected_library = pa.locateOnScreen(paths.steam_library_coh2_unselected)
    if pa.locateOnScreen(paths.steam_library_selected):
        pass
    elif unselected_library:
        pa.click(unselected_library)
    else:
        raise Exception("open_library() unable to find 'Library' button")


def select_coh2():
    """GUI check if coh selected, and if not - selects it"""

    selected_coh2 = pa.locateOnScreen(paths.steam_library_coh2_selected)
    unselected_coh2 = pa.locateOnScreen(paths.steam_library_coh2_unselected)
    if selected_coh2:
        pa.click(selected_coh2)
    elif unselected_coh2:
        pa.click(unselected_coh2)
    else:
        raise Exception("select_coh2() unable to find 'coh2' button")


def close_news():
    if pa.locateOnScreen(paths.steam_news_title):
        pa.click(pa.locateOnScreen(paths.steam_news_title_close))
