"""Contains functions that used to configure and click elements in-game
"""

import time
import pyautogui as pa
import logging as log
import autoplayer.coh2.paths as paths
import autoplayer.coh2.coordinates as coord
import autoplayer.window as wgui
from autoplayer.util.system_utils import is_process_running
from autoplayer.coh2.main import process_coh2, window_name_coh2
from autoplayer.coh2.model.playmode.abstract_playmode import AbstractPlaymode
from autoplayer.coh2.model.faction.abstract_faction import AbstractFaction
from autoplayer.coh2.model.exceptions import GuiElementNotFound, PointsLimitReached, \
    ApplicationFailedToOpen, ApplicationFailedToStart
from autoplayer.util.autogui_utils import wait_for_element


def wait_coh2_readiness():
    """Waits certain time and focuses on Company of Heroes 2 window"""
    
    log.info("Waiting for game to load...")
    launched = False

    for i in range(5):  # Waiting 5 minutes for small updates
        log.info(f"Waiting {i} minute(s) for game to be ready")
        time.sleep(60)
        if is_process_running(process_coh2):
            launched = True
            break

    if not launched:
        raise ApplicationFailedToStart(window_name_coh2)

    time.sleep(55)  # Waiting additional time, just in case game was launched recently
    focus_on_game()
    open_network_and_battle()


def open_network_and_battle():
    """Opens 'network_and_battle' menu"""
    
    pa.click(x=10, y=10)  # Closing any "adds" or "tutorials"
    time.sleep(2)
    network_and_battle_coord = wait_for_element(paths.network_and_battle, 5, 10)
    if network_and_battle_coord:
        log.info("Hitting 'network_and_battle_coord' button...")
        pa.click(network_and_battle_coord)
    else:
        log.error("Could not open match setup screen!")
        raise GuiElementNotFound("'network_and_battle' in-game button")


def is_main_menu():
    """Returns True if current page has 'network_and_battle' button"""
    
    if pa.locateOnScreen(paths.network_and_battle, confidence=0.7) is not None:
        return True
    else:
        return False


def focus_on_game():
    """Focuses on game window"""

    window = wgui.find_window(window_name_coh2)
    if window is 0 or None:
        log.error(f"{window_name_coh2} was not found!")
        raise ApplicationFailedToOpen(window_name_coh2)

    wgui.set_foreground(window)
    time.sleep(4)
    wgui.set_maximized(window)
    time.sleep(10)
    wgui.is_windowed(window)


def configure_match():
    """Sets bot and creates customer game from in-game menu"""

    log.info("Configuring match...")
    time.sleep(5)
    pa.click(x=50, y=50)
    time.sleep(3)
    log.info("Hitting 'create_custom_game' button...")

    create_custom_game_coord = pa.locateCenterOnScreen(paths.create_custom_game, confidence=0.65)
    if create_custom_game_coord:
        pa.click(create_custom_game_coord)
    else:
        log.warning("Failed to find 'create_custom_game'!")

        raise GuiElementNotFound("'create_custom_game' in-game button")

    time.sleep(13)
    pa.click(x=50, y=50)
    time.sleep(2)
    log.info("Hitting 'add_ai' button...")
    pa.click(pa.locateCenterOnScreen(paths.add_ai, confidence=0.7))
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
    """Selects specified faction using Faction coordinates"""
    
    pa.click(coord.match_current_faction)
    time.sleep(2)
    pa.click(faction.get_match_select_coordinates())


def play_match(i: int, playmode: AbstractPlaymode, consider_points_limit: bool):
    """Runs match, checks points limit"""

    log.info("=====================")
    log.info(f"Playing game #{i}")

    if pa.locateOnScreen(paths.no_points, confidence=0.7) is not None and consider_points_limit:
        log.warning("Points limit reached. Stopping game...")
        raise PointsLimitReached

    start_match_time = time.time()
    pa.moveTo([x / 2 for x in pa.size()])
    try:
        pa.click()  # Reset mouse position
        log.info("Locating 'Start match button'...")
        start_button_position = pa.locateCenterOnScreen(paths.start_game, confidence=0.7)
        pa.click(start_button_position)

        # Clicking second time, as sometimes, one click is not enough
        time.sleep(3)
        pa.click(start_button_position)
    except TypeError:
        log.warning("Button is not visible. Hitting blindly...")
        pa.click(coord.start_button)

    if not wait_for_element(paths.press_anykey, 20, 5):
        log.warning("'press_anykey' in-game button was not found. Windowed mode?")

        if pa.locateCenterOnScreen(paths.press_anykey_cut, confidence=0.7) is not None:
            log.info("Found 'press_anykey_cut'. Game is in windowed mode.")
        elif pa.locateCenterOnScreen(paths.langresskaya_map_loadin_screen, confidence=0.7) is not None:
            log.info("Found 'langresskaya_map_loadin_screen'. Game is in windowed mode.")
        elif pa.locateCenterOnScreen(paths.map_name_match_start, confidence=0.7) is not None:
            log.info("Found 'map_name_match_start'. Game is in windowed mode.")
        else:
            raise GuiElementNotFound("'press_anykey' in-game button")

    log.info("Starting match...")
    pa.press("escape")
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
