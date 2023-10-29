"""mwbot的工具集"""
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def get_all_links(content: str) -> list:
    """从一段文字中获取其中所有的链接
    .. code-block:: python
        linklist = utils.get_all_links(content)
    :param content: 包含链接的字符串
    :returns: [list]
    """
    page_list = re.findall(pattern="(?<=\[\[)(.+?)(?=(\|.*?)|(\]\]))", string=content)
    return [i[0] for i in page_list]


def get_page_links_from_pagelist_txt(folder=str(Path(__file__).parent),) -> list:
    """从bot文件同目录下的pagelist.txt读取每行对应的页面名并返回列表。

    .. code-block:: python
        pagelist = utils.get_page_links_from_pagelist_txt()
    :param folder: [可选项]pagelist.txt所在的文件夹
    :returns: list"""
    file_path = str(Path(folder)/"pagelist.txt")
    with open(file_path, "r", encoding="UTF-8") as f:
        pagelist = f.readlines()
    return [l.rstrip() for l in pagelist]


class templates_env:
    """创建一个模板的渲染Environment，
    .. code-block:: python
            ENV = utils.templates_env
    :params: DIR_PATH(`str`)：环境目录，默认为`./templates`
    :params: **kwargs : Jinja.Environment所需的参数，参考[https://jinja.palletsprojects.com/en/3.0.x/api/#jinja2.Environment]
    :return: `dict`
    默认位置为 `./templates `"""

    def __init__(
        self,
        DIR_PATH: str = f"{str(Path(__file__).parent / 'templates')}",
        **kwargs,
    ):
        self.T_ENV = Environment(loader=FileSystemLoader(DIR_PATH), **kwargs)

    def render(self, T_NAME: str, **kwargs) -> str:
        """选择Jinja2模板并渲染
        .. code-block:: python
            utils.render_template(T_NAME="test.jinja", name="Test")
        :param T_NAME: 目录中的模板文件名
        :param **kwargs: 对应模板要求的参数
        :return: 渲染后的结果"""
        return self.T_ENV.get_template(T_NAME).render(**kwargs).strip()
