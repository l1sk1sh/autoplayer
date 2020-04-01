from autoplayer.coh2.model.playmode.abstract_playmode import AbstractPlaymode
from autoplayer.coh2.model.map.abstract_map import AbstractMap
from autoplayer.coh2.model.faction.abstract_faction import AbstractFaction
from autoplayer.coh2.paths import match_config_real

# Cheat engine hotkeys: ctrl+[ / ctrl+] - unlimited resources
# ctrl+num2 / ctrl+num0 - fast construction


class RealPlaymode(AbstractPlaymode):

    _name = AbstractPlaymode.real_playmode
    _match_config = match_config_real
    _ai_difficulty = AbstractPlaymode.easy_bot_path

    def __init__(self, game_map: AbstractMap, faction: AbstractFaction):
        AbstractPlaymode.__init__(self, game_map, faction)

    def get_playmode_name(self):
        return self._name

    def get_match_config_path(self):
        return self._match_config

    def get_difficulty_path(self):
        return self._ai_difficulty

    def play_middlegame(self):
        pass

    def play_endgame(self):
        pass

    def play(self):
        pass
        # This code is ripped from the middle of play
        # Seems that usual key points victory play is always failed
        # No clues what other verifications are on board
        # This playmode is halted, as maximum is 30k vs 24k for modded

        # pa.click(attack_point)  # Focus on enemy base
        # # time.sleep(28)
        # pa.press("r")
        # time.sleep(32)
        #
        # time.sleep(60)  # They are killing too fast
        # time.sleep(60)
        # for x in range(4):
        #     pa.press("r")
        #     time.sleep(32)
        #
        # # Total ~4.45 s
        #
        # # Wait for small box to show up at winning screen
        # if wait_for_element("./resources/winning_box.png", 20, 8):
        #     print("Winning screen located")
        #     pa.press("escape")
        # else:
        #     print(
        #         f"Winning screen could not be located for {20 * 8} seconds!")
        #     raise Exception("Failed to located winning screen")
