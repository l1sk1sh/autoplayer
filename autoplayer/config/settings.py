"""Contains credentials used for Steam login. Must be filled manually
"""

import os.path
import json
import logging as log
import autoplayer.util.crypt_util as crypt
from autoplayer.config.config import settings_path, workdir
from autoplayer.model.exceptions import CredentialsNotSet

_steam_username = ""
_steam_password = ""
temp_dir = workdir + "../../tmp/"


def read_settings_file():
    """Reads credentials from config file, or creates it if it's empty/not set"""
    global _steam_username
    global _steam_password
    global temp_dir

    if os.path.exists(settings_path) and os.path.isfile(settings_path):
        log.info("Reading Steam credentials from file...")
        with open(settings_path) as settings_file:
            data = json.load(settings_file)
            _steam_username = data["steam_username"]
            _steam_password = data["steam_password"]
            temp_dir = data["temp_dir"]

        if not crypt.is_encrypted(_steam_password):
            _steam_password = crypt.encrypt_string(_steam_password)
            _write_settings()
    else:
        log.warning("Something wrong with config. Creating new one...")
        _write_settings()
        raise CredentialsNotSet


def _write_settings():
    """Writes current variables into file"""
    data = {
        "steam_username": _steam_username,
        "steam_password": _steam_password,
        "temp_dir": temp_dir
    }

    with open(settings_path, 'w') as settings_file:
        json.dump(data, settings_file)


def get_steam_username():
    """Returns steam username"""
    return _steam_username


def get_steam_password():
    """Returns decrypted steam password"""
    return crypt.decrypt_string(_steam_password)

