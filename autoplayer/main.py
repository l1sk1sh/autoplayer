import psutil
import pyautogui as pa
import platform
# import win32gui

required_processes = ["Finder", "Mail", "iTerm2"]

# Asserts
if platform.system() != "Darwin":  # TODO Change to Windows
    print("Current script is designed for Windows only.")
    exit(1)

local_processes = [p.name() for p in psutil.process_iter()]
if not all(process in local_processes for process in required_processes):
    print("Seems that one of the required programs is not launched.")
    exit(1)

# pygetwindow
# window = win32gui.GetForegroundWindow()
# if win32gui.GetWindowText(window) != "Company of Heroes 2":
#     print("Currently active window is not Company of Heroes 2")
#     exit(1)

screen_width, screen_height = pa.size()
current_mouse_x, current_mouse_y = pa.position()

# use tweening/easing function to move mouse over 2 seconds.
# pa.moveTo(500, 500, duration=2, tween=pa.easeInOutQuad)
# pa.typewrite('Hello world!', interval=0.25)  # type with quarter-second pause in between each key

discord_button = pa.locateOnScreen('./resources/chrome_icon.png', grayscale=False, confidence=0.98)
print(discord_button)
pa.screenshot('my.png', region=(discord_button.left, discord_button.top, discord_button.width, discord_button.height))

pa.click(discord_button.left, discord_button.top)
