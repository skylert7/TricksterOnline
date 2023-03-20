import math
import pymem
import pymem.process
import pymem.memory
import pyautogui
from time import sleep
import random
import os
import sys

from discord_webhook import DiscordWebhook

process = pymem.process
mem = pymem.memory
coowon_game_flash_pid = 0x000041A0
pymem_object = pymem.Pymem()
pymem_object.open_process_from_id(coowon_game_flash_pid)

quanlenh_num_addr = 0x0DF3221C
quanlenh_num = pymem_object.read_int(address=quanlenh_num_addr)
print(quanlenh_num)

# tuuquan_addr = 0x2F247BEC
# tuuquan = pymem_object.read_int(address=tuuquan_addr)
# print(tuuquan)



def notify_discord(msg='Test'):
    discord_webhook_url = 'https://discord.com/api/webhooks/1016231343090323476/t0cMLZ7YoD3V7-K5YKcvoRyi-fgQ3deZX11611syrDtkiNu5VApRhin-DfzjDf25EyHm'
    webhook = DiscordWebhook(
        url=discord_webhook_url,
        rate_limit_retry=True,
        content='@everyone {}'.format(msg))
    response = webhook.execute()
    return response.status_code


def quanruou():
    while True:
        tuuquan_before = pymem_object.read_int(address=tuuquan_addr)

        print(tuuquan_before)

        sleep(5)

        tuuquan_after = pymem_object.read_int(address=tuuquan_addr)
        print(tuuquan_after)
        if tuuquan_before == tuuquan_after:
            characters = (613, 220)

            moinhanh = (1221, 780)
            for i in range(3):
                pyautogui.click(characters[0], characters[1])
                sleep(2)
            pyautogui.click(moinhanh[0], moinhanh[1])


def chiencong():
    print('Please switch to ngoalong window')
    sleep(5)
    print('Start chiencong')
    troops = (1189, 364)
    tancong_confirm = troops  # in this case

    quanlenh_num = pymem_object.read_int(address=quanlenh_num_addr)
    is_spinning = False
    while True:
        try:
            if quanlenh_num < 100 and not is_spinning:
                tinhtu(start=True)
                is_spinning = True
            elif quanlenh_num > 900 and is_spinning:
                tinhtu(start=False)
                is_spinning = False

            print(quanlenh_num)

            pyautogui.click(troops[0], troops[1])
            sleep(1)
            pyautogui.click(tancong_confirm[0], tancong_confirm[1])
            sleep(1)

            quanlenh_num = pymem_object.read_int(address=quanlenh_num_addr)

        except:
            print('Exception')

    return


def tinhtu(start=True):
    tinhtu_icon = (1138, 164)
    start_stop_button = (780, 472)
    start_confirm = (1020, 423)
    close_button = (1440, 160)
    if start:
        pyautogui.click(tinhtu_icon[0], tinhtu_icon[1])
        sleep(0.5)
        pyautogui.click(start_stop_button[0], start_stop_button[1])
        sleep(0.5)
        pyautogui.click(start_confirm[0], start_confirm[1])
        sleep(0.5)
        pyautogui.click(close_button[0], close_button[1])
        sleep(0.5)
    else:
        pyautogui.click(tinhtu_icon[0], tinhtu_icon[1])
        sleep(0.5)
        pyautogui.click(start_stop_button[0], start_stop_button[1])
        sleep(0.5)
        pyautogui.click(close_button[0], close_button[1])
        sleep(0.5)
    return


chiencong()
