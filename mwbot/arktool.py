"""存储与PRTS编辑相关的方法"""
import mwparserfromhell
import ujson as json
from typing import Union

# import re
# from loguru import logger
# import os
# from pathlib import Path


GameDataPosition = "/home/bot/ArknightsGameData/zh_CN/gamedata"


def read_ark_file(filename: str) -> dict:
    with open(f"{GameDataPosition}/{filename}", "r", encoding="utf-8") as f:
        content = f.read()
    return json.loads(content)


def get_item_name(id: Union[str, int]) -> str:
    """输出item(物品)ID对应的名称
    .. code-block:: python
        item = get_item_name("30012")
    :param id: 物品ID
    :returns: 对应物品的名称
    """
    return read_ark_file("excel/item_table.json")["items"][str(id)]["name"]


def deal_item_info(type: str, id: str, droptype: int) -> str:
    link = read_ark_file("excel/item_table.json")["items"][id]
    name = link["name"]
    if droptype == 8:
        kind = "三星获得"
    return f"{name}:{kind}"


def catch_item_template(id: str, count: int) -> str:
    return (
        "{{材料消耗|"
        + str(read_ark_file("excel/item_table.json")["items"][id]["name"])
        + "|"
        + str(count)
        + "}}"
    )


def get_stage_id(content):
    wikicode = mwparserfromhell.parse(content)
    templates = wikicode.filter_templates()
    for i in templates:
        if i.name.matches("普通关卡信息") or i.name.matches("剿灭关卡信息"):
            return str(i.get("关卡id").value).strip()


def get_stage_info(content):
    stage_id = get_stage_id(content=content)
    stage_id_location = read_ark_file("excel/stage_table.json")["stages"][stage_id][
        "levelId"
    ]
    if stage_id_location == None:
        return None
    else:
        stage_id_location = stage_id_location.lower()
        return read_ark_file("gamedata/levels/{stage_id_location}.json")


class char:
    def __init__(self) -> None:
        self.character_table = read_ark_file("excel/character_table.json")

    def get_char_name(self, id: str) -> str:
        return self.character_table[id]["name"]
