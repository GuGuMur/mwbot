"""存储与PRTS编辑相关的方法"""
import mwparserfromhell
import ujson as json
from typing import Union
import re

# from loguru import logger
# import os
# from pathlib import Path


GameDataPosition = "/home/bot/ArknightsGameData/zh_CN/gamedata"

def read_ark_text(filename: str) -> str:
    with open(f"{GameDataPosition}/{filename}", "r", encoding="utf-8") as f:
        content = f.read()
    return content

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


def deal_item_info(type: str, id: str, droptype: Union[str, int]) -> str:
    link = read_ark_file("excel/item_table.json")["items"][id]
    name = link["name"]
    if droptype == 8 or droptype == "COMPLETE":
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


def get_stage_id(content) -> str:
    wikicode = mwparserfromhell.parse(content)
    templates = wikicode.filter_templates()
    for i in templates:
        if i.name.matches("普通关卡信息") or i.name.matches("剿灭关卡信息"):
            return str(i.get("关卡id").value).strip()
    return None


def get_stage_info(content: str):
    stage_id: str = get_stage_id(content=content)
    # 处理关卡id对应的文件路径
    if stage_id == "":
        return None
    elif match := re.match(r"^ro(\d+)_", stage_id):
        number = int(match.group(1))
        stage_location = read_ark_file("excel/roguelike_topic_table.json")["details"][f"rogue_{number}"]["stages"][stage_id]["levelId"]
    elif stage_id.startswith("mem_"):
        for k, v in read_ark_file("excel/handbook_info_table.json")["handbookStageData"].items():
            if v["stageId"] == stage_id:
                stage_location = v["levelId"]
                break
    elif stage_id.startswith("tower_"):
        stage_location = read_ark_file("excel/climb_tower_table.json")["levels"][stage_id]["levelId"]
    elif stage_id.startswith("act42d0_"):
        stage_location = read_ark_file("excel/activity_table.json")["activity"]["TYPE_ACT42D0"]["act42d0"]["stageInfoData"][stage_id]["levelId"]
    elif stage_id.startswith("sandbox_0"):
        stage_location = read_ark_file("excel/sandbox_table.json")["sandboxActTables"]["act1sandbox"]["stageDatas"][stage_id]["levelId"]
    elif stage_id.startswith("sandbox_1"):
        stage_location = read_ark_file("excel/sandbox_perm_table.json")["detail"]["SANDBOX_V2"]["sandbox_1"]["stageData"][stage_id]["levelId"]
    elif stage_id.startswith("ch_"):
        stage_location = read_ark_file("excel/story_review_meta_table.json")["trainingCampData"]["stageData"][stage_id]["levelId"]
    else:
        stage_location = read_ark_file("excel/stage_table.json")["stages"][stage_id]["levelId"]
    # 返回文件
    if stage_location:
        stage_location = stage_location.replace("\\", "/").lower()
        return read_ark_file(f"levels/{stage_location}.json")
    else:
        return ""


class char:
    def __init__(self) -> None:
        self.character_table = read_ark_file("excel/character_table.json")

    def get_char_name(self, id: str) -> str:
        return self.character_table[id]["name"]
