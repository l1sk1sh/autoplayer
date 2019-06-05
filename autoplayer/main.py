import pyautogui as pa
import time
import traceback
import sys
import argparse
from autoplayer.asserter import Asserter
from autoplayer.util.autogui_utils import wait_for_element
from autoplayer.model.faction.abstract_faction import AbstractFaction as af
from autoplayer.model.map.abstract_map import AbstractMap as am
from autoplayer.model.playmode.abstract_playmode import AbstractPlaymode as ap
from autoplayer.model.playmode.real_playmode import RealPlaymode
from autoplayer.model.playmode.modded_playmode import ModdedPlaymode
from autoplayer.model.faction.bri_faction import BRIFaction
from autoplayer.model.faction.ger_faction import GERFaction
from autoplayer.model.faction.okw_faction import OKWFaction
from autoplayer.model.faction.rus_faction import RUSFaction
from autoplayer.model.faction.usa_faction import USAFaction
from autoplayer.model.map.langresskaya import LangresskayaMap


# TODO Cheat engine hotkeys: ctrl+[ / ctrl+] - unlimited resources
# ctrl+num2 / ctrl+num0 - fast construction


def main(argv):

    playmode = None
    faction = None
    game_map = None

    parser = argparse.ArgumentParser(description="CoH2 autoplayer bot")
    parser.add_argument("-p", "--playmode", type=str,
                        choices=[ap.real_playmode, ap.modded_gamemode],
                        help="select one of the script modes to play",
                        default=ap.modded_gamemode)
    parser.add_argument("-f", "--faction", type=str,
                        choices=[af.okw_name, af.ussr_name, af.british_name, af.wehrmacht_name, af.usa_name],
                        help="select faction to be used for play",
                        default=af.okw_name)
    parser.add_argument("-m", "--map", type=str,
                        choices=[am.langresskaya_name],
                        help="select map to be run at",
                        default=am.langresskaya_name)
    parser.add_argument("-a", "--amount", type=int,
                        help="amount of games to be played",
                        default=12)
    parser.add_argument("-i", type=bool,
                        help="ignore points limit",
                        default=True)
    args = vars(parser.parse_args(argv))

    if args.get("map") == am.langresskaya_name:
        game_map = LangresskayaMap()

    if args.get("faction") == af.british_name:
        faction = BRIFaction()
    elif args.get("faction") == af.wehrmacht_name:
        faction = GERFaction()
    elif args.get("faction") == af.okw_name:
        faction = OKWFaction()
    elif args.get("faction") == af.ussr_name:
        faction = RUSFaction()
    elif args.get("faction") == af.usa_name:
        faction = USAFaction()

    if args.get("playmode") == ap.real_playmode:
        playmode = RealPlaymode(game_map, faction)
    elif args.get("playmode") == ap.modded_gamemode:
        playmode = ModdedPlaymode(game_map, faction)

    amount_of_matches = args.get("amount")
    ignore_points_limit = args.get("i")

    try:
        application_start = time.time()
        asserter = Asserter(faction, playmode, game_map)
        asserter.assert_preload()
        pa.click(pa.locateCenterOnScreen("./resources/coh2_icon.png"))
        asserter.assert_game_setup()

        for i in range(amount_of_matches):
            print("\n=====================")
            print(f"Playing game #{i}")

            if pa.locateOnScreen("./resources/no_points.png") is None and ignore_points_limit:
                print("Points limit reached. Script won't run")
                break

            start_match_time = time.time()
            pa.moveTo([x / 2 for x in pa.size()])
            try:
                print("Locating 'Start match button'...")
                pa.click(pa.locateCenterOnScreen(
                    './resources/start_game.png', confidence=0.98))
            except TypeError:
                print("Button is not visible. Hitting blindly...")
                pa.click(684, 704)

            if wait_for_element("./resources/press_anykey.png", 20, 4):
                print("Starting match...")
                pa.press("escape")
            else:
                print("Could not start match!")
                raise Exception("'press_anykey' was not found!")
            time.sleep(10)  # Sleep for n seconds to skip dimming screen
            print(f"Match load #{i} took {time.time() - start_match_time}s.")

            play_time = time.time()
            playmode.play()
            time.sleep(28)  # Usually 15s to load winning screen + 10 for boxes
            print("Closing winning screen...")
            for c in range(4):  # Close lootboxes
                pa.click(608, 60)  # Hit exit button
                time.sleep(3)

            print("Match ended!")
            print(f"The game #{i} took {time.time() - play_time}s.")

            if wait_for_element("./resources/summary_close.png", 20, 4):
                pa.click(642, 677)  # Click summary exit button
            else:
                print("Could not hit summary exit button!")
                raise Exception

            time.sleep(8)  # Waiting for preparation screen to load

        print(f"Script finished! It took {time.time() - application_start}s.")
    except Exception as e:
        traceback.print_exc()
        print(f"Seems that something is broken: '{e}'. Pausing the game...")
        pa.press("escape")
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
