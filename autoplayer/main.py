import psutil
import pyautogui as pa
import time
import platform
import traceback

debug = True

required_processes = {
    "coh2": "RelicCoH2.exe",
    "ce": "CheatEnginePortable.exe"
}

window_names = {
    "coh2": "Company Of Heroes 2",
    "ce": "Cheat Engine 6.7"
}

amount_of_matches = 12  # Maximum for modded game

"""Asserts before launch"""
if platform.system() != "Windows":
    print("Current script is designed for Windows only.")
    exit(1)

local_processes = [p.name() for p in psutil.process_iter()]
if not all(pr in local_processes for pr in required_processes.values()):
    print("Seems that one of the required programs is not launched.")
    exit(1)

print("Make sure that keyboard layout is English!")
time.sleep(5)

"""Find coh2 icon and focus on it"""
coh2_icon_x_y = pa.locateCenterOnScreen(
    './resources/coh2_icon.png',
    grayscale=False, confidence=0.98)
pa.click(coh2_icon_x_y)

# TODO Assert that map is prepared in-game

# TODO Improve logging and add in-game logging (enter chat)

# TODO Add timing calculations

# TODO Separate OKV config (and think about another)

# TODO Add warning + assert in game about resolution

# TODO Add launch arguments processing

# TODO Separate map configuration (with coordinates)

# TODO Think about joining play function, as first and last parts must be same

# TODO Separate all coordinates and asserts corresponding to screen resolution


def on_ce():
    """Enable CE scripts"""
    pa.keyDown("ctrl")
    pa.press("[")
    pa.keyUp("ctrl")


def off_ce():
    """Disable CE scripts"""
    pa.keyDown("ctrl")
    pa.press("]")
    pa.keyUp("ctrl")


def wait_for_element(element: str, iter_time: int, iter_amount: int):
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
            print(f"Waiting for element '{element}' for #{count} time.")

    return False


def start_match():
    """Starts match, waits for load"""
    # TODO Move mouse to the center of the screen
    """Find start game button and click it"""
    try:
        print("Locating 'Start match button'...")
        coh2_start_game_x_y = pa.locateCenterOnScreen(
            './resources/coh2_start_game.png',
            grayscale=False, confidence=0.98)
        pa.click(coh2_start_game_x_y)
    except TypeError:
        print("Button is not visible ot match is a go. Hitting blindly...")
        pa.click(684, 704)

    """Wait for game to load and try to find 'press any key' message"""
    if wait_for_element("./resources/coh2_press_anykey.png", 20, 4):
        print("Starting match...")
        pa.press("escape")
    elif not debug:
        print("Could not start match!")
        raise Exception

    time.sleep(10)  # Sleep for n seconds to skip dimming screen


def end_match():
    time.sleep(25)  # Usually 15s to load winning screen + 10 for boxes
    print("Closing winning screen...")
    for c in range(4):  # Close lootboxes
        pa.click(608, 60)  # Hit exit button
        time.sleep(3)

    print("Match ended!")


def usual_match():
    """Tries to play as usual using Cheat Engine
    As for now, CE breaks victory points
    """

    # TODO One squad is enough to get reward

    """Locate enemy base"""
    coh2_enemy_base_x_y = pa.locateCenterOnScreen(
        './resources/coh2_enemy_base.png',
        confidence=0.92)
    pa.click(coh2_enemy_base_x_y)
    print("Hey! Change it to .click + .rightClick ", coh2_enemy_base_x_y)

    """Set rally point on the enemy base"""
    pa.press("f1")
    center_screen_x_y = [x / 2 for x in pa.size()]
    pa.moveTo(center_screen_x_y)
    pa.rightClick()

    # TODO Rewrite ordering flow to more comprehensive ans fast
    # Folsk - 24 s
    # Engineers - 28 s
    # Phep - 32 s

    """Order units"""
    on_ce()
    time.sleep(5)
    pa.press("v")
    time.sleep(5)
    pa.press("v")
    time.sleep(10)
    pa.press("s")

    """Order some more for period of time"""
    off_ce()
    cnt = 0
    while cnt != 3:
        time.sleep(24)
        pa.press("s")
        cnt = cnt + 1

    """Order killing units and be immortal"""
    time.sleep(60)
    on_ce()
    cnt = 0
    while cnt != 4:
        time.sleep(24)
        pa.press("r")
        cnt = cnt + 1

    # TODO Locate winning screen here for some time
    minutes_to_end = 2
    print(f"Waiting for {minutes_to_end} minutes...")
    time.sleep((60 * minutes_to_end) + 30)  # Wait for match to finish
    end_match()


def mod_play():
    """Plays with Cheat Command 2 mod for 5 minutes and sets the winner
    """

    print("Ordering units...")
    pa.press("f1")
    pa.rightClick(120, 679)  # Point near enemy base
    pa.press("v")  # One should be enough to pass validation
    time.sleep(28)  # Until next is ready to be purchased
    pa.press("v")  # Just to be sure - send another squad
    time.sleep(20)  # Buffer time

    # TODO Notify that you are free to do by Enter
    print("Waiting for match to finish...")
    for j in range(4):  # minutes until end
        print(f"Waiting for {j+1} minute of match...")
        time.sleep(60)

    print("Preparing for win...")
    time.sleep(3)
    pa.click(118, 12)  # button_cc_menu_x_y
    time.sleep(3)
    pa.click(96, 98)  # button_cc_menu_general_x_y
    time.sleep(3)
    pa.click(289, 255)  # button_cc_menu_general_win_x_y
    time.sleep(3)
    pa.click(516, 262)  # button_cc_menu_general_win_player_x_y
    time.sleep(3)
    pa.click(624, 454)  # button_cc_menu_general_win_player_ok_x_y
    time.sleep(5)  # Count down till winning

    end_match()


try:
    """Handling functions and between game throws"""
    for i in range(amount_of_matches):
        off_ce()
        print(f"Game #{i}")
        start_match()
        mod_play()

        if wait_for_element("./resources/coh2_summary_close.png", 20, 4):
            pa.click(642, 677)  # Click summary exit button
        elif not debug:
            print("Could not hit summary exit button!")
            raise Exception

        time.sleep(8)  # Waiting for preparation screen to load

    print("Execution has ended!")


except Exception as e:
    traceback.print_exc()
    print(f"Seems that something is broken: '{e}'. Pausing the game...")
    pa.press("escape")
    exit(1)
