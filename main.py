import math
import pymem
import pymem.process
import pymem.memory
import pyautogui
import pydirectinput
from getbaseaddr import *
from time import sleep
import random
import numpy as np
import threading
import multiprocessing
import os
import sys

from helper import *

process = pymem.process
mem = pymem.memory
PROCNAME = "Trickster.bin"

DMC5 = pymem.Pymem(PROCNAME)
game_handle_pymem = DMC5.process_handle
GAME_BASE_ADDRESS = get_base_address()
hwndMain = win32gui.FindWindow('xmflrtmxj', None)

MAX_COR = (3960, 3960)  # or 4000 but 3960 for check

SCREEN_RES = {
    'x': 1024,
    'y': 768
}

PLAYER_POS_ON_SCREEN_RES = [
    SCREEN_RES['x'] // 2,
    SCREEN_RES['y'] // 2
]

INSULT_WORDS = [
    'Dull',
    'Dumb',
    'Foolish',
    'Laughable',
    'Ludicrous',
]

ITEM_NAME_TO_PICKUP = [
    'Shield',
    # 'Gun',
    # 'Rod',
    # 'Staff',
    # 'Sword',
    # 'Dagger',
    # 'Broken Artifact 3: 1 number',
    'Aposis Card',
    'Mimic Card',


]

CURSOR_COOR_CORNERS = [
    (800, 700),  # player at top left
    (100, 700),  # player at top right
    (100, 100),  # player at bottom right
    (800, 100),  # player at bottom left
]

CURSOR_COOR_SIDES = [
    (800, 350),  # player at left
    (500, 700),  # player at top
    (100, 350),  # player at right
    (500, 100),  # player at bottom
]

random.choice(INSULT_WORDS)
# FORMULAS
# DEST_X = CUR_X + CURSOR_X - 504 (+-10) (based on screen resolution)
# DEST_Y = CUR_Y + CURSOR_Y - 377 (+-10) (based on screen res)
# for 3500 >= CUR_X, CUR_Y >= 500

# ------- POINTER AND OFFSET -------

# -- PLAYER'S STATS --
# These addresses are of 2 byte type
PLAYER_BASE_ADDRESS = GAME_BASE_ADDRESS + int(0x007B2E6C)
PLAYER_BASE_ADDRESS_OFFSET = [0, 0]
PLAYER_LEVEL_BASE_OFFSET = [0, 0x398]
PLAYER_NAME_OFFSET = [0, 0x3C]
PLAYER_X_OFFSET = [0, 0x6C]
PLAYER_Y_OFFSET = [0, 0x6E]
PLAYER_HP_OFFSET = [0, 0x1C4]
PLAYER_MP_OFFSET = [0, 0x1C8]
PLAYER_MAX_HP_OFFSET = [0, 0x1F0]
PLAYER_MAX_MP_OFFSET = [0, 0x1D8]
# -- END PLAYER'S STATS --


# -- MONSTERS --
MONSTER_BASE_ADDRESS = GAME_BASE_ADDRESS + int(0x007B5D1C)

# All start address at 0 offset of monster
# MONSTER_BASE_OFFSET = [[hex(i), 0] for i in range(0, 32, 4)]
# MONSTER_BASE_OFFSET = [[hex(i), 0] for i in range(0, 32, 4)]
MONSTER_BASE_OFFSET = [
    [0x0, 0],
    [0x4, 0],
    [0x8, 0],
    [0xc, 0],
    [0x10, 0],
    [0x14, 0],
    [0x18, 0],
    [0x1c, 0],
    [0x20, 0],
    [0x24, 0],
]

MONSTER_STATS_OFFSET = [
    [0, 0],  # Monster's address / ID
    [0, 0x6C],  # Monster's X coordinate
    [0, 0x6E],  # Monster's Y coordinate
    [0, 0x1C4],  # Monster's HP
    [0, 0x60],  # Monster's check if real or not
    [0, 0x3C],  # Monster's name in array of byte
    # (can be hex, can be decimal and changed to text)
]

# -- END MONSTERS --
# CURSOR_STATE_BASE = GAME_BASE_ADDRESS + int(0x0151B35C)
# CURSOR_STATE_OFFSET = [0xDF0]

CURSOR_STATE_BASE = GAME_BASE_ADDRESS + int(0x009B7484)
# CURSOR_STATE_BASE = GAME_BASE_ADDRESS + int(0x0088A4D0)
CURSOR_STATE_OFFSET = [0x4, 0x1F8]
# CURSOR_STATE_OFFSET = [0x0, 0x1C, 0x48, 0x14, 0x2C4, 0x4, 0x164]


TARGET_ID_BASE = GAME_BASE_ADDRESS + int(0x009B7484)
# TARGET_ID_BASE = GAME_BASE_ADDRESS + int(0x009B7484)
TARGET_ID_OFFSET = [0x4, 0x200]
# TARGET_ID_OFFSET = [0x0, 0x1C, 0x48, 0x14, 0x2C4, 0x4, 0x200]

MOUSE_X_BASE = GAME_BASE_ADDRESS + int(0x00994118)
MOUSE_X_OFFSET = [4]

MOUSE_Y_BASE = GAME_BASE_ADDRESS + int(0x00994118)
MOUSE_Y_OFFSET = [8]

