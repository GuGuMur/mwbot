'''定义一些功能特化的基类'''
from abc import ABC
import mwparserfromhell
# import pendulum
# import regex as re

class WikiSectionDict(ABC):
    '''用于Bot.get_section()方法的字典类
    覆写了dict.index()方法，输出可直接用于edit(section)的值'''
    def __init__(self, wd:list):
        self.wd = wd
    def index(num:str)->int:
        return self.wd.index(num)+1
    def __str__(self):
        return str(self.wd)
    
class gen_wikitext:
    '''生成wikitext'''
    def __init__(self):
        self.txt:str = """"""
    def add_title(self,po:int,title:str):
        self.txt += "="*po + title + "="*po + "\n"
    def add_text(self,text:str):
        self.txt += (text + "\n")
    def add_cat(self,cat:str):
        self.txt += f"[[分类:{cat}]]\n"
        
class gen_tem:
    '''生成wikitext-template'''
    def __init__(self,title:str):
        self.txt = "{{"+title
        self.enter_int = 0
    def add_par(self,name:str = "", txt:str = "", enter:bool=True):
        '''添加一行参数。'''
        if bool == True:
            self.txt += "\n"
            self.enter_int += 1
        if name:
            self.txt+=f"|{name}={txt}"
        else:
            self.txt += f"|{txt}"
    def result(self)->str:
        '''输出结果'''
        if self.enter_int != 0:
            self.txt += "\n"
        self.txt += "}}"
        return self.txt