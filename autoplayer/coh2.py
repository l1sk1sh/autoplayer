"""Contains functions that used to configure and click elements in-game
"""

import time
import pyautogui as pa
import logging as log
import autoplayer.config.paths as paths
import autoplayer.config.coordinates as coord
import autoplayer.window as wgui
from autoplayer.model.exceptions import ApplicationFailedToStart
from autoplayer.config.system import window_name_coh2
from autoplayer.model.playmode.abstract_playmode import AbstractPlaymode
from autoplayer.model.faction.abstract_faction import AbstractFaction
from autoplayer.model.exceptions import GuiElementNotFound, PointsLimitReached
from autoplayer.util.autogui_utils import wait_for_element


def wait_coh2_readiness():
    log.info("Waiting for game to load...")
    time.sleep(55)
    focus_on_game()
    open_network_and_battle()


def open_network_and_battle():
    pa.click(x=10, y=10);  # Closing any "adds" or "tutorials"
    time.sleep(2)
    network_and_battle_coord = wait_for_element(paths.network_and_battle, 5, 10)
    if network_and_battle_coord:
        pa.click(network_and_battle_coord)
    else:
        log.error("Could not open match setup screen!")
        raise GuiElementNotFound("'network_and_battle' in-game button")


def is_main_menu():
    if pa.locateOnScreen(paths.network_and_battle, confidence=0.8) is not None:
        return True
    else:
        return False


def focus_on_game():
    """Focuses on game window"""

    window = wgui.find_window(window_name_coh2)
    if window is 0 or None:
        log.error(f"{window_name_coh2} was not found!")
        raise ApplicationFailedToStart(window_name_coh2)

    wgui.set_foreground(window)
    time.sleep(10)


def configure_match():
    """Sets bot and creates customer game from in-game menu"""

    log.info("Configuring match...")
    pa.click(x=50, y=50);  # Closing any "adds" or "tutorials"
    log.info("Closed tutorials.")
    time.sleep(3)
    log.info("Hitting 'create customer game' button...")
    print(pa.locateCenterOnScreen(paths.create_custom_game, confidence=0.8))
    pa.click(pa.locateCenterOnScreen(paths.create_custom_game, confidence=0.8))
    time.sleep(13)
    pa.click(x=50, y=50);  # Closing any "adds" or "tutorials"
    log.info("Closed tutorials.")
    time.sleep(2)
    pa.click(pa.locateCenterOnScreen(paths.add_ai, confidence=0.8))
    # pa.click(coord.add_ai_button)


def close_game():
    """Closes game through in-game interface"""

    log.info("Closing game through in-game interface...")
    pa.click(coord.ingame_menu)
    time.sleep(3)
    pa.click(coord.ingame_menu_exit)
    time.sleep(3)
    pa.click(coord.ingame_menu_exit_confirm)

    time.sleep(10 + 15)  # Wait for game to close


def select_faction(faction: AbstractFaction):
    pa.click(coord.match_current_faction)
    time.sleep(2)
    pa.click(faction.get_match_select_coordinates())


def play_match(i: int, playmode: AbstractPlaymode, consider_points_limit: bool):
    """Runs match, checks points limit"""

    log.info("=====================")
    log.info(f"Playing game #{i}")

    if pa.locateOnScreen(paths.no_points, confidence=0.8) is not None and consider_points_limit:
        log.warning("Points limit reached. Stopping game...")
        raise PointsLimitReached

    start_match_time = time.time()
    pa.moveTo([x / 2 for x in pa.size()])
    try:
        pa.click()  # Reset mouse position
        log.info("Locating 'Start match button'...")
        pa.click(pa.locateCenterOnScreen(paths.start_game, confidence=0.8))
    except TypeError:
        log.warning("Button is not visible. Hitting blindly...")
        pa.click(coord.start_button)

    if wait_for_element(paths.press_anykey, 20, 8):
        log.info("Starting match...")
        pa.press("escape")
    else:
        log.error("Could not start match!")
        raise GuiElementNotFound("'press_anykey' in-game button")
    time.sleep(10)  # Sleep for n seconds to skip dimming screen
    log.info(f"Match load #{i} took {time.time() - start_match_time}s.")

    play_time = time.time()
    playmode.play()
    time.sleep(28)  # Usually 15s to load winning screen + 10 for boxes
    log.info("Closing winning screen...")
    for c in range(4):  # Close lootboxes
        pa.click(coord.winning_screen_exit)  # Hit exit button
        time.sleep(3)

    log.info("Match ended!")
    log.info(f"The game #{i} took {time.time() - play_time}s.")

    summary_exit_coord = wait_for_element(paths.summary_close, 20, 4)
    if summary_exit_coord:
        pa.click(summary_exit_coord)  # Click summary exit button
    else:
        log.error("Could not hit summary exit button!")
        raise GuiElementNotFound("'summary_exit' in-game button")

    time.sleep(8)  # Waiting for preparation screen to load