# -- MONSTERS --
ITEM_BASE_ADDRESS = GAME_BASE_ADDRESS + int(0x007B8768)

# All start address at 0 offset of item
ITEM_BASE_OFFSET = [
    [0x0, 0],
    [0x4, 0],
    [0x8, 0],
    [0xc, 0],
    [0x10, 0],
    [0x14, 0],
    [0x18, 0],
    [0x1c, 0],
    [0x20, 0],
    [0x24, 0],
    [0x28, 0],
    [0x2C, 0],
    [0x30, 0],
]

ITEM_STATS_OFFSET = [
    [0, 0],  # Item's address / ID
    [0, 0x6C],  # Item's X coordinate
    # 64536 is invalid
    [0, 0x6E],  # Item's Y coordinate
    # 64536 is invalid
    [0, 0x60],  # Item's check if real or not
    # //65527, 65524 Dead, 65532 or 66535 or 65524 or any thing else Alive - real
    [0, 0x3C],  # Item's name in array of byte
    # (can be hex, can be decimal and changed to text)
    # //65527, 65524 Dead, 65532 or 66535 or any thing else Alive - real

]

# -- END ITEMS/DROPS --

# -- CURRENT MAP --
CURRENT_MAP_BASE = GAME_BASE_ADDRESS + 0x009C2030
CURRENT_MAP_MAX_X_OFFSET = [0xEC, 0x40, 0x94C, 0xC, 0xC74]
CURRENT_MAP_MAX_Y_OFFSET = [0xEC, 0x40, 0x94C, 0xC, 0xC78]


# -- END CURRENT MAP --


def calculate_angle(playerX, playerY, centerX=MAX_COR[0] / 2,
                    centerY=MAX_COR[1] / 2):
    diagonal_vector_1 = [playerX - centerX, playerY - centerY]
    horizontal_vector_2 = [playerX - centerX, centerY - centerY]

    unit_vector_1 = diagonal_vector_1 / np.linalg.norm(diagonal_vector_1)
    unit_vector_2 = horizontal_vector_2 / np.linalg.norm(horizontal_vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)

    return angle


