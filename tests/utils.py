# import mwparserfromhell
import re
import ujson as json
from loguru import logger
import os
import inspect
from mako.template import Template
from mako.runtime import Context

def get_keys(dict,value)->list:
	'''[dict]用于获取键内容相同的所有值'''
	l = [k for k,v in dict.items() if v==value]
	if l :
		return l
	else:
		logger.warning(f'请检查字典{dict}中是否存在值为{value}的键!')
		return []

def get_all_links(content:str)->list:
    page_list = re.findall(pattern='(?<=\[\[)(.+?)(?=(\|.*?)|(\]\]))', string=content)
    return [i[0] for i in page_list]

# def get_page_links_from_pagelist_txt(content=os.path.dirname(__file__))->list:
def get_page_links_from_pagelist_txt(content=os.path.dirname(inspect.stack()[1].filename))->list:
	classes_path = os.path.expanduser(f'{content}/pagelist.txt')
	with open(classes_path,'r',encoding = 'UTF-8') as f:
		pagelist = f.readlines()
	pagelist = [c.rstrip() for c in pagelist]
	return pagelist

def template_from_file(t_name:str,**kwargs)->str:
    template = Template(filename=os.path.expanduser(f'{os.path.dirname(inspect.stack()[1].filename)}/templates/{t_name}'),strict_undefined=True)  
    return template.render(**kwargs).strip()