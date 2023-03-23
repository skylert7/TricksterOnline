import math
import pymem
import pymem.process
import pymem.memory
import pyautogui
import ctypes
from time import sleep
import random
import numpy as np
import os
import sys

from Trickster_Bot import *
from helper import *

process = pymem.process
mem = pymem.memory
PROCNAME = "Trickster.bin"

DMC5 = pymem.Pymem(PROCNAME)
game_handle_pymem = DMC5.process_handle
hwndMain = win32gui.FindWindow('xmflrtmxj', None)
# Get the handle of the window you want to send mouse events to
hwndSendMouseEventsTo = win32gui.FindWindow(None, "LifeTO")

trickster_bot = Trickster_Bot(game_handle_pymem)


def calculate_angle(playerX, playerY, centerX=MAX_COR[0] / 2,
                    centerY=MAX_COR[1] / 2):
    diagonal_vector_1 = [playerX - centerX, playerY - centerY]
    horizontal_vector_2 = [playerX - centerX, centerY - centerY]

    unit_vector_1 = diagonal_vector_1 / np.linalg.norm(diagonal_vector_1)
    unit_vector_2 = horizontal_vector_2 / np.linalg.norm(horizontal_vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)

    return angle


def mouse_click(hwndParam=''):
    global hwndMain
    x, y = 100, 100

    # Convert the coordinates to screen coordinates
    screen_x, screen_y = win32gui.ClientToScreen(hwndMain, (x, y))

    # Send a left mouse button down event
    win32api.SendMessage(hwndMain, win32con.WM_LBUTTONDOWN,
                         win32con.MK_LBUTTON,
                         screen_y << 16 | screen_x)

    # Send a left mouse button up event
    win32api.SendMessage(hwndMain, win32con.WM_LBUTTONUP, 0,
                         screen_y << 16 | screen_x)


def doubleClick(x=0, y=0):
    global hwndMain
    x, y = 100, 100

    # Convert the coordinates to screen coordinates
    screen_x, screen_y = win32gui.ClientToScreen(hwndMain, (x, y))

    # According to MSDN documentation The correct order of messages you will see
    # for double click event are -
    # WM_LBUTTONDOWN, WM_LBUTTONUP, WM_LBUTTONDBLCLK, and WM_LBUTTONUP

    # WM_LBUTTONDOWN
    win32api.SendMessage(hwndMain, win32con.WM_LBUTTONDOWN,
                         win32con.MK_LBUTTON,
                         screen_y << 16 | screen_x)

    # WM_LBUTTONUP
    win32api.SendMessage(hwndMain, win32con.WM_LBUTTONUP,
                         win32con.MK_LBUTTON,
                         screen_y << 16 | screen_x)

    # WM_LBUTTONDBLCLK
    win32api.SendMessage(hwndMain, win32con.WM_LBUTTONDBLCLK,
                         win32con.MK_LBUTTON,
                         screen_y << 16 | screen_x)

    # Send a left mouse button up event
    win32api.SendMessage(hwndMain, win32con.WM_LBUTTONUP, 0,
                         screen_y << 16 | screen_x)


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
        valid_player_X = list(range(math.floor(MAX_COR[0] * 30 / 100),
                                    math.floor(MAX_COR[0] * 70 / 100)))
        valid_player_Y = list(range(math.floor(MAX_COR[1] * 30 / 100),
                                    math.floor(MAX_COR[1] * 70 / 100)))

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
            player_info = trickster_bot.get_player_info()

            use_skill('1')
            for x in valid_cursor_X:
                for y in valid_cursor_Y:
                    trickster_bot.set_cursor(x, y)

                    if trickster_bot.get_cursor_info()['cursor_state'] == 10:
                        tmp = random.choice(CURSOR_COOR_SIDES)
                        cursor_to_move_X, cursor_to_move_Y = tmp[0], tmp[1]
                        trickster_bot.move(cursor_to_move_X, cursor_to_move_Y)

                    elif trickster_bot.get_cursor_info()['cursor_state'] == 26:
                        current_target = trickster_bot.get_cursor_info()[1]
                        monster_info = trickster_bot.get_monster_info_from_address(
                            current_target)
                        mouse_click(hwndMain)
                        print('Attacking' + ' ' +
                              random.choice(INSULT_WORDS) + ' ' +
                              monster_info[-1])
                        sleep(2)
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


def attack(skill_slot, centerparam, radius):
    print('Attack now')
    player_info = trickster_bot.get_player_info()
    all_monster = trickster_bot.get_all_valid_monster()
    monster_found = False
    playerX, playerY = player_info['player_x'], player_info['player_y']
    valid_player_X = list(range(math.floor(MAX_COR[0] * 30 / 100),
                                math.floor(MAX_COR[0] * 70 / 100)))
    valid_player_Y = list(range(math.floor(MAX_COR[1] * 30 / 100),
                                math.floor(MAX_COR[1] * 70 / 100)))

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
        if all_monster[i]['monster_x'] in range(centerparam[0] -
                                                radius,
                                                centerparam[1] + radius):
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
            use_skill(skill_slot)
            print('Set cursor to ({},{})'.format(cursorX, cursorY))
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
                # mouse_doucleclick(hwndMain)
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


