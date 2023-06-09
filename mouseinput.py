import win32api
import win32con
import win32gui
import logging
import time
import ctypes

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def _mouseinput():
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            print(hex(hwnd), win32gui.GetWindowText(hwnd), end=' | ')

    win32gui.EnumWindows(winEnumHandler, None)

    # Get the handle of the window you want to send mouse events to
    hwnd = win32gui.FindWindow(None,
                               "LifeTO(EN) - Jewelia : Ruby Island [v03192023v3]")

    count = 0
    while True:
        count += 1
        # Set the coordinates where you want to send the mouse event (in this example, x=100, y=100)
        x, y = 100, 100

        # Convert the coordinates to screen coordinates
        screen_x, screen_y = win32gui.ClientToScreen(hwnd, (x, y))

        # Send a left mouse button down event
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN,
                             win32con.MK_LBUTTON,
                             screen_y << 16 | screen_x)

        # Send a left mouse button up event
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0,
                             screen_y << 16 | screen_x)

        if count % 100 == 0:
            logging.info(f'Auto buy is running')
            logging.info(f'Bought')
        time.sleep(1)


def keyboard_input():
    # Define key codes
    VK_F5 = 0x74

    # Find the handle of the window by window class name
    hwnd = win32gui.FindWindow('xmflrtmxj', None)

    # Define a KEYBDINPUT structure
    class KEYBDINPUT(ctypes.Structure):
        _fields_ = [("wVk", ctypes.c_ushort),
                    ("wScan", ctypes.c_ushort),
                    ("dwFlags", ctypes.c_ulong),
                    ("time", ctypes.c_ulong),
                    ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

    # Define the key down and key up events
    keydown = KEYBDINPUT(VK_F5, 0,
                         win32con.KEYEVENTF_EXTENDEDKEY,
                         0, None)
    keyup = KEYBDINPUT(VK_F5, 0,
                       win32con.KEYEVENTF_EXTENDEDKEY,
                       0, None)

    # Define an INPUT structure for the key events
    class INPUT(ctypes.Structure):
        _fields_ = [("type", ctypes.c_ulong),
                    ("ki", KEYBDINPUT)]

    # Send the key down and key up events using SendInput
    inputs = (INPUT(win32con.INPUT_KEYBOARD, keydown),
              INPUT(win32con.INPUT_KEYBOARD, keyup))
    win32api.SendInput(len(inputs), ctypes.byref(inputs),
                       ctypes.sizeof(inputs[0]))

    # Wait for a brief moment before sending the next keystroke
    time.sleep(0.1)

    # Send the 'B' key to the same window
    keydown = KEYBDINPUT(0x42, 0,
                         win32con.KEYEVENTF_EXTENDEDKEY,
                         0, None)
    keyup = KEYBDINPUT(0x42, 0,
                       win32con.KEYEVENTF_EXTENDEDKEY,
                       0, None)
    inputs = (INPUT(win32con.INPUT_KEYBOARD, keydown),
              INPUT(win32con.INPUT_KEYBOARD, keyup))
    win32api.SendInput(len(inputs), ctypes.byref(inputs),
                       ctypes.sizeof(inputs[0]))

keyboard_input()