"""Main command for launching and running Company of Heroes 2
"""

import time
import argparse
import sys
import logging as log
import autoplayer.config.settings as settings
import autoplayer.steam as steam
import autoplayer.config.config as config
from autoplayer.steam import process_steam
from autoplayer.util.autogui_utils import scheenshot_on_fail
from autoplayer.coh2.model.exceptions import GuiElementNotFound, SteamLoginException, \
    PointsLimitReached, ApplicationFailedToStart, ApplicationFailedToOpen
from autoplayer.util.system_utils import is_process_running, kill_process
from autoplayer.coh2.model.playmode.abstract_playmode import AbstractPlaymode as ap
from autoplayer.coh2.model.playmode.real_playmode import RealPlaymode
from autoplayer.coh2.model.playmode.modded_playmode import ModdedPlaymode
from autoplayer.coh2.model.faction.abstract_faction import AbstractFaction as af
from autoplayer.coh2.model.faction.bri_faction import BRIFaction
from autoplayer.coh2.model.faction.ger_faction import GERFaction
from autoplayer.coh2.model.faction.okw_faction import OKWFaction
from autoplayer.coh2.model.faction.rus_faction import RUSFaction
from autoplayer.coh2.model.faction.usa_faction import USAFaction
from autoplayer.coh2.model.map.abstract_map import AbstractMap as am
from autoplayer.coh2.model.map.langresskaya import LangresskayaMap

process_coh2 = "RelicCoH2.exe"
process_ce = "CheatEnginePortable.exe"

window_name_coh2 = "Company Of Heroes 2"
window_name_ce = "Cheat Engine 6.7"

coh2_appid = "231430"
coh2_launch_params = "-window –fullwindow -lockmouse -novsync -nomovies"


def run(argv):
    """Launches CoH 2 Asserter, then launches Steam and plays the game"""

    import autoplayer.coh2.game as game
    from autoplayer.coh2.asserter import Asserter

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
    args, ignore = parser.parse_known_args(argv)

    grid_layout_used = args.grid

    if args.map == am.langresskaya_name:
        game_map = LangresskayaMap()

    if args.faction == af.british_name:
        faction = BRIFaction(grid_layout_used)
    elif args.faction == af.wehrmacht_name:
        faction = GERFaction(grid_layout_used)
    elif args.faction == af.okw_name:
        faction = OKWFaction(grid_layout_used)
    elif args.faction == af.ussr_name:
        faction = RUSFaction(grid_layout_used)
    elif args.faction == af.usa_name:
        faction = USAFaction(grid_layout_used)

    if args.playmode == ap.real_playmode:
        playmode = RealPlaymode(game_map, faction)
    elif args.playmode == ap.modded_gamemode:
        playmode = ModdedPlaymode(game_map, faction)

    amount_of_matches = args.amount
    consider_points_limit = args.i

    try:
        application_start = time.time()

        asserter = Asserter(faction, playmode, game_map)
        asserter.assert_preload()

        if asserter.is_coh_running:
            game.focus_on_game()
            if game.is_main_menu():
                log.info("Seems that game is opened in main menu...")
                game.open_network_and_battle()
                game.configure_match()
        elif asserter.is_steam_running:
            steam.launch_game(coh2_appid, coh2_launch_params)
            game.wait_coh2_readiness()
            game.configure_match()
        else:
            steam.login(settings.get_steam_username(), settings.get_steam_password())
            steam.launch_game(coh2_appid, coh2_launch_params)
            game.wait_coh2_readiness()
            game.configure_match()

        asserter.assert_game_setup()

        if not asserter.is_correct_faction:
            game.select_faction(faction)

        try:
            for i in range(amount_of_matches):
                game.play_match(i, playmode, consider_points_limit)
        except PointsLimitReached:
            log.warning("Points limit for game has been reached.")

        log.info("=====================")
        log.info(f"Script finished! It took {time.time() - application_start}s.")

        game.close_game()
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
        log.error(f"Application \"{a.application}\" failed to launch. Leaving applications a running.")
        if is_process_running(process_steam):
            sys.exit(1)
    except ApplicationFailedToOpen as a:
        log.error(f"Expecting that \"{a.application}\" should be running according to checks, but it is not.")
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
