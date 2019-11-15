"""Contains credentials used for Steam login. Must be filled manually
"""

import os.path
import json
import logging as log
import autoplayer.util.crypt_util as crypt
from autoplayer.config.config import settings_path, workdir

_steam_username = ""
_steam_password = ""
_temp_dir = workdir + "/../tmp/"


def _write_settings():
    """Writes current variables into file"""

    w_data = {
        "steam_username": _steam_username,
        "steam_password": _steam_password,
        "temp_dir": _temp_dir
    }

    with open(settings_path, 'w') as w_settings_file:
        json.dump(w_data, w_settings_file)


def _exit_without_credentials():
    """Stop execution with message about credentials"""

    log.error(f"Configure {settings_path} and restart application.")


if os.path.exists(settings_path) and os.path.isfile(settings_path):
    log.info("Reading Steam credentials from file...")
    with open(settings_path) as settings_file:
        data = json.load(settings_file)
        _steam_username = data["steam_username"]
        _steam_password = data["steam_password"]
        _temp_dir = data["temp_dir"]

    if _steam_username == "" or _steam_password == "":
        _exit_without_credentials()

    if not crypt.is_encrypted(_steam_password):
        _steam_password = crypt.encrypt_string(_steam_password)
        _write_settings()
else:
    log.warning("Something wrong with config. Creating new one...")
    _write_settings()
    _exit_without_credentials()

if not os.path.exists(_temp_dir):
    os.makedirs(_temp_dir)
log.basicConfig(
    level=log.INFO,
    format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
    handlers=[
        log.FileHandler("{0}/{1}.log".format(_temp_dir, "autoplayer-coh2")),
        log.StreamHandler()
    ])


def get_steam_username():
    """Returns steam username"""

    return _steam_username


def get_steam_password():
    """Returns decrypted steam password"""

    return crypt.decrypt_string(_steam_password)


def get_temp_dir():
    """Returns temporary directory"""

    return _temp_dir