class Trickster_Bot():
    def __init__(self, game_handle):
        self.handle = game_handle
        self.player_info = self.get_player_info()
        self.map_valid_monster = self.get_all_valid_monster()
        self.cursor_info = self.get_cursor_info()
        self.map_valid_item = self.get_all_valid_item()
        # self.map_info = self.get_map_info()

    def write_address(self):
        valueX = 100
        valueY = 10
        while True:
            if keyboard.is_pressed("space"):
                '''
                Parameters:	
                handle (ctypes.wintypes.HANDLE) – A handle to the process memory to be modified. The handle must have PROCESS_VM_WRITE and PROCESS_VM_OPERATION access to the process.
                address (int) – An address in the specified process to which data is written.
                value (int) – The data to be written.
                Returns:	
                If the function succeeds, the return value is nonzero.
                
                Return type:	
                bool
                
                Raise:	
                TypeError if address is not a valid intege        r
                
                Raise:	
                WinAPIError if WriteProcessMemory failed
                '''
                # X coor
                status = mem.write_int(self.handle, 460425028, valueX)
                print(status)
                # Y coor
                status = mem.write_int(self.handle, 460425032, valueY)
                print(status)

    def address_adder(self, base_address, offsets=[]):
        pointer_add = base_address
        tmp = pymem.memory.read_int(self.handle, base_address)
        if offsets:
            for offset in offsets:
                pointer_add = tmp + offset
                tmp = pymem.memory.read_int(self.handle, pointer_add)

        return pointer_add

    def get_player_info(self):
        player_x = mem.read_short(self.handle,
                                  self.address_adder(
                                      PLAYER_BASE_ADDRESS,
                                      offsets=PLAYER_X_OFFSET,
                                  )
                                  )

        player_y = mem.read_short(self.handle,
                                  self.address_adder(
                                      PLAYER_BASE_ADDRESS,
                                      offsets=PLAYER_Y_OFFSET,
                                  )
                                  )

        player_hp = mem.read_short(self.handle,
                                   self.address_adder(
                                       PLAYER_BASE_ADDRESS,
                                       offsets=PLAYER_HP_OFFSET,
                                   )
                                   )

        player_mp = mem.read_short(self.handle,
                                   self.address_adder(
                                       PLAYER_BASE_ADDRESS,
                                       offsets=PLAYER_MP_OFFSET,
                                   )
                                   )

        player_max_hp = mem.read_short(self.handle,
                                       self.address_adder(
                                           PLAYER_BASE_ADDRESS,
                                           offsets=PLAYER_MAX_HP_OFFSET,
                                       )
                                       )

        player_max_mp = mem.read_short(self.handle,
                                       self.address_adder(
                                           PLAYER_BASE_ADDRESS,
                                           offsets=PLAYER_MAX_MP_OFFSET,
                                       )
                                       )

        player_name = mem.read_bytes(self.handle,
                                     self.address_adder(
                                         PLAYER_BASE_ADDRESS,
                                         offsets=PLAYER_NAME_OFFSET),
                                     byte=20
                                     )
        player_name = player_name.split(b'\x00')[0].decode("utf-8")

        player_info = {
            'player_x': player_x,
            'player_y': player_y,
            'player_hp': player_hp,
            'player_mp': player_mp,
            'player_max_hp': player_max_hp,
            'player_max_mp': player_max_mp,
            'player_name': player_name,
        }

        self.player_info = player_info

        # print('PlayerX: ', player_x)
        # print('PlayerY: ', player_y)
        # print('Player HP: ', player_hp)
        # print('Player MP: ', player_mp)
        # print('Player MaxHP: ', player_max_hp)
        # print('Player MaxMP: ', player_max_mp)
        # print('Player Name: ', player_name)
        # print('Cursor state: ', cursor_state)
        # print('TargetID: ', hex(target_id))
        # print('Mouse X is at: ', mouse_x_value)
        # print('Mouse Y is at:', mouse_y_value)
        # print('----------------------------------------------------')
        return player_info

    def get_cursor_info(self):
        # cursor_state = mem.read_int(self.handle,
        #                             self.address_adder(
        #                                 CURSOR_STATE_BASE,
        #                                 offsets=CURSOR_STATE_OFFSET))
        cursor_state = mem.read_uint(self.handle,
                                     self.address_adder(
                                         CURSOR_STATE_BASE,
                                         offsets=CURSOR_STATE_OFFSET)
                                     )

        target_id = mem.read_uint(self.handle,
                                  self.address_adder(
                                      TARGET_ID_BASE,
                                      offsets=TARGET_ID_OFFSET)
                                  )
        # target_id = mem.read_int(self.handle, 0x0F200F70)

        mouse_x_value = mem.read_uint(self.handle,
                                      self.address_adder(
                                          MOUSE_X_BASE,
                                          offsets=MOUSE_X_OFFSET)
                                      )

        mouse_y_value = mem.read_uint(self.handle,
                                      self.address_adder(
                                          MOUSE_Y_BASE,
                                          offsets=MOUSE_Y_OFFSET)
                                      )
        cursor_info = {
            'cursor_state': cursor_state,
            # 0 = MOVEABLE,
            # 2 = ON GUI,
            # 3 = ON WALL,
            # 6 = ATTACK ON TARGET,
            # 10 = ON PORTAL,
            # 11 = ON NPC,
            # 15 = CAST SPELL,
            # 26 = CAST SPELL ON TARGET,
            'target_id': target_id,
            'mouse_x_value': mouse_x_value,
            'cursor_x': mouse_x_value,
            'mouse_y_value': mouse_y_value,
            'cursor_y': mouse_y_value,

        }
        self.cursor_info = cursor_info
        return cursor_info

    def set_cursor(self, valueX, valueY):
        # X coor
        mem.write_int(self.handle,
                      self.address_adder(MOUSE_X_BASE, MOUSE_X_OFFSET),
                      valueX)
        # Y coor
        mem.write_int(self.handle,
                      self.address_adder(MOUSE_Y_BASE, MOUSE_Y_OFFSET),
                      valueY)

    def move(self, cursor_to_move_X, cursor_to_move_Y):
        self.set_cursor(cursor_to_move_X,
                        cursor_to_move_Y)
        print(
            'Set cursor to ({},{})'.format(cursor_to_move_X, cursor_to_move_Y))
        self.set_cursor(cursor_to_move_X,
                        cursor_to_move_Y)
        sleep(1)
        mouse_click(hwndMain)
        mouse_click(hwndMain)
        sleep(4)
        print('Done moving...')

    def check_cursor_state(self, check_code):
        cursor_state = self.get_cursor_info()['cursor_state']
        if cursor_state == check_code:
            return True
        return False

    def get_all_valid_monster(self):
        map_monster_info = []
        for mbo in MONSTER_BASE_OFFSET:
            try:
                monster_base_hex = self.address_adder(
                    MONSTER_BASE_ADDRESS,
                    offsets=mbo,
                )
            except Exception as e:
                continue

            for i in range(1, 16):
                try:
                    tmp_list = [monster_base_hex + mso[1] for mso in
                                MONSTER_STATS_OFFSET]
                    monster_x = mem.read_ushort(self.handle, tmp_list[1])
                    monster_y = mem.read_ushort(self.handle, tmp_list[2])
                    monster_hp = mem.read_ushort(self.handle, tmp_list[3])
                    monster_check = mem.read_ushort(self.handle, tmp_list[4])
                    monster_name = mem.read_bytes(self.handle, tmp_list[5],
                                                  byte=20)
                    monster_name = monster_name.split(b'\x00')[0].decode(
                        "utf-8")
                    if monster_name and \
                            monster_x != 64536 and \
                            monster_check != 65527 and \
                            'Shadow' not in monster_name and \
                            monster_hp > 0:
                        valid_monster = {
                            'monster_id': hex(monster_base_hex),
                            'monster_x': monster_x,
                            'monster_y': monster_y,
                            'monster_hp': monster_hp,
                            'monster_check': monster_check,
                            'monster_name': monster_name
                        }
                        map_monster_info.append(valid_monster)
                        # print('----------------------------------------------------')
                        # print('Monster is at: ', hex(monster_base_hex))
                        # print([hex(j) for j in tmp_list])
                        # print('MonsterX: ', monster_x)
                        # print('MonsterY: ', monster_y)
                        # print('Monster HP: ', monster_hp)
                        # print('Monster Check: ', monster_check)
                        # print('Monster Name: ', monster_name)
                    monster_base_hex = monster_base_hex + 0x604
                except Exception as e:
                    # print(e)
                    continue
        self.map_valid_monster = map_monster_info
        return map_monster_info

    def get_monster_info_from_address(self, monster_base):
        tmp_list = [monster_base + i[1] for i in MONSTER_STATS_OFFSET]
        monster_x = mem.read_ushort(self.handle, tmp_list[1])
        monster_y = mem.read_ushort(self.handle, tmp_list[2])
        monster_hp = mem.read_ushort(self.handle, tmp_list[3])
        monster_check = mem.read_ushort(self.handle, tmp_list[4])
        monster_name = mem.read_bytes(self.handle, tmp_list[5], byte=20)
        monster_name = monster_name.split(b'\x00')[0].decode("utf-8")
        monster_info = [monster_x,
                        monster_y,
                        monster_hp,
                        monster_check,
                        monster_name
                        ]

        return monster_info

    def get_all_valid_item(self):
        map_item_info = []
        for ibo in ITEM_BASE_OFFSET:
            try:
                item_base_hex = self.address_adder(
                    ITEM_BASE_ADDRESS,
                    offsets=ibo,
                )
                # print(hex(item_base_hex))
            except Exception as e:
                continue

            for i in range(1, 16):
                try:
                    tmp_list = [item_base_hex + iso[1] for iso in
                                ITEM_STATS_OFFSET]
                    item_x = mem.read_ushort(self.handle, tmp_list[1])
                    item_y = mem.read_ushort(self.handle, tmp_list[2])
                    item_check = mem.read_ushort(self.handle, tmp_list[3])
                    item_name = mem.read_bytes(self.handle, tmp_list[4],
                                               byte=30)
                    item_name = item_name.split(b'\x00')[0].decode("utf-8")
                    if item_check != 65524 and item_check != 65527:
                        if item_name and item_x != 64536:
                            valid_item = {
                                'item_id': hex(item_base_hex),
                                'item_x': item_x,
                                'item_y': item_y,
                                'item_check': item_check,
                                'item_name': item_name
                            }
                            map_item_info.append(valid_item)
                    item_base_hex = item_base_hex + 0x224
                    # print(hex(item_base_hex))
                except Exception as e:
                    # print(e)
                    continue
        self.map_valid_item = map_item_info
        return map_item_info

    def get_map_info(self):

        map_max_x_address = self.address_adder(CURRENT_MAP_BASE,
                                               CURRENT_MAP_MAX_X_OFFSET)
        map_max_y_address = self.address_adder(CURRENT_MAP_BASE,
                                               CURRENT_MAP_MAX_Y_OFFSET)

        max_x = mem.read_uint(self.handle, map_max_x_address)
        max_y = mem.read_uint(self.handle, map_max_y_address)
        # print('Map Max X', max_x)
        # print('Map Max Y', max_y)

        map_info = {
            'map_max_x': max_x,
            'map_max_y': max_y,
            # 'map_max_x': ,
        }

        self.map_info = map_info

        return map_info


