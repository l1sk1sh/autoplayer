"""Main module that handles all logic, imports and run bots itself
"""

import argparse
import sys
import os
sys.path.append(os.getcwd())  # Addition of current directory to system path
import logging as log
import autoplayer.config.settings as settings
import autoplayer.coh2.main as coh2

log.basicConfig(
    level=log.INFO,
    format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
    handlers=[
        log.FileHandler("{0}/{1}.log".format(settings.get_temp_dir(), "autoplayer-coh2")),
        log.StreamHandler()
    ])

supported_games = ["coh2", "dst"]


def main(argv):
    """Verifies if specified during launch game is supported by program"""

    parser = argparse.ArgumentParser(description="Autoplayer launcher")
    parser.add_argument("-g", "--game", type=str,
                        choices=supported_games,
                        help="select game that will be used in autoplayer")
    args = vars(parser.parse_known_args(argv))

    if args.get("game") == supported_games[0]:
        log.info("Launching Company of Heroes 2 autoplayer...")
        coh2.run(argv)
    elif args.get("game") == supported_games[1]:
        log.warning("DST is not implemented yet.")
        sys.exit(0)
    else:
        log.error(f"Game should be selected from {supported_games} to launch autoplayer!")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
