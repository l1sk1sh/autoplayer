"""Contains credentials used for Steam login. Must be filled manually
"""

import os.path
import json
import logging as log
from autoplayer.config.system import config_path
from autoplayer.model.exceptions import CredentialsNotSet

steam_username = ""
steam_password = ""


def credentials_available():
    """Returns True if credentials are ready"""
    if steam_password == "" or steam_username == "":
        return False
    else:
        return True


def read_credentials():
    """Reads credentials from config file, or creates it if it's empty/not set"""
    global steam_username
    global steam_password

    if os.path.exists(config_path) and os.path.isfile(config_path):
        log.info("Reading Steam credentials from file...")
        with open(config_path) as config_file:
            data = json.load(config_file)
            steam_username = data["steam_username"]
            steam_password = data["steam_password"]
    else:
        log.warning("Something wrong with config. Creating new one...")
        data = {
            "steam_username": "",
            "steam_password": ""
        }

        with open(config_path, 'w') as config_file:
            json.dump(data, config_file)

        raise CredentialsNotSet
