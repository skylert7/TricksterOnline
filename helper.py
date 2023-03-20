from getbaseaddr import *
import time
from scipy.optimize import fsolve
import logging

logging.basicConfig(level=logging.INFO,
                    filename='log.txt',
                    filemode='a',
                    format='%(asctime)s.%(msecs)03d: %(message)s',
                    datefmt='%H:%M:%S')

max_cor = (3960, 3960)  # or 4000 but 3960 for check

# DWORD MonsterCheckIsRealOffset[2] = {0x0, 0x60}; // 65527 Dead, 65532 or 66535 or any thing else Alive - real

# Cursor state
# 0 = MOVEABLE, 2 = ON GUI,
# 3 = ON WALL, 4 = ON DROP (ITEM)
# 6 = ATTACK ON TARGET,
# 10 = ON PORTAL, 11 = ON NPC,
# 15 = CAST SPELL, 26 = CAST SPELL ON TARGET

# DWORD MonsterIDOffset[2] = { 0x0,0x0 };
# //Monster X and Y position in List Offsets
# DWORD MonsterXPosOffset[2] = { 0x0,0x6C };
# DWORD MonsterYPosOffset[2] = { 0x0,0x6E };
# //Monster Health value in List Offsets
# DWORD MonsterHPBaseOffset[2] = { 0x0,0x1C4 };
# //Monster Deal or Alive value in List Offsets
# DWORD MonsterCheckIsRealOffset[2] = { 0x0,0x60 };
# //65527 Dead, 512 Alive-real
# //65527 Dead, 65532 or 66535 or 65524 or any thing else Alive - real
# //Monster Name in List Offsets DWORD
# MonsterNameArrayOneoffset[2] = { 0x0,0x3c };
# Monster addresses increment of 604
mon_dict = {
    'monsterX': 0,
    'monsterY': 0,
    'monsterHP': 0,
    'isAliveOrDead': 0,
    'monsterName': 0,  # bytearray to string or whatever
}

MONSTER_INFO = [mon_dict]


def press_key_board():
    while True:
        if keyboard.is_pressed("p"):
            logging('You pressed p')
            print("You pressed p")


def attach_to_game():
    wantedClass = 'xmflrtmxj'
    hwnd = win32gui.FindWindow(wantedClass, None)
    child_handles = []

    def all_ok(hwnd, param):
        child_handles.append(hwnd)

    win32gui.EnumChildWindows(hwnd, all_ok, None)
    print(child_handles)
    game_pid = 0
    # Locate Window
    if hwnd:
        print(hwnd)
        print('Attached to game')
        game_pid = win32process.GetWindowThreadProcessId(hwnd)
        print('PID:', game_pid[1])
    else:
        print('Can\'t find LifeTO instance')


def send_keys_unfocused():
    hwndMain = win32gui.FindWindow('xmflrtmxj', None)
    tx, ty = 50, 50

    while (True):
        # [hwndChild] this is the Unique ID of the sub/child application/proccess
        # [win32con.WM_CHAR] This sets what PostMessage Expects for input theres KeyDown and KeyUp as well
        # [0x44] hex code for D
        # [0]No clue, good luck!
        # temp = win32api.PostMessage(hwndChild, win32con.WM_CHAR, 0x44, 0) returns key sent
        lParam = win32api.MAKELONG(10, 300)
        win32api.PostMessage(hwndMain, win32con.WM_LBUTTONDOWN,
                             win32con.MK_LBUTTON, lParam)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(tx), int(ty), 0, 0)
        time.sleep(3)
        print('Clicked')


def set_game_cursor(x, y):
    return


def PostMessage_win32():
    # This works
    GAME_BASE_ADDRESS = get_base_address()
    hwndMain = win32gui.FindWindow('xmflrtmxj', None)
    lParam = win32api.MAKELONG(10, 11)
    win32api.PostMessage(hwndMain, win32con.WM_KEYDOWN, 0x32, 0)
    # win32gui.SendMessage(hwnd_from_win32, win32con.WM_LBUTTONUP, None, lParam)
    win32api.PostMessage(hwndMain, win32con.WM_KEYUP, 0, 0)
    return


def SendMessage_win32():
    GAME_BASE_ADDRESS = get_base_address()
    hwndMain = win32gui.FindWindow('xmflrtmxj', None)
    lParam = win32api.MAKELONG(10, 11)
    win32api.SendMessage(hwndMain, win32con.WM_KEYDOWN, 0x74, lParam)
    # win32gui.SendMessage(hwnd_from_win32, win32con.WM_LBUTTONUP, None, lParam)
    win32api.SendMessage(hwndMain, win32con.WM_KEYUP, None, lParam)
    return
    # hwndMain = attach_to_game()
# send_keys_unfocused()
# test_ctypes()
# set_game_cursor(100, 100)
# to_bot = Trickster_Bot()
    return
