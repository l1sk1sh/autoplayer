import pyautogui as pa
import time
from abc import ABC, abstractmethod
from autoplayer.model.map.abstract_map import AbstractMap
from autoplayer.model.faction.abstract_faction import AbstractFaction
from autoplayer.config.paths import easy_bot, expert_bot


class AbstractPlaymode(ABC):

    real_playmode = "real"
    modded_gamemode = "mode"
    easy_bot_path = easy_bot
    expert_bot_path = expert_bot

    def __init__(self, game_map: AbstractMap, faction: AbstractFaction):
        self.game_map = game_map
        self.faction = faction
        super().__init__()

    @abstractmethod
    def get_playmode_name(self):
        pass

    @abstractmethod
    def get_match_config_path(self):
        pass

    @abstractmethod
    def get_difficulty_path(self):
        pass

    def play_opening(self):
        attack_point = self.game_map.get_near_enemy_base_point()
        unit_button = self.faction.get_base_unit_button()
        unit_order_time = self.faction.get_base_unit_order_time()

        pa.press("alt")  # If you alt+tab alt-rotation screen might stuck
        pa.press(".")
        time.sleep(3)
        pa.rightClick(attack_point)  # Sending first engineers into battle

        print("Ordering units...")
        pa.press("f1")
        time.sleep(3)
        pa.rightClick(attack_point)  # Point near enemy base
        time.sleep(3)
        pa.press(unit_button)  # One should be enough to pass validation
        time.sleep(unit_order_time)  # Until next is ready to be purchased
        pa.press(unit_button)  # Just to be sure - send another squad

    @abstractmethod
    def play_middlegame(self):
        pass

    @abstractmethod
    def play_endgame(self):
        pass

    @abstractmethod
    def play(self):
        pass
