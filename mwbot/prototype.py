"""定义一些功能特化的基类"""
from abc import ABC
import mwparserfromhell

# import pydantic
# import pendulum
# import regex as re


class WikiSectionList(ABC):
    """用于Bot.get_sections()方法的字典类
    覆写了dict.index()方法，输出可直接用于bot.edit(section)的值"""

    def __init__(self, wl: list):
        self.wl = wl

    def index(self, name: str) -> int:
        return self.wl.index(name) + 1

    def __str__(self):
        return str(self.wl)

    @property
    def list(self):
        return self.wl


class gen_wikitext:
    """生成wikitext"""

    def __init__(self):
        self.txt: str = """"""

    def add_title(self, times: int, title: str):
        self.txt += "=" * times + title + "=" * times + "\n"

    def add_text(self, text: str):
        self.txt += text + "\n"

    def add_cat(self, cat: str):
        self.txt += f"[[分类:{cat}]]\n"


class gen_tem:
    """生成wikitext-template"""

    def __init__(self, title: str, with_enter: bool = True):
        self.params = []
        self.with_enter = with_enter
        if self.with_enter:
            self.txt += "\n"

    def add_par(self, name: str = "", txt: str = ""):
        """添加一行参数"""
        if name:
            self.params.append(f"|{name}={txt}")
        else:
            self.params.append(f"|{txt}")

    def result(self) -> str:
        """输出结果"""
        enter_key = ""
        if self.with_enter:
            enter_key = "\n"
        return "{{" + enter_key.join(self.params) + "}}"
