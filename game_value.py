from getbaseaddr import *

GAME_BASE_ADDRESS = get_base_address()

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
    # 'Shield',
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

PINK_POTION_A_BASE = GAME_BASE_ADDRESS + int(0x0008FEA0)
PINK_POTION_A_OFFSET = [0x48, 0x14, 0x0, 0x7C]

BUY_BOX_BASE = GAME_BASE_ADDRESS + int(0x009B7484)
X0_BUY_BOX_OFFSET = [0xDF0, 0x864, 0xB8, 0x14, 0x0, 0x24, 0x30]
Y0_BUY_BOX_OFFSET = [0xDF0, 0x864, 0xB8, 0x14, 0x0, 0x24, 0x34]

NUMBER_OF_ITEMS_IN_ETC_TAB_BASE = GAME_BASE_ADDRESS + int(0x009AFEB4)
NUMBER_OF_ITEMS_IN_ETC_TAB_OFFSET = [0x3DC, 0x46C, 0x4E0, 0x1E4]

SKILL_SLOT_BASE = GAME_BASE_ADDRESS + int(0x009B7484)
SKILL_SLOT_X_OFFSET = [0x474, 0x10, 0x30, 0x4C, 0xD8, 0xB4, 0x108]
SKILL_SLOT_Y_OFFSET = [0x474, 0x10, 0x30, 0x4C, 0xD8, 0xB4, 0x10C]