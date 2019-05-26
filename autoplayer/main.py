import psutil
import pyautogui as pa
import time
import platform
import traceback

debug = True
real_game = True
amount_of_matches = 12  # Maximum for modded game
faction = "okv"
faction_symbol = "./resources/okv_symbol_setup.png"
screen_resolution = (1366, 768)

process_coh2 = "RelicCoH2.exe"
process_ce = "CheatEnginePortable.exe"

window_name_coh2 = "Company Of Heroes 2"
window_name_ce = "Cheat Engine 6.7"


def assert_preload():
    """Asserts before launch of the application
    """

    if platform.system() != "Windows":
        print("Current script is designed for Windows only.")
        exit(1)

    local_processes = [p.name() for p in psutil.process_iter()]

    if process_coh2 not in local_processes:
        print("Company of Heroes 2 is not launched!")
        exit(1)

    if process_ce not in local_processes and real_game:
        print("Cheat engine is required for 'real' game!")
        exit(1)

    print("WARNING: Make sure that keyboard layout is English!")
    time.sleep(5)

    if real_game:
        print("WARNING: Make sure that Cheat Engine is configured!")
        time.sleep(5)


def assert_game_setup():
    """Assert match configuration
    """

    print("Checking match setup...")
    if pa.size() != screen_resolution:
        print(f"Screen size is not {screen_resolution}!")
        exit(1)

    print("Checking faction...")
    if faction == "okv":
        if pa.locateOnScreen(faction_symbol) is None:
            print(f"Seems that selected faction is not {faction}!")
            exit(1)

    print("Checking map...")
    if pa.locateOnScreen("./resources/map_name.png") is None:
        print("Selected map is not 'Лангресская'!")
        exit(1)

    print("Checking match configuration...")
    if real_game:
        if pa.locateOnScreen("./resources/match_config_real.png") is None:
            print("Real match configuration must include:"
                  "\n\t- No modifications"
                  "\n\t- Standard resources"
                  "\n\t- Specified positions"
                  "\n\t- Annihilation")
            exit(1)
    else:
        if pa.locateOnScreen("./resources/match_config_mod.png") is None:
            print("Modded configuration must include:"
                  "\n\t- Standard resources"
                  "\n\t- Specified positions"
                  "\n\t- CheatCommands Mod II (Annih.)")
            exit(1)

    print("Checking AI difficulty...")
    if real_game:
        if pa.locateOnScreen("./resources/ai_easy.png") is None:
            print("WARNING: 'Real' game will take too long with not easy bot!")
            exit(1)
    else:
        if pa.locateOnScreen("./resources/ai_expert.png") is None:
            print("WARNING: Modded game is preferred against expert computer.")

    print("Match setup verification is complete.")


def on_ce():
    """Enable CE scripts
    """

    pa.keyDown("ctrl")
    pa.press("[")
    pa.keyUp("ctrl")


def off_ce():
    """Disable CE scripts
    """

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
    """Starts match, waits on the loading screen
    """

    pa.moveTo(center_screen_x_y)
    try:
        print("Locating 'Start match button'...")
        pa.click(pa.locateCenterOnScreen(
            './resources/start_game.png', confidence=0.98))
    except TypeError:
        print("Button is not visible ot match is a go. Hitting blindly...")
        pa.click(684, 704)

    if wait_for_element("./resources/press_anykey.png", 20, 4):
        print("Starting match...")
        pa.press("escape")
    else:
        print("Could not start match!")
        raise Exception("'press_anykey' was not found!")

    time.sleep(10)  # Sleep for n seconds to skip dimming screen


def play():
    """Plays the actual game
    """

    # TODO Seems that CE somehow screws up verification
    # Try separating God mode and Money. Then play with money only

    attack_point = (113, 715) if real_game else (120, 679)

    pa.press(",")
    pa.rightClick(attack_point)  # Sending first engineers into battle

    print("Ordering units...")
    pa.press("f1")
    pa.rightClick(attack_point)  # Point near enemy base
    time.sleep(5)
    pa.press("v")  # One should be enough to pass validation
    # time.sleep(28)  # Until next is ready to be purchased
    # pa.press("v")  # Just to be sure - send another squad

    if real_game:
        pa.click(attack_point)  # Focus on enemy base
        # time.sleep(28)
        on_ce()  # Get infinite money
        pa.press("r")
        off_ce()  # Allow infantry to be killed
        time.sleep(32)

        time.sleep(60)  # They are killing too fast
        on_ce()
        time.sleep(60)
        for x in range(4):
            pa.press("r")
            time.sleep(32)

        # Total ~4.45 s

        # Wait for small box to show up at winning screen
        if wait_for_element("./resources/winning_box.png", 20, 8):
            print("Winning screen located")
            pa.press("escape")
        else:
            print(f"Winning screen could not be located for {20 * 8} seconds!")
            raise Exception("Failed to located winning screen")

    else:
        print("Waiting for match to finish...")
        for j in range(4):  # minutes until end
            print(f"Waiting for {j + 1} minute of match...")
            time.sleep(60)

        print("Preparing for modded win...")
        time.sleep(12)
        pa.click(118, 12)  # button_cc_menu_x_y
        time.sleep(3)
        pa.click(96, 98)  # button_cc_menu_general_x_y
        time.sleep(3)
        pa.click(289, 255)  # button_cc_menu_general_win_x_y
        time.sleep(3)
        pa.click(516, 262)  # button_cc_menu_general_win_player_x_y
        time.sleep(3)
        pa.click(624, 454)  # button_cc_menu_general_win_player_ok_x_y

    time.sleep(28)  # Usually 15s to load winning screen + 10 for boxes
    print("Closing winning screen...")
    for c in range(4):  # Close lootboxes
        pa.click(608, 60)  # Hit exit button
        time.sleep(3)

    print("Match ended!")


try:
    # TODO Add limit of points assert
    full_start = time.time()
    assert_preload()
    pa.click(pa.locateCenterOnScreen('./resources/icon.png'))  # Open CoH2
    assert_game_setup()
    center_screen_x_y = [x / 2 for x in pa.size()]

    for i in range(amount_of_matches):
        if real_game:
            off_ce()
        print("\n=====================")
        print(f"Playing game #{i}")

        start_match_time = time.time()
        start_match()
        print(f"Start of match #{i} took {time.time() - start_match_time}s.")

        play_time = time.time()
        play()
        print(f"The game #{i} took {time.time() - play_time}s.")

        if wait_for_element("./resources/summary_close.png", 20, 4):
            pa.click(642, 677)  # Click summary exit button
        elif not debug:
            print("Could not hit summary exit button!")
            raise Exception

        time.sleep(8)  # Waiting for preparation screen to load

    print(f"Execution has ended! It took {time.time()-full_start} seconds")
except Exception as e:
    traceback.print_exc()
    print(f"Seems that something is broken: '{e}'. Pausing the game...")
    pa.press("escape")
    exit(1)
