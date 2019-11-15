"""Main module that handles all logic, imports and run bots itself
"""

import time
import sys
import argparse
import os
sys.path.append(os.getcwd())  # Addition of current directory to system path
import autoplayer.config.settings as settings
import logging as log
import autoplayer.steam as steam
import autoplayer.coh2 as coh2
import autoplayer.config.config as config
from autoplayer.util.autogui_utils import scheenshot_on_fail
from autoplayer.model.exceptions import GuiElementNotFound, SteamLoginException, \
    PointsLimitReached, ApplicationFailedToStart
from autoplayer.asserter import Asserter
from autoplayer.config.system import process_coh2, process_steam
from autoplayer.util.system_utils import is_process_running, kill_process
from autoplayer.model.playmode.abstract_playmode import AbstractPlaymode as ap
from autoplayer.model.playmode.real_playmode import RealPlaymode
from autoplayer.model.playmode.modded_playmode import ModdedPlaymode
from autoplayer.model.faction.abstract_faction import AbstractFaction as af
from autoplayer.model.faction.bri_faction import BRIFaction
from autoplayer.model.faction.ger_faction import GERFaction
from autoplayer.model.faction.okw_faction import OKWFaction
from autoplayer.model.faction.rus_faction import RUSFaction
from autoplayer.model.faction.usa_faction import USAFaction
from autoplayer.model.map.abstract_map import AbstractMap as am
from autoplayer.model.map.langresskaya import LangresskayaMap


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
    parser.add_argument("-g", "--grid", type=bool,
                        help="if grid keyboard layout is used",
                        default=True)
    args = vars(parser.parse_args(argv))

    grid_layout_used = args.get("grid")

    if args.get("map") == am.langresskaya_name:
        game_map = LangresskayaMap()

    if args.get("faction") == af.british_name:
        faction = BRIFaction(grid_layout_used)
    elif args.get("faction") == af.wehrmacht_name:
        faction = GERFaction(grid_layout_used)
    elif args.get("faction") == af.okw_name:
        faction = OKWFaction(grid_layout_used)
    elif args.get("faction") == af.ussr_name:
        faction = RUSFaction(grid_layout_used)
    elif args.get("faction") == af.usa_name:
        faction = USAFaction(grid_layout_used)

    if args.get("playmode") == ap.real_playmode:
        playmode = RealPlaymode(game_map, faction)
    elif args.get("playmode") == ap.modded_gamemode:
        playmode = ModdedPlaymode(game_map, faction)

    amount_of_matches = args.get("amount")
    consider_points_limit = args.get("i")

    try:
        application_start = time.time()

        asserter = Asserter(faction, playmode, game_map)
        asserter.assert_preload()

        if asserter.is_coh_running:
            coh2.focus_on_game()
            if coh2.is_main_menu():
                log.info("Seems that game is opened in main menu...")
                coh2.open_network_and_battle()
                coh2.configure_match()
        elif asserter.is_steam_running:
            steam.launch_coh2()
            coh2.wait_coh2_readiness()
            coh2.configure_match()
        else:
            steam.login(settings.get_steam_username(), settings.get_steam_password())
            steam.launch_coh2()
            coh2.wait_coh2_readiness()
            coh2.configure_match()

        asserter.assert_game_setup()

        if not asserter.is_correct_faction:
            coh2.select_faction(faction)

        try:
            for i in range(amount_of_matches):
                coh2.play_match(i, playmode, consider_points_limit)
        except PointsLimitReached:
            log.warning("Points limit for game has been reached.")

        log.info("=====================")
        log.info(f"Script finished! It took {time.time() - application_start}s.")

        coh2.close_game()
        steam.shutdown()

    except GuiElementNotFound as e:
        log.error(f"Element \"{e.element}\" was not found.")
        scheenshot_on_fail()
    except TypeError as t:
        log.error(f"Probably, failed to find element.")
        log.error(t, exc_info=True)
        scheenshot_on_fail()
    except SteamLoginException:
        log.error(f"Failed to login to Steam account. Check {config.settings_path} file.")
    except ApplicationFailedToStart as a:
        log.error(f"Expecting that \"{a.application}\" should be running, but it is not.")
    except Exception as e:
        log.error(f"Something wrong happened!")
        log.error(e, exc_info=True)
    finally:
        if is_process_running(process_steam) or is_process_running(process_coh2):
            kill_process(process_coh2)
            kill_process(process_steam)
            sys.exit(1)
        else:
            sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