def use_skill(key):
    x0, y0 = trickster_bot.get_skill_slot_coord()
    skill_slot_x = [x0, x0 + 32]
    skill_slot_y = [y0 + i * 32 for i in range(4)]
    skill_slot_coords = [(x, y) for y in skill_slot_y for x in skill_slot_x]
    skill_slot_lookup = {}
    for i in range(1, 9):
        skill_slot_lookup[i] = skill_slot_coords[i - 1]
        skill_slot_lookup[str(i)] = skill_slot_coords[i - 1]

    trickster_bot.set_cursor(skill_slot_lookup[key][0],
                             skill_slot_lookup[key][1])

    print(f'Use skill {key}')
    doubleClick(skill_slot_lookup[key][0], skill_slot_lookup[key][1])
    doubleClick(skill_slot_lookup[key][0], skill_slot_lookup[key][1])
    time.sleep(1)


def drink_potion(key):
    x0, y0 = trickster_bot.get_skill_slot_coord()
    skill_slot_x = [x0, x0 + 32]
    skill_slot_y = [y0 + i * 32 for i in range(4)]
    skill_slot_coords = [(x, y) for y in skill_slot_y for x in skill_slot_x]
    skill_slot_lookup = {}
    for i in range(1, 9):
        skill_slot_lookup[i] = skill_slot_coords[i - 1]
        skill_slot_lookup[str(i)] = skill_slot_coords[i - 1]

    trickster_bot.set_cursor(skill_slot_lookup[key][0],
                             skill_slot_lookup[key][1])

    print(f'Drink potion at {key}')
    doubleClick(skill_slot_lookup[key][0], skill_slot_lookup[key][1])
    doubleClick(skill_slot_lookup[key][0], skill_slot_lookup[key][1])
    time.sleep(1)


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


def test6_buy_pink_potionA_one_by_one():
    print('----- Test 6 -----')

    def winEnumHandler(myhwnd, ctx):
        if win32gui.IsWindowVisible(myhwnd):
            print(hex(myhwnd), win32gui.GetWindowText(myhwnd), end=' | ')

    win32gui.EnumWindows(winEnumHandler, None)

    count = 0
    while True:
        # Set pink potion to One

        trickster_bot.set_potionA_buy_amount_to_one()

        # Set cursor to 'Buy'
        buy_pos = (481, 548)
        trickster_bot.set_cursor(buy_pos[0], buy_pos[1])

        count += 1

        mouse_click()

        if count % 100 == 0:
            logging.info(f'Auto buy is running')
            logging.info(f'Bought')
        time.sleep(1)


def test7_sell5thingsinetc():
    print('----- Test 7 -----')

    number_of_items_etc_tab_before_selling = \
        trickster_bot.get_number_of_items_in_inventory_tabs()

    print(f'Number of items in Etc tab before selling:'
          f' {number_of_items_etc_tab_before_selling}')

    x0, y0 = trickster_bot.get_buy_sell_box_end_coord()
    # Buy/Sell button = (x1, y1) = (x0 - 120, y0)
    x_sell_buy, y_sell_buy = x0 - 120, y0

    # Use | Equip | Drill | Pet | Card | Etc =
    # [x0 - 320, Use
    # x0 - 280, Equip
    # x0 - 250, Drill
    # x0 - 220, Pet
    # x0 - 190, Card
    # x0 - 160, Etc] , y0 - 371
    tab_coords_x = [x0 - 320,
                    x0 - 280,
                    x0 - 250,
                    x0 - 220,
                    x0 - 190,
                    x0 - 160]
    tab_coords_y = y0 - 371

    # Switch to etc tab
    trickster_bot.set_cursor(tab_coords_x[-1], tab_coords_y)
    mouse_click()
    time.sleep(1)

    # First item increment button x, y = x0 - 26, y0 - 316
    x_increment_button, y_increment_button = x0 - 26, y0 - 316
    number_of_items_etc_tab_after_selling = \
        trickster_bot.get_number_of_items_in_inventory_tabs()
    while number_of_items_etc_tab_after_selling > \
            number_of_items_etc_tab_before_selling - 5:
        trickster_bot.set_cursor(x_increment_button, y_increment_button)
        mouse_click()
        time.sleep(0.5)
        trickster_bot.set_cursor(x_sell_buy, y_sell_buy)
        mouse_click()
        time.sleep(0.5)
        number_of_items_etc_tab_after_selling = \
            trickster_bot.get_number_of_items_in_inventory_tabs()
    print(f'Number of items in Etc tab after selling is '
          f'{number_of_items_etc_tab_after_selling}. Stopping auto....')


if __name__ == '__main__':
    global is_quit
    is_quit = False
    center = (trickster_bot.get_player_info()['player_x'],
              trickster_bot.get_player_info()['player_y'])
    while True:
        try:
            if not is_quit:
                attack(1, center, 400)
                pickup_by_name('Aposis Card: 1 number')
                sleep(1)
            else:
                sys.exit(0)
        except Exception as e:
            print(e)
            continue
