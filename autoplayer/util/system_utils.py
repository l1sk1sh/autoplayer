"""Contains utils connected with system itself
"""

import psutil
import os
import logging as log
from autoplayer.coh2.model.exceptions import Error


def is_process_running(process: str, local_processes: list = None):
    """Checks if specified process is still running"""

    if local_processes is None:
        local_processes = [p.name().lower() for p in psutil.process_iter()]

    if process.lower() in local_processes:
        return True
    else:
        return False


def kill_process(process):
    """Kills specified process name"""

    try:
        os.system(f"TASKKILL /F /IM {process}")
    except Error:
        log.error("Couldn't kill")
