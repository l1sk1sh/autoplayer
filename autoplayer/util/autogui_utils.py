"""Contains utils for PyAutoGui
"""

import time
import logging as log
import pyautogui as pa
from autoplayer.config import settings


def wait_for_element(element: str, iter_time: int, iter_amount: int):
    """Waits for iter_time and returns coordinates of element. Otherwise - False"""

    count = 0
    while count != iter_amount:
        time.sleep(iter_time)
        try:
            position = pa.locateCenterOnScreen(element, confidence=0.8)
            if position is not None:
                return position
            else:
                raise TypeError
        except TypeError:
            count = count + 1
            log.info(f"Waiting for element '{element}' for #{count} time.")

    return False


def scheenshot_on_fail():
    """Creates screenshot of failed scenario"""

    pa.screenshot(settings.get_temp_dir() + "gui_element_notfound_" + str(time.time()) + ".png")

