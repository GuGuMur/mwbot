'''存储与PRTS编辑相关的方法'''
import mwparserfromhell
import re
import ujson as json
from loguru import logger
import os
from pathlib import Path
from typing import Union

GameDataPosition = "/home/bot/ArknightsGameData/zh_CN/gamedata"

def read_ark_cn_file(filename):
    return json.loads(Path(f"{GameDataPosition}/{filename}").read_text())


def get_item_name(id:Union[str,int])->str:
    '''输出item(物品)ID对应的名称
    .. code-block:: python
        
    :param id: 物品ID
    :returns: 对应物品的名称
    '''
    return read_ark_cn_file("excel/item_table.json")['items'][str(id)]['name']

def deal_item_info(type:str,id:str,droptype:int)->str:
    link = read_ark_cn_file("excel/item_table.json")["items"][id]
    name = link["name"]
    if droptype == 8:
        kind = "三星获得"
    return f"{name}:{kind}"

def catch_item_template(id:str,count:int)->str:
    return "{{材料消耗|"+str(read_ark_cn_file("excel/item_table.json")["items"][id]["name"])+"|"+str(count)+"}}"

def get_stage_id(content):
    wikicode = mwparserfromhell.parse(content)
    templates = wikicode.filter_templates()
    for i in templates:
        if i.name.matches('普通关卡信息') or i.name.matches('剿灭关卡信息'):
            return str(temp.get('关卡id').value).strip()

def get_stage_info(content):
    stage_id = get_stage_id(content=content)
    stage_id_location = read_ark_cn_file("excel/stage_table.json")['stages'][stage_id]['levelId']
    if stage_id_location == None:
        return None
    else:
        stage_id_location = stage_id_location.lower()
        return read_ark_cn_file('gamedata/levels/{stage_id_location}.json')

def get_char_name(id:str)->str:
    return read_ark_cn_file("excel/character_table")[id]["name"]