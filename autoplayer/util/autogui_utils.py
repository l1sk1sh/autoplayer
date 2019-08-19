"""Contains utils for PyAutoGui
"""

import time
import logging as log
import pyautogui as pa


def wait_for_element(element: str, iter_time: int, iter_amount: int):
    """Waits for iter_time and returns coordinates of element. Otherwise - False"""

    count = 0
    while count != iter_amount:
        time.sleep(iter_time)
        try:
            position = pa.locateCenterOnScreen(element, confidence=0.98)
            if position is not None:
                return position
            else:
                raise TypeError
        except TypeError:
            count = count + 1
            log.info(f"Waiting for element '{element}' for #{count} time.")

    return False
