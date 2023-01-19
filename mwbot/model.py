'''储存了一些变量'''
from .arktool import read_ark_cn_file as AKR
STAGE_TABLE = AKR("excel/stage_table.json")
ITEM_TABLE = AKR("excel/item_table.json")
GAMEDATA_CONST = AKR("excel/gamedata_const.json")
CHARACTER_TABLE = AKR("excel/character_table.json")
HANDBOOK_INFO = AKR("excel/handbook_info_table.json")
