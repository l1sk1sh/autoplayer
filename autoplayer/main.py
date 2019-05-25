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

# Asserts
if platform.system() != "Windows":
    print("Current script is designed for Windows only.")
    exit(1)

local_processes = [p.name() for p in psutil.process_iter()]
if not all(process in local_processes for process in required_processes.values()):
    print("Seems that one of the required programs is not launched.")
    exit(1)

print("Make sure that keyboard layout is English!")

"""Find coh2 icon and focus on it"""
coh2_icon_x_y = pa.locateCenterOnScreen(
    './resources/coh2_icon.png',
    grayscale=False, confidence=0.98)
pa.click(coh2_icon_x_y)

# TODO Assert that map is prepared in-game


def en_ce():
    """Enable CE scripts"""
    pa.keyDown("ctrl")
    pa.press("[")
    pa.keyUp("ctrl")


def di_ce():
    """Disable CE scripts"""
    pa.keyDown("ctrl")
    pa.press("]")
    pa.keyUp("ctrl")


def start_game():
    """Starts match, waits for load"""

    """Find start game button and click it"""
    try:
        print("Locating 'Start match button'...")
        coh2_start_game_x_y = pa.locateCenterOnScreen(
            './resources/coh2_start_game.png',
            grayscale=False, confidence=0.98)
        pa.click(coh2_start_game_x_y)
    except TypeError:
        print("Seems that button is not visible. Hitting blindly.")
        pa.click(684, 704)

    """Wait for game to load and try to find 'press anykey'"""
    wait = 30  # seconds
    match_started = False
    count = 0
    while count != 3:
        time.sleep(wait)
        try:
            if pa.locateOnScreen('./resources/coh2_press_anykey.png',
                                 confidence=0.98) is not None:
                print("Starting match...")
                pa.press("escape")
                match_started = True
                break
            else:
                raise TypeError
        except TypeError:
            count = count + 1
            print(f"Waiting for game to load for #{count} time.")

    if not match_started and not debug:
        print("Could start match!")
        raise Exception

    time.sleep(10)  # Sleep for n seconds to skip dimming screen


def end_match():
    print("Closing winning screen...")
    pa.click(608, 60)  # Close lootboxes
    time.sleep(3)
    pa.click(608, 60)
    time.sleep(3)
    pa.click(608, 60)  # Click "exit" at the winning screen
    print("Match ended!")


def usual_match():
    """Tries to play as usual using Cheat Engine
    As for now, CE breaks victory points
    """

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
    # Folsk - 24
    # Engineers - 28
    # Phep - 32

    """Order units"""
    en_ce()
    time.sleep(5)
    pa.press("v")
    time.sleep(5)
    pa.press("v")
    time.sleep(10)
    pa.press("s")

    """Order some more for period of time"""
    di_ce()
    cnt = 0
    while cnt != 3:
        time.sleep(24)
        pa.press("s")
        cnt = cnt + 1

    """Order killing units and be immortal"""
    time.sleep(60)
    en_ce()
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
    """Plays with Cheat Command 2 mod for 5 minutes
    sets the winner
    """

    map_central_enemy_point = (120, 679)

    print("Ordering units...")
    pa.press("f1")
    pa.rightClick(map_central_enemy_point)
    pa.press("v")
    time.sleep(3)
    pa.press("s")
    time.sleep(3)
    pa.press("v")
    time.sleep(28)
    pa.press("s")
    pa.press("v")

    print("Preparing for win...")
    time.sleep(5)
    pa.click(118, 12)  # button_cc_menu_x_y
    time.sleep(3)
    pa.click(96, 98)  # button_cc_menu_general_x_y
    time.sleep(3)
    pa.click(289, 255)
    time.sleep(3)
    pa.click(516, 262)  # button_cc_menu_general_win_player_x_y

    minutes_to_end = 4
    print(f"Waiting for {minutes_to_end} minutes...")
    time.sleep((60 * minutes_to_end) + 30)  # Wait for match to finish
    pa.click(624, 454)  # button_cc_menu_general_win_player_ok_x_y
    time.sleep(32)  # Wait
    end_match()


try:
    """Handling functions and between game throws"""
    for i in range(4):
        di_ce()
        print(f"Game #{i}")
        start_game()
        mod_play()
        time.sleep(60)  # Wait for game to return to menu
        pa.click(642, 677)  # Click summary exit button
        time.sleep(8)  # Waiting for preparation screen to load

    print("Execution has ended!")


except Exception:
    traceback.print_exc()
    print("\nPausing the game...")
    pa.press("escape")
