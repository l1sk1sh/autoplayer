"""Module contains methods to assert game before start
"""

import platform
import psutil
import time
import sys
import pyautogui as pa
import logging as log
import ctypes
from autoplayer.util.system_utils import is_process_running
from autoplayer.steam import process_steam
from autoplayer.coh2.main import process_coh2, process_ce
from autoplayer.coh2.model.faction.abstract_faction import AbstractFaction as af
from autoplayer.coh2.model.map.abstract_map import AbstractMap as am
from autoplayer.coh2.model.playmode.abstract_playmode import AbstractPlaymode as ap

screen_resolution = (1366, 768)


class Asserter:
    """Contains all asserts required to launch scripts"""

    def __init__(self, faction: af, playmode: ap, map_game: am):
        self.faction = faction
        self.playmode = playmode
        self.map_game = map_game
        self.is_coh_running = True
        self.is_steam_running = True
        self.is_correct_faction = True

    def assert_preload(self):
        """Asserts before launch of the application"""

        if platform.system() != "Windows":
            log.error("Current script is designed for Windows only.")
            sys.exit(1)

        local_processes = [p.name() for p in psutil.process_iter()]

        if not is_process_running(process_steam, local_processes):
            log.warning("Steam is not launched! Will try to handle it!")
            self.is_steam_running = False
            self.is_coh_running = False
        elif not is_process_running(process_coh2, local_processes):
            log.warning("Company of Heroes 2 is not launched! Will try to launch it with Steam!")
            self.is_coh_running = False
        else:
            log.info("Company of Heroes 2 is launched!")

        if not is_process_running(process_ce, local_processes) \
                and self.playmode.get_playmode_name() == ap.real_playmode:
            log.error("Cheat engine is required for 'real' game!")
            sys.exit(1)

        log.warning("Make sure that 'English - United States' keyboard is selected!")

        # Currently not used as bugged (shows failure when correct keyboard is selected)
        # Getting current keyboard layout
        # user32 = ctypes.WinDLL('user32', use_last_error=True)  # For debug Windows error codes in the current thread
        # curr_window = user32.GetForegroundWindow()
        # thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
        # klid = user32.GetKeyboardLayout(thread_id)  # Made up 0xAAABBBB, AAA = HKL (handle obj) & BBBB = language ID
        # lid = klid & (2 ** 16 - 1)  # lid = klid & (2 ** 16 - 1) # Extract language ID from KLID
        # lid_hex = hex(lid)  # Convert language ID from decimal to hexadecimal
        # if lid_hex != '0x409':
        #     log.error("Keyboard layout must be 'English - United States'!")
        #     sys.exit(1)

        if self.playmode.get_playmode_name() == ap.real_playmode:
            log.warning("Make sure that Cheat Engine is configured!")
            time.sleep(5)

    def assert_game_setup(self):
        """Asserts match configuration"""

        log.info("Checking match setup...")
        if pa.size() != screen_resolution:
            log.error(f"Screen size is not {screen_resolution} it is {pa.size()}!")
            sys.exit(1)

        log.info("Checking faction...")
        if self.faction.get_faction_name() in \
                (af.okw_name, af.usa_name, af.wehrmacht_name, af.british_name, af.ussr_name):
            if pa.locateOnScreen(self.faction.get_faction_symbol_path(), confidence=0.7) is None:
                log.warning(f"Selected faction is not {self.faction.get_faction_name()}!")
                self.is_correct_faction = False
        else:
            log.error(f"Unknown selected faction!")
            sys.exit(1)

        log.info("Checking map...")
        if self.map_game.get_map_name() == am.langresskaya_name:
            if pa.locateOnScreen(self.map_game.get_config_name_path(), confidence=0.7) is None:
                log.error("Selected map is not 'Лангресская'!")
                sys.exit(1)
        else:
            log.error(f"Unknown map!")
            sys.exit(1)

        log.info("Checking match configuration...")
        if self.playmode.get_playmode_name() == ap.real_playmode:
            if pa.locateOnScreen(self.playmode.get_match_config_path(), confidence=0.7) is None:
                log.error("'Real' match configuration must include:"
                          "\n\t- No modifications"
                          "\n\t- Standard resources"
                          "\n\t- Specified positions"
                          "\n\t- Annihilation")
                sys.exit(1)
        elif self.playmode.get_playmode_name() == ap.modded_gamemode:
            if pa.locateOnScreen(self.playmode.get_match_config_path(), confidence=0.7) is None:
                log.error("'Mode' configuration must include:"
                          "\n\t- Standard resources"
                          "\n\t- Specified positions"
                          "\n\t- CheatCommands Mod II (Annih.)")
                sys.exit(1)
        else:
            log.error(f"Unknown play mode selected!")
            sys.exit(1)

        log.info("Checking AI difficulty...")
        if self.playmode.get_playmode_name() == ap.real_playmode:
            if pa.locateOnScreen(self.playmode.easy_bot_path, confidence=0.7) is None:
                log.error("'Real' game takes too long with hard bot!")
                sys.exit(1)
        elif self.playmode.get_playmode_name() == ap.modded_gamemode:
            if pa.locateOnScreen(self.playmode.expert_bot_path, confidence=0.7) is None:
                log.warning("'Modded' game is better against expert bot!")
        else:
            log.error(f"Unknown difficulty!")
            sys.exit(1)
