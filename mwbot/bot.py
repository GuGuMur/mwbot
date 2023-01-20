import httpx
import ujson as json
from loguru import logger
import os
from .prototype import WikiSectionDict
from typing import Union

class Bot:
    '''(https://www.mediawiki.org/wiki/API:Main_page/zh)[Mediawiki文档]
    现阶段要求sitename, api，index，username，password五个参数'''

    # 成员变量
    def __init__(self,sitename:str,api:str,index:str,username:str,password:str):
        '''初始化参数sitename, api, index, username, password'''
        self.sitename = sitename
        self.api = api
        self.index = index
        self.username = username
        self.password = password
        self.client = httpx.AsyncClient()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'}

    async def fetch_token(self, type:str)->str:
        '''fetch_token(type=STRING)
        根据不同的type类型返回对应的token'''
        PARAMS = {
            'action': "query",
            'meta': "tokens",
            'type': type,
            'format': "json"
        }
        token = await self.client.post(url=self.api, data=PARAMS)
        token = token.json()
        location = type + "token"
        return token['query']['tokens'][location]

    async def login(self):
        '''登录'''
        login_PARAMS = {
            'action': "login",
            'lgname': self.username,
            'lgpassword': self.password,
            'lgtoken': await self.fetch_token(type="login"),
            'format': "json"
        }
        login = await self.client.post(url=self.api, data=login_PARAMS,headers=self.headers)
        login = login.json()
        if login['login']['result'] == "Success":
            logger.info(f'Welcome to {self.sitename}, {login["login"]["lgusername"]}!')

    async def close(self):
        await self.client.aclose()

    async def get_data(self, page_name:str):
        PARAMS = {
            "action": "query",
            "prop": "revisions",
            "titles": page_name,
            "rvslots": "*",
            "rvprop": "content",
            "formatversion": 2,
            "format": "json"
        }
        text = await self.client.post(url=self.api, data=PARAMS, headers=self.headers)
        text = text.json()
        text = text["query"]["pages"][0]
        logger.info(f'Get info of [[{text["title"]}]] successfully.')
        return text

    async def get_page_text(self,page_name:str,section:Union[str,int]='')->str:
        '''获取页面中的文本'''
        # PARAMS = {
        #     "title=": page_name,
        #     "action": "raw",
        #     "section": section
        # }
        # act = self.S.post(url=self.index, data=PARAMS, headers=self.headers)
        act = await self.client.post(url=f"{self.index}?action=raw&title={page_name}&section={str(section)}", headers=self.headers)
        if act.status_code == 404:
            logger.warning(f"请检查get_page_text传入的页面是否在{self.sitename}存在。")
            return None
        else:
            return str(act.text)

    async def edit_page(self,title:str,text:str,summary:str="", **kwargs):
        '''编辑一个页面。常用参数：title,text,summary.'''
        PARAMS = {
            "action": "edit",
            "minor": True,
            "bot": True,
            "format": "json",
            "title": title,
            "text": text,
            "summary":summary
        }
        for key, value in kwargs.items():
            key = str(key)
            value = str(value)
            PARAMS[key] = value
        PARAMS["token"] = self.fetch_token(type="csrf")
        PARAMS["summary"] += " //Edit by Bot."
        act = await self.client.post(url=self.api, data=PARAMS, headers=self.headers)
        act = act.json()
        if act['edit']['result'] == "Success":
            logger.info(f'Edit [[{PARAMS["title"]}]] successfully.')
        else:
            logger.debug(act)

    async def create_page(self,title:str,text:str,summary:str)->bool:
        '''创建页面'''
        deal = self.get_data(page_name=title)
        if "missing" in deal:
            self.edit_page(title=title,text=text,summary=summary)
            return False
        else:
            logger.info(f"Skip Create [[{title}]].")
            return True

    async def upload_local(self,local_name,local_path,web_name,text="", **kwargs):
        '''从本地上传一个文件.'''
        PARAMS = {
            "action": "upload",
            "filename": web_name,
            "format": "json",
            "token": self.fetch_token(type="csrf"),
            "ignorewarnings": True,
            "watchlist" :"nochange"
        }
        for key, value in kwargs.items():
            key = str(key)
            value = str(value)
            PARAMS[key] = value
        FILE = {'file': (local_name, open(local_path, 'rb'), 'multipart/form-data')}
        act = await self.client.post(url=self.api, data=PARAMS,headers=self.headers, files=FILE)
        act = act.json()
        # logger.info(f'Upload {local_name}=>[[File:{web_name}]] successfully.')
        print(act)

    async def purge(self,titles:str,**kwargs):
        '''刷新页面'''
        PARAMS = {
            "action": "purge",
            "titles": titles,
            "format": "json"
        }
        for key, value in kwargs.items():
            key = str(key)
            value = str(value)
            PARAMS[key] = value
        act = await self.client.post(url=self.api, data=PARAMS,headers=self.headers)
        act = act.json()
        logger.info(f"Purge [[{titles}]] Successfully.")

    async def parse(self, page_name, **kwargs):
        '''解析'''
        PARAMS = {
            "format": "json",
            "page": page_name,
            "action": "parse"
        }
        for key, value in kwargs.items():
            key = str(key)
            value = str(value)
            PARAMS[key] = value
        act = await self.client.post(url=self.api, data=PARAMS, headers=self.headers)
        return act.json()


    async def get_section(self, page_name:str)->WikiSectionDict:
        result = await self.parse(page_name=page_name, prop='sections')
        result = result['parse']['sections']
        result_list = []
        for i in result:
            result_list.append(i['line'])
        if result_list:
            return WikiSectionDict(result_list)
        else:
            logger.info(f'页面{page_name}没有任何章节！')

    async def deal_flow(self,title,cotmoderationState,cotreason="标记"):
        PARAMS = {
            "action": "flow",
            "page": str(title),
            "submodule":"lock-topic", 
            "cotmoderationState":cotmoderationState,
            "cotreason":cotreason,
            "format": "json",
            "token":self.fetch_token(type="csrf")
        }
        act = await self.client.post(url=self.api, data=PARAMS, headers=self.headers).json()
        logger.info(f"{cotmoderationState} the flow {title} successfully.({cotreason})")

    async def reply_flow(self,title,content):
        PARAMS = {
            "action": "flow",
            "submodule":"reply",
            "page":title,
            "repreplyTo": str(title),
            "repcontent":str(content),
            "repformat":"wikitext",
            "format": "json",
            "token":self.fetch_token(type="csrf")
        }
        act = await self.client.post(url=self.api, data=PARAMS, headers=self.headers).json()
        logger.info(f"Reply the flow {title} successfully.")

    async def rc(self,namespace):
        ...