'''存储与PRTS编辑相关的方法'''
import mwparserfromhell
import re
import requests
import json
from loguru import logger
import os
import mwbot.model as model

def get_item_name(id:str)->str:
    """输入：`id`
    输出：对应的道具名称"""
    return model.ITEM_TABLE['items'][id]['name']

def deal_item_info(type:str,id:str,droptype:int)->str:
    link = model.ITEM_TABLE["items"][id]
    name = link["name"]
    if droptype == 8:
        kind = "三星获得"
    return f"{name}:{kind}"

def catch_item_template(id:str,count:int)->str:
    return "{{材料消耗|"+str(model.ITEM_TABLE["items"][id]["name"])+"|"+str(count)+"}}"

def read_ark_cn_file(filename):
	with open(f"/home/bot/ArknightsGameData/zh_CN/gamedata/{filename}",'r',encoding='utf-8') as load_f:
		return json.load(load_f)

def trap_set(page_name:str, trap_list:list):
    ...

def get_stage_id(content):
    wikicode = mwparserfromhell.parse(content)
    templates = wikicode.filter_templates()
    for i in templates:
        if i.name.matches('普通关卡信息') or i.name.matches('剿灭关卡信息'):
            temp = i
            break
    stage_id = temp.get('关卡id').value
    return stage_id.strip()


def get_stage_info(content):
    stage_id = get_stage_id(content=content)
    stage_id_location = model.STAGE_TABLE['stages'][stage_id]['levelId']
    if stage_id_location == None:
        return None
    else:
        stage_id_location = stage_id_location.lower()
        return read_ark_cn_file('gamedata/levels/{stage_id_location}.json')

def get_char_name(id:str)->str:
    return model.CHARACTER_TABLE[id]["name"]