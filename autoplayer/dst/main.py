"""Main command for launching and running Don't Starve Together
"""

import time
import sys
import logging as log
import autoplayer.config.settings as settings
import autoplayer.config.config as config
import autoplayer.steam as steam
from autoplayer.steam import process_steam
from autoplayer.util.system_utils import is_process_running, kill_process
from autoplayer.dst.model.exceptions import SteamLoginException, ApplicationFailedToStart, ApplicationFailedToOpen, \
    MenuIsNotReached

process_dst = "dontstarve_steam_x64.exe"

window_name_dst = "Don't Starve Together"

dst_appid = "322330"
dst_launch_params = ""


def run():
    """Launches DST Asserter, then launches Steam and plays the game"""

    import autoplayer.dst.game as game
    from autoplayer.dst.asserter import Asserter

    try:
        application_start = time.time()

        asserter = Asserter()
        asserter.assert_preload()

        if asserter.is_dst_running:
            game.focus_on_game()
        elif asserter.is_steam_running:
            steam.launch_game(dst_appid, dst_launch_params)
            game.wait_dst_readiness()
        else:
            steam.login(settings.get_steam_username(), settings.get_steam_password())
            steam.launch_game(dst_appid, dst_launch_params)
            game.wait_dst_readiness()

        game.take_present()

        log.info("=====================")
        log.info(f"Script finished! It took {time.time() - application_start}s.")

        kill_process(process_dst)
        steam.shutdown()
    except SteamLoginException:
        log.error(f"Failed to login to Steam account. Check {config.settings_path} file.")
    except ApplicationFailedToStart as a:
        log.error(f"Application \"{a.application}\" failed to launch. Leaving applications a running.")
        if is_process_running(process_steam):
            sys.exit(1)
    except ApplicationFailedToOpen as a:
        log.error(f"Expecting that \"{a.application}\" should be running according to checks, but it is not.")
    except MenuIsNotReached:
        log.error(f"Main menu has not been reached for some reason. It is possible, that game has new popups.")
    finally:
        if is_process_running(process_steam) or is_process_running(process_dst):
            kill_process(process_steam)
            kill_process(process_dst)
            sys.exit(1)
        else:
            sys.exit(0)
