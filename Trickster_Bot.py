from game_value import *


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

    def set_potionA_buy_amount_to_one(self):
        # set potion A buy amount to one
        mem.write_int(self.handle,
                      self.address_adder(PINK_POTION_A_BASE,
                                         PINK_POTION_A_OFFSET),
                      1)

    def get_number_of_items_in_inventory_tabs(self):
        number_of_items_etc_tab_addr = self.address_adder(
            NUMBER_OF_ITEMS_IN_ETC_TAB_BASE,
            NUMBER_OF_ITEMS_IN_ETC_TAB_OFFSET)
        number_of_items_etc_tab = mem.read_uint(self.handle,
                                                number_of_items_etc_tab_addr)

        return number_of_items_etc_tab

    def get_buy_sell_box_end_coord(self):
        x0_buy_box_addr = self.address_adder(BUY_BOX_BASE,
                                             X0_BUY_BOX_OFFSET)

        y0_buy_box_addr = self.address_adder(BUY_BOX_BASE,
                                             Y0_BUY_BOX_OFFSET)

        x0_buy_box = mem.read_uint(self.handle, x0_buy_box_addr)
        y0_buy_box = mem.read_uint(self.handle, y0_buy_box_addr)

        # print(f'x0 - {x0_buy_box}, y0 - {y0_buy_box}')
        return x0_buy_box, y0_buy_box

    def get_skill_slot_coord(self):
        skill_slot_x_addr = self.address_adder(SKILL_SLOT_BASE,
                                               SKILL_SLOT_X_OFFSET)

        skill_slot_y_addr = self.address_adder(SKILL_SLOT_BASE,
                                               SKILL_SLOT_Y_OFFSET)

        skill_slot_x = mem.read_uint(self.handle, skill_slot_x_addr)
        skill_slot_y = mem.read_uint(self.handle, skill_slot_y_addr)

        return skill_slot_x, skill_slot_y
