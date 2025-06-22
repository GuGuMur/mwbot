import httpx
from typing import Union
import re
import mwparserfromhell


class arktool:
    def __init__(
        self,
        domains: list = [
            "https://raw.githubusercontent.com/",
            "https://raw.kkgithub.com/",
            "https://ghproxy.com/https://raw.githubusercontent.com/",
            "https://fastly.jsdelivr.net/gh/",
            "https://cdn.staticaly.com/gh/",
            "https://ghproxy.net/https://raw.githubusercontent.com/",
            "https://gcore.jsdelivr.net/gh/",
            "https://jsdelivr.b-cdn.net/gh/",
        ],
    ):
        """同步构造函数"""
        self.domains = domains
        timeout = httpx.Timeout(10.0, connect=60.0, read=60.0, write=60.0, pool=60.0)
        self.client = httpx.AsyncClient(verify=False, timeout=timeout)
        self.headers = {"User-Agent": "mwbot/arktool"}

    async def __aexit__(self):
        """异步析构函数"""
        await self.client.aclose()

    async def read_ark_text(self, filename: str) -> str:
        for i in self.domains:
            try:
                res = await self.client.get(
                    url=f"{i}/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/{filename}",
                    headers=self.headers,
                )
                return res.text
            except Exception:
                pass
        return None

    async def read_ark_file(self, filename: str) -> dict:
        for i in self.domains:
            try:
                res = await self.client.get(
                    url=f"{i}/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/{filename}",
                    headers=self.headers,
                )
                return res.json()
            except Exception:
                pass
        return None

    async def get_item_name(self, id: Union[str, int]) -> str:
        """输出item(物品)ID对应的名称
        .. code-block:: python
            item = get_item_name("30012")
        :param id: 物品ID
        :returns: 对应物品的名称
        """
        res = await self.read_ark_file("excel/item_table.json")
        return res["items"][str(id)]["name"]

    async def deal_item_info(self, type: str, id: str, droptype: Union[str, int]) -> str:
        res = await self.read_ark_file("excel/item_table.json")
        link = res["items"][id]
        name = link["name"]
        if droptype == 8 or droptype == "COMPLETE":
            kind = "三星获得"
        return f"{name}:{kind}"

    async def catch_item_template(self, id: str, count: int) -> str:
        res = await self.read_ark_file("excel/item_table.json")
        return "{{材料消耗|" + str(res["items"][id]["name"]) + "|" + str(count) + "}}"

    def get_stage_id(self, content: str) -> str:
        wikicode = mwparserfromhell.parse(content)
        templates = wikicode.filter_templates()
        for i in templates:
            if i.name.matches("普通关卡信息") or i.name.matches("剿灭关卡信息"):
                return str(i.get("关卡id").value).strip()
        return None

    async def get_stage_info(self, content: str):
        stage_id: str = self.get_stage_id(content=content)
        stage_location: str = ""
        # 处理关卡id对应的文件路径
        if stage_id == "":
            return None
        elif match := re.match(r"^ro(\d+)_", stage_id):
            number = int(match.group(1))
            file = await self.read_ark_file("excel/roguelike_topic_table.json")
            stage_location = file["details"][f"rogue_{number}"]["stages"][stage_id]["levelId"]
        elif stage_id.startswith("mem_"):
            file = await self.read_ark_file("excel/handbook_info_table.json")
            for k, v in file["handbookStageData"].items():
                if v["stageId"] == stage_id:
                    stage_location = v["levelId"]
                    break
        elif stage_id.startswith("tower_"):
            file = await self.read_ark_file("excel/climb_tower_table.json")
            stage_location = file["levels"][stage_id]["levelId"]
        elif stage_id.startswith("act42d0_"):
            file = await self.read_ark_file("excel/activity_table.json")
            stage_location = file["activity"]["TYPE_ACT42D0"]["act42d0"]["stageInfoData"][stage_id]["levelId"]
        elif stage_id.startswith("sandbox_0"):
            file = await self.read_ark_file("excel/sandbox_table.json")
            stage_location = file["sandboxActTables"]["act1sandbox"]["stageDatas"][stage_id]["levelId"]
        elif stage_id.startswith("sandbox_1"):
            file = await self.read_ark_file("excel/sandbox_perm_table.json")
            stage_location = file["detail"]["SANDBOX_V2"]["sandbox_1"]["stageData"][stage_id]["levelId"]
        elif stage_id.startswith("ch_"):
            file = await self.read_ark_file("excel/story_review_meta_table.json")
            stage_location = file["trainingCampData"]["stageData"][stage_id]["levelId"]
        else:
            file = await self.read_ark_file("excel/stage_table.json")
            stage_location = file["stages"][stage_id]["levelId"]
        # 返回文件
        if stage_location:
            stage_location = stage_location.replace("\\", "/").lower()
            return await self.read_ark_file(f"levels/{stage_location}.json")
        else:
            return ""

    async def get_char_name(self, id: str) -> str:
        character_table = await self.read_ark_file("excel/character_table.json")
        return character_table[id]["name"]