trickster_bot = Trickster_Bot(game_handle_pymem)


def mouse_click(hwnd_from_win32):
    lParam = win32api.MAKELONG(10, 11)
    win32api.SendMessage(hwnd_from_win32, win32con.WM_LBUTTONDOWN,
                         win32con.MK_LBUTTON, lParam)
    # win32gui.SendMessage(hwnd_from_win32, win32con.WM_LBUTTONUP, None, lParam)
    win32api.SendMessage(hwnd_from_win32, win32con.WM_LBUTTONUP, None, lParam)


def mouse_release(hwnd_from_win32):
    lParam = win32api.MAKELONG(10, 11)
    win32api.SendMessage(hwnd_from_win32, win32con.WM_RBUTTONDOWN,
                         win32con.MK_RBUTTON, lParam)
    # win32gui.SendMessage(hwnd_from_win32, win32con.WM_LBUTTONUP, None, lParam)
    win32api.SendMessage(hwnd_from_win32, win32con.WM_RBUTTONUP, None, lParam)


def main_bak():
    time_finding_monster = 0
    time_finding_monster_allotted = 20
    player_info = trickster_bot.get_player_info()
    angle = calculate_angle(player_info['player_x'], player_info['player_y'])
    print(angle)

    while True:
        cursor_info = trickster_bot.get_cursor_info()
        player_info = trickster_bot.get_player_info()
        trickster_bot.get_all_valid_monster()
        playerX, playerY = player_info[0], player_info[1]
        valid_player_X = list(range(math.floor(MAX_COR[0] * 20 / 100),
                                    math.floor(MAX_COR[0] * 80 / 100)))
        valid_player_Y = list(range(math.floor(MAX_COR[1] * 20 / 100),
                                    math.floor(MAX_COR[1] * 80 / 100)))

        valid_cursor_X = list(range(50, 800, 10))
        valid_cursor_Y = list(range(10, 700, 10))

        sleep(0.2)

        # cursor_to_move_X = min(abs(1500 - playerX + 504 + valid_cursor_X[-1]), valid_cursor_X[-1])
        # cursor_to_move_Y = min(abs(1500 - playerY + 377 + valid_cursor_Y[-1]), valid_cursor_Y[-1])

        invalid_player_pos = False
        # # Top left
        # if playerX <= valid_player_X[0] and playerY <= valid_player_Y[0]:
        #     invalid_player_pos = True
        #     cursor_to_move_X, cursor_to_move_Y = CURSOR_COOR[0][0], CURSOR_COOR[0][1]
        # # Top right
        # elif playerX >= valid_player_X[-1] and playerY <= valid_player_Y[0]:
        #     invalid_player_pos = True
        #     cursor_to_move_X, cursor_to_move_Y = CURSOR_COOR[1][0], CURSOR_COOR[1][1]
        #
        # # Bottom right
        # elif playerX >= valid_player_X[-1] and playerY >= valid_player_Y[-1]:
        #     invalid_player_pos = True
        #     cursor_to_move_X, cursor_to_move_Y = CURSOR_COOR[2][0], CURSOR_COOR[2][1]
        #
        # # Bottom left
        # elif playerX <= valid_player_X[0] and playerY >= valid_player_Y[-1]:
        #     invalid_player_pos = True
        #     cursor_to_move_X, cursor_to_move_Y = CURSOR_COOR[3][0], CURSOR_COOR[3][1]

        # LEFT
        if playerX < valid_player_X[0]:
            print('At left, moving right')
            cursor_to_move_X, cursor_to_move_Y = CURSOR_COOR_SIDES[0][0], \
                                                 CURSOR_COOR_SIDES[0][1]
            trickster_bot.move(cursor_to_move_X, cursor_to_move_Y)

        # TOP
        if playerY < valid_player_Y[0]:
            print('At top, moving down')
            cursor_to_move_X, cursor_to_move_Y = CURSOR_COOR_SIDES[1][0], \
                                                 CURSOR_COOR_SIDES[1][1]
            trickster_bot.move(cursor_to_move_X, cursor_to_move_Y)

        # RIGHT
        if playerX > valid_player_X[-1]:
            print('At right, moving left')
            cursor_to_move_X, cursor_to_move_Y = CURSOR_COOR_SIDES[2][0], \
                                                 CURSOR_COOR_SIDES[2][1]
            trickster_bot.move(cursor_to_move_X, cursor_to_move_Y)

        # BOTTOM
        if playerY > valid_player_Y[-1]:
            print('At bottom, moving up')
            cursor_to_move_X, cursor_to_move_Y = CURSOR_COOR_SIDES[3][0], \
                                                 CURSOR_COOR_SIDES[3][1]
            trickster_bot.move(cursor_to_move_X, cursor_to_move_Y)

        try:
            if time_finding_monster >= time_finding_monster_allotted:
                time_finding_monster = 0
                tmp = random.choice(CURSOR_COOR_SIDES)
                cursor_to_move_X, cursor_to_move_Y = tmp[0], tmp[1]
                trickster_bot.move(cursor_to_move_X, cursor_to_move_Y)

            time_finding_monster += 5
            # player_info = [
            #     player_x,
            #     player_y,
            #     player_hp,
            #     player_mp,
            #     player_max_hp,
            #     player_max_mp,
            #     player_name,
            # ]

            if int(player_info['player_mp']) < int(
                    player_info['player_max_mp'] * 80 / 100):
                drink_potion('num5')

            player_info = trickster_bot.get_player_info()
            if int(player_info['player_mp']) < int(
                    player_info['player_max_mp'] * 80 / 100):
                drink_potion('num5')

            if int(player_info['player_hp']) < int(
                    player_info['player_max_hp'] * 80 / 100):
                drink_potion('num6')

            aoe_used = False
            found_monster = False
            use_skill('num1')
            for x in valid_cursor_X:
                for y in valid_cursor_Y:
                    trickster_bot.set_cursor(x, y)
                    # if trickster_bot.get_cursor_info()[0] == 26:
                    #     mouse_click(hwndMain)
                    #
                    # if trickster_bot.get_cursor_info()[0] == 6:
                    #     use_skill('num3')
                    #     mouse_click(hwndMain)
                    #     aoe_used = True
                    #     found_monster = True
                    #     time.sleep(6)
                    #     use_skill('num1')
                    #     for i in range(5):
                    #         pickup()

                    if trickster_bot.get_cursor_info()['cursor_state'] == 10:
                        tmp = random.choice(CURSOR_COOR_SIDES)
                        cursor_to_move_X, cursor_to_move_Y = tmp[0], tmp[1]
                        trickster_bot.move(cursor_to_move_X, cursor_to_move_Y)

                    elif trickster_bot.get_cursor_info()['cursor_state'] == 26:
                        current_target = trickster_bot.get_cursor_info()[1]
                        monster_info = trickster_bot.get_monster_info_from_address(
                            current_target)
                        if 'Punisher' in monster_info[-1]:
                            continue
                        mouse_click(hwndMain)
                        print('Attacking' + ' ' +
                              random.choice(INSULT_WORDS) + ' ' +
                              monster_info[-1])
                        sleep(3)
                        # trickster_bot.set_cursor(x, y)
                        # use_skill('num3')
                        # mouse_click(hwndMain)
                        found_monster = True
                        for i in range(5):
                            # pickup()
                            pick_up_valid_X = list(
                                range(500 - 200, 500 + 200, 5))
                            pick_up_valid_Y = list(
                                range(380 - 100, 380 + 100, 5))
                            for x_drop in pick_up_valid_X:
                                for y_drop in pick_up_valid_Y:
                                    trickster_bot.set_cursor(x_drop, y_drop)
                                    if trickster_bot.get_cursor_info()[0] == 4:
                                        mouse_click(hwndMain)
                                        sleep(2)
                        break

                        # time_elapsed = 0
                        # time_allotted = 15
                        # while True:
                        #     time.sleep(2)
                        #     time_elapsed += 2
                        #     if time_elapsed > time_allotted:
                        #         break
                        #     monster_info = trickster_bot.get_monster_info_from_address(current_target)
                        #     if monster_info[-2] == 65527 or \
                        #             playerX == trickster_bot.get_player_info()[0]:
                        #         break

                        #

                if found_monster:
                    time_finding_monster = 0
                    break

        except Exception as e:
            print(e)
            print('Exception, moving on...')


