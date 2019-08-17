import pyautogui as pa
import time
import logging as log
from autoplayer.model.playmode.abstract_playmode import AbstractPlaymode
from autoplayer.model.map.abstract_map import AbstractMap
from autoplayer.model.faction.abstract_faction import AbstractFaction
from autoplayer.config.paths import match_config_modded
from autoplayer.config.coordinates import mod_menu, mod_menu_general, mod_menu_general_win, \
    mod_menu_general_win_player, mod_menu_general_win_player_confirm


class ModdedPlaymode(AbstractPlaymode):

    _name = AbstractPlaymode.modded_gamemode
    _match_config = match_config_modded
    _ai_difficulty = AbstractPlaymode.expert_bot_path

    def __init__(self, game_map: AbstractMap, faction: AbstractFaction):
        AbstractPlaymode.__init__(self, game_map, faction)

    def get_playmode_name(self):
        return self._name

    def get_match_config_path(self):
        return self._match_config

    def get_difficulty_path(self):
        return self._ai_difficulty

    def play_middlegame(self):
        log.info("Waiting for match to finish...")
        for j in range(4):  # minutes until end
            log.info(f"Waiting for {j + 1} minute of match...")
            time.sleep(60)

    def play_endgame(self):
        log.info("Preparing for modded win...")
        time.sleep(12)
        pa.click(mod_menu)
        time.sleep(3)
        pa.click(mod_menu_general)
        time.sleep(3)
        pa.click(mod_menu_general_win)
        time.sleep(3)
        pa.click(mod_menu_general_win_player)
        time.sleep(3)
        pa.click(mod_menu_general_win_player_confirm)

    def play(self):
        self.play_opening()
        self.play_middlegame()
        self.play_endgame()
