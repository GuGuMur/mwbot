from abc import ABC
import mwparserfromhell
import pendulum
import regex as re
'''定义一些功能特化的基类'''
class WikiSectionDict(ABC):
    '''用于get_section()方法的字典类
    覆写了dict.index()方法，输出可直接用于edit(section)的值'''
    def __init__(wd):
        self.wd = wd
    def index(num:str)->str:
        return int(self.wd.index(num)+1)
    
class gen_wikitext():
    '''生成wikitext'''
    def __init__(self):
        self.txt:str = """"""
    def add_title(self,po:int,title:str):
        self.txt += "="*po + title + "="*po + "\n"
    def add_text(self,text:str):
        self.txt += (text + "\n")
    def add_cat(self,cat:str):
        self.txt += f"[[分类:{cat}]]\n"
        
class gen_tem():
    '''生成wikitext-template'''
    def __init__(self,title):
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
    def result(self):
        '''输出结果'''
        if self.enter_int != 0:
            self.txt += "\n"
        self.txt += "}}"
        return self.txt