def main(center_param):
    heal_mana('f5', 80)
    heal_hp('f6', 80)
    while pickup_by_name('Blue Potion A: 1 number'):
        sleep(1)
        continue

    attack_aoe('f3')

    radius = 500

    attack('f1', center_param, radius)
    attack('f1', center_param, radius)
    attack('f1', center_param, radius)


def attack(skill_slot, center, radius):
    print('Attack now')
    player_info = trickster_bot.get_player_info()
    all_monster = trickster_bot.get_all_valid_monster()
    monster_found = False
    # valueX, valueY = 10, 10
    # all_monster = sorted(all_monster, key=lambda d: d['monster_x'])
    # print('---- attack ----')
    near_all_monster = []
    visible_all_monster = []
    for i in range(len(all_monster)):
        if all_monster[i]['monster_x'] in range(player_info['player_x'] -
                                                100,
                                                player_info['player_y'] + 100):
            near_all_monster.append(all_monster[i])

    for i in range(len(all_monster)):
        # if all_monster[i]['monster_x'] in range(player_info['player_x'] - 500, player_info['player_x'] + 500):
        if all_monster[i]['monster_x'] in range(center[0] -
                                                radius, center[1] + radius):
            visible_all_monster.append(all_monster[i])

    if near_all_monster:
        all_monster = near_all_monster
    elif visible_all_monster:
        all_monster = visible_all_monster
    else:
        all_monster = all_monster

    for i in range(len(all_monster)):
        cursorX = all_monster[i]['monster_x'] - player_info['player_x'] + (
                SCREEN_RES['x'] // 2 - 10)
        cursorY = all_monster[i]['monster_y'] - player_info['player_y'] + (
                SCREEN_RES['y'] // 2 - 10)
        monster_x = all_monster[i]['monster_x']
        monster_y = all_monster[i]['monster_y']
        # print(all_monster[i])
        if (cursorX in range(50, 950)) and (cursorY in range(100, 700)):
            print('Set cursor to ({},{})'.format(cursorX, cursorY))
            use_skill(skill_slot)
            trickster_bot.set_cursor(cursorX, cursorY)
            sleep(0.5)
            # print(trickster_bot.get_cursor_info())
            monster_found = True
            if trickster_bot.check_cursor_state(26):
                sleep(0.5)
                mouse_click(hwndMain)
                print('Attacking' + ' ' +
                      random.choice(INSULT_WORDS) + ' ' +
                      all_monster[i]['monster_name']
                      )
                return 200

    if not monster_found:
        #
        if cursorX > 950:
            cursorX = 950
            cursorY = math.floor((cursorX - player_info['player_x']) *
                                 (monster_y - player_info['player_y']) /
                                 (monster_x - player_info['player_x'])) + \
                      player_info['player_y']

        elif cursorX < 50:
            cursorX = 50
            cursorY = math.floor((cursorX - player_info['player_x']) *
                                 (monster_y - player_info['player_y']) /
                                 (monster_x - player_info['player_x'])) + \
                      player_info['player_y']

        if cursorY > 700:
            cursorY = 700
            cursorX = math.floor((cursorY - player_info['player_y']) *
                                 (monster_x - player_info['player_x']) /
                                 (monster_y - player_info['player_y'])) + \
                      player_info['player_x']

        elif cursorY < 100:
            cursorY = 100
            cursorX = math.floor((cursorY - player_info['player_y']) *
                                 (monster_x - player_info['player_x']) /
                                 (monster_y - player_info['player_y'])) + \
                      player_info['player_x']

        cursorX = 700 if cursorX > 700 else cursorX
        cursorX = 100 if cursorX < 100 else cursorX

        cursorY = 700 if cursorY > 700 else cursorY
        cursorY = 100 if cursorY < 100 else cursorY

        print('Monster out of range')
        print('Set cursor to ({},{})'.format(cursorX, cursorY))
        trickster_bot.set_cursor(cursorX, cursorY)
        sleep(0.5)
        mouse_click(hwndMain)
    return 0


def attack_aoe(skill_slot):
    player_info = trickster_bot.get_player_info()
    all_monster = trickster_bot.get_all_valid_monster()
    monster_found = False
    # valueX, valueY = 10, 10
    # all_monster = sorted(all_monster, key=lambda d: d['monster_x'])
    # print('---- attack ----')
    near_all_monster = []
    visible_all_monster = []
    for i in range(len(all_monster)):
        if all_monster[i]['monster_x'] in range(player_info['player_x'] - 100,
                                                player_info['player_x'] + 100) \
                and all_monster[i]['monster_y'] in range(
            player_info['player_y'] - 100, player_info['player_y'] + 100):
            near_all_monster.append(all_monster[i])

    for i in range(len(all_monster)):
        if all_monster[i]['monster_x'] in range(player_info['player_x'] - 500,
                                                player_info['player_x'] + 500) \
                and all_monster[i]['monster_y'] in range(
            player_info['player_y'] - 300, player_info['player_y'] + 300):
            visible_all_monster.append(all_monster[i])

    if near_all_monster:
        all_monster = near_all_monster
    elif visible_all_monster:
        all_monster = visible_all_monster
    else:
        all_monster = all_monster

    # [print(i) for i in all_monster]

    for i in range(len(all_monster)):
        cursorX = all_monster[i]['monster_x'] - player_info['player_x'] + (
                SCREEN_RES['x'] // 2 - 10)
        cursorY = all_monster[i]['monster_y'] - player_info['player_y'] + (
                SCREEN_RES['y'] // 2 - 10)
        monster_x = all_monster[i]['monster_x']
        monster_y = all_monster[i]['monster_y']
        # print(all_monster[i])
        if (cursorX in range(50, 950)) and (cursorY in range(100, 700)):
            mouse_release(hwndMain)
            print('Set cursor to ({},{})'.format(cursorX, cursorY))
            trickster_bot.set_cursor(cursorX, cursorY)
            print('Attack AOE now')
            sleep(0.5)
            # print(trickster_bot.get_cursor_info())
            monster_found = True
            if trickster_bot.check_cursor_state(6):
                use_skill(skill_slot)
                mouse_click(hwndMain)
                print('Attacking' + ' ' +
                      random.choice(INSULT_WORDS) + ' ' +
                      all_monster[i]['monster_name']
                      )
                return 200

    if not monster_found:
        #
        if cursorX > 950:
            cursorX = 950
            cursorY = math.floor((cursorX - player_info['player_x']) *
                                 (monster_y - player_info['player_y']) /
                                 (monster_x - player_info['player_x'])) + \
                      player_info['player_y']

        elif cursorX < 50:
            cursorX = 50
            cursorY = math.floor((cursorX - player_info['player_x']) *
                                 (monster_y - player_info['player_y']) /
                                 (monster_x - player_info['player_x'])) + \
                      player_info['player_y']

        if cursorY > 700:
            cursorY = 700
            cursorX = math.floor((cursorY - player_info['player_y']) *
                                 (monster_x - player_info['player_x']) /
                                 (monster_y - player_info['player_y'])) + \
                      player_info['player_x']

        elif cursorY < 100:
            cursorY = 100
            cursorX = math.floor((cursorY - player_info['player_y']) *
                                 (monster_x - player_info['player_x']) /
                                 (monster_y - player_info['player_y'])) + \
                      player_info['player_x']

        cursorX = 700 if cursorX > 700 else cursorX
        cursorX = 100 if cursorX < 100 else cursorX

        cursorY = 700 if cursorY > 700 else cursorY
        cursorY = 100 if cursorY < 100 else cursorY

        print('Monster out of range')
        print('Set cursor to ({},{})'.format(cursorX, cursorY))
        trickster_bot.set_cursor(cursorX, cursorY)
        sleep(0.5)
        mouse_click(hwndMain)
    return 0


def pickup_by_name(name='not_necessary'):
    player_info = trickster_bot.get_player_info()
    all_item = trickster_bot.get_all_valid_item()

    for i in range(len(all_item)):
        valueX = all_item[i]['item_x'] - player_info['player_x'] + (
                SCREEN_RES['x'] // 2 - 10)
        valueY = all_item[i]['item_y'] - player_info['player_y'] + (
                SCREEN_RES['y'] // 2 - 10)
        # print(all_item[i])
        if (valueX in range(50, 1000)) and \
                (valueY in range(100, 700)) and \
                (any([True for item in ITEM_NAME_TO_PICKUP if
                      item in all_item[i]['item_name']])):
            mouse_release(hwndMain)
            print('Set cursor to ({},{})'.format(valueX, valueY))
            trickster_bot.set_cursor(valueX, valueY)
            sleep(0.5)
            if trickster_bot.check_cursor_state(4):
                mouse_click(hwndMain)
                logging.info('Picking up one' +
                             ' ' +
                             all_item[i]['item_name']
                             )
                return 200
    sleep(1)
    return 0


def quit_program():
    global is_quit
    is_quit = True


def pickup():
    pyautogui.press('num0')
    sleep(0.5)


def use_skill(key):
    pydirectinput.press(key)
    sleep(0.5)


def drink_potion(key):
    pydirectinput.press(key)
    sleep(0.5)


def heal_mana(key, percentage: int):
    while True:
        player_info = trickster_bot.get_player_info()
        if int(player_info['player_mp']) < int(
                player_info['player_max_mp'] * percentage / 100):
            drink_potion(key)
        else:
            break


def heal_hp(key, percentage: int):
    while True:
        player_info = trickster_bot.get_player_info()
        if int(player_info['player_hp']) < int(
                player_info['player_max_hp'] * percentage / 100):
            drink_potion(key)
        else:
            break


def test1():
    print('----- Test 1 -----')
    original_addressses = [
        0x2E6586DC
    ]

    address_value_pair = {}
    value_to_find = 3480

    for addr in original_addressses:
        start = addr - 0x50000
        for i in range(0, 0x100000, 2):
            # print(hex(start + i), '----', hex(mem.read_uint(trickster_bot.handle, start + i)))
            # print(mem.read_ushort(trickster_bot.handle, start + i))
            try:
                address_value = mem.read_ushort(trickster_bot.handle,
                                                start + i)
                # print('Address value: ', address_value)
                address_value_pair[hex(start + i)] = address_value
                if address_value == value_to_find:
                    print(hex(addr) + '----' + hex(start + i) + '----' + str(
                        address_value))
                    print('Difference: ' + hex(abs(start + i - addr)))
                # map_name = mem.read_bytes(trickster_bot.handle, start + i, byte=40)
                # map_name = map_name.split(b'\x00')[0].decode("utf-8")
                # print(map_name)
            except Exception as e:
                # print(e)
                continue
    for address, value in address_value_pair.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if value_to_find == value:
            print(address, '----', value)


def test2():
    print('---- Test 2 ----')
    for i in trickster_bot.get_all_valid_item():
        print(i)
    return


def test3():
    print('---- Test 3 ----')
    player_info = trickster_bot.get_player_info()
    all_monster = trickster_bot.get_all_valid_monster()

    for i in range(len(all_monster)):
        valueX = all_monster[i]['monster_x'] - player_info['player_x'] + (
                SCREEN_RES['x'] // 2 - 10)
        valueY = all_monster[i]['monster_y'] - player_info['player_y'] + (
                SCREEN_RES['y'] // 2 - 10)
        print(all_monster[i])
        if (valueX in range(200, 1000)) and (valueY in range(100, 700)):
            print('Set cursor to ({},{})'.format(valueX, valueY))
            use_skill('num1')
            trickster_bot.set_cursor(valueX, valueY)
            sleep(0.5)
            mouse_click(hwndMain)
            break
    sleep(2)
    return


def test4():
    print('---- Test 4 ----')
    player_info = trickster_bot.get_player_info()
    all_item = trickster_bot.get_all_valid_item()

    for i in range(len(all_item)):
        valueX = all_item[i]['item_x'] - player_info['player_x'] + (
                SCREEN_RES['x'] // 2 - 10)
        valueY = all_item[i]['item_y'] - player_info['player_y'] + (
                SCREEN_RES['y'] // 2 - 10)
        if (valueX in range(200, 1000)) and \
                (valueY in range(100, 700)) and \
                'Card' in all_item[i]['item_name']:
            print('Set cursor to ({},{})'.format(valueX, valueY))
            trickster_bot.set_cursor(valueX, valueY)
            sleep(0.5)
            mouse_click(hwndMain)
            break
    sleep(1)
    return


def test_threading(q):
    q.put(trickster_bot.get_all_valid_item())
    q.put(trickster_bot.get_all_valid_monster())


def test5():
    print('----- Test 5 -----')

    address_value_pair = {}
    map_max_x_address = trickster_bot.address_adder(CURRENT_MAP_BASE,
                                                    CURRENT_MAP_MAX_X_OFFSET)
    map_max_y_address = trickster_bot.address_adder(CURRENT_MAP_BASE,
                                                    CURRENT_MAP_MAX_Y_OFFSET)
    start = map_max_x_address - 0x100000
    print('Map Max X', mem.read_uint(trickster_bot.handle, map_max_x_address))
    print('Map Max Y', mem.read_uint(trickster_bot.handle, map_max_y_address))
    for i in range(0, 0x200000, 2):
        # print(hex(start + i), '----', hex(mem.read_uint(trickster_bot.handle, start + i)))
        # print(mem.read_ushort(trickster_bot.handle, start + i))
        try:
            address_value = mem.read_ushort(trickster_bot.handle, start + i)
            # print('Address value: ', address_value)
            map_name = mem.read_bytes(trickster_bot.handle, start + i, byte=40)
            map_name = map_name.decode("utf-8")
            # map_name = map_name.split(b'\x00')[0].decode("utf-8")
            address_value_pair[hex(start + i)] = map_name

            # print(map_name)
        except Exception as e:
            # print(e)
            continue

    for address, value in address_value_pair.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if 'S' in value:
            print(address, '----', value)


if __name__ == '__main__':
    # name = "Skyler"
    # queue = multiprocessing.Queue()
    #
    # while True:
    #     print("in main thread id(q) is {}".format(id(queue)))
    #     pro = multiprocessing.Process(target=test, args=(queue, ))
    #     pro.start()
    #     print(queue.get())
    #     sleep(4)
    #     pro.join()

    global is_quit
    is_quit = False
    center = (trickster_bot.get_player_info()['player_x'],
              trickster_bot.get_player_info()['player_y'])
    while True:
        try:
            if not is_quit:
                # all_item = trickster_bot.get_all_valid_item()
                # print(all_item)
                pickup_by_name('Broken Artifact 3: 1 number')
                sleep(1)
            else:
                sys.exit(0)
        except Exception as e:
            print(e)
            continue
