from getbaseaddr import *
import time
from scipy.optimize import fsolve
import logging
from itertools import product

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


# 0x00A94B0C - general npc
# Buy/Sell button = (x1, y1) = (x0 - 120, y0)
# Use | Equip | Drill | Pet | Card | Etc =
# [x0 - 320, Use
# x0 - 280, Equip
# x0 - 250, Drill
# x0 - 220, Pet
# x0 - 190, Card
# x0 - 160, Etc] , y0 - 371
