import win32api
import win32con
import win32gui
import logging
import time
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        print(hex(hwnd), win32gui.GetWindowText(hwnd), end=' | ')


win32gui.EnumWindows(winEnumHandler, None)

# Get the handle of the window you want to send mouse events to
hwnd = win32gui.FindWindow(None, "LifeTO(EN) - Jewelia : Ruby Island [v03192023v3]")

count = 0
while True:
    count += 1
    # Set the coordinates where you want to send the mouse event (in this example, x=100, y=100)
    x, y = 100, 100

    # Convert the coordinates to screen coordinates
    screen_x, screen_y = win32gui.ClientToScreen(hwnd, (x, y))

    # Send a left mouse button down event
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON,
                         screen_y << 16 | screen_x)

    # Send a left mouse button up event
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, screen_y << 16 | screen_x)

    if count % 100 == 0:
        logging.info(f'Auto buy is running')
        logging.info(f'Bought')
    time.sleep(1)