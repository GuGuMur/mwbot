'''mwbot的工具集'''
import re
import os
import ujson as json
import datetime
from loguru import logger
from jinja2 import Environment, FileSystemLoader

__all__ =  ["get_all_links",
            "get_page_links_from_pagelist_txt",
            "render_template"]


def get_all_links(content: str) -> list:
    '''从一段文字中获取其中所有的链接
    .. code-block:: python
        linklist = utils.get_all_links(content)
    :param content: 包含链接的字符串
    :returns: [list]
    '''
    page_list = re.findall(
        pattern='(?<=\[\[)(.+?)(?=(\|.*?)|(\]\]))', string=content)
    return [i[0] for i in page_list]


def get_page_links_from_pagelist_txt(folder=os.path.dirname(os.path.abspath(__file__))) -> list:
    '''从bot文件同目录下的pagelist.txt读取每行对应的页面名并返回列表。

    .. code-block:: python
        pagelist = utils.get_page_links_from_pagelist_txt()
    :param folder: [可选项]pagelist.txt所在的文件夹
    :returns: list'''
    classes_path = os.path.expanduser(f'{folder}/pagelist.txt')
    with open(f"{folder}/pagelist.txt", 'r', encoding='UTF-8') as f:
        pagelist = f.readlines()
    pagelist = [c.rstrip() for c in pagelist]
    return pagelist


def render_template(T_NAME: str, **kwargs) -> str:
    '''从 bot程序 目录下的 /templates 目录中选择Jinja2模板并渲染
    .. code-block:: python
        utils.render_template(T_NAME="test.jinja",name="Test")
    :param T_NAME: ./templates 目录中的模板文件名
    :param **kwargs: 对应模板要求的参数
    :return: 渲染后的结果'''
    T_ENV = Environment(loader=FileSystemLoader(
        f'{os.path.dirname(os.path.abspath(__file__))}/templates'))
    return T_ENV.get_template(T_NAME).render(**kwargs).strip()