import httpx
from loguru import logger
import os
import urllib
from mwbot import error
from typing import Union
from .prototype import WikiSectionList


class Bot:
    """(https://www.mediawiki.org/wiki/API:Main_page/zh)[Mediawiki文档]
    Bot根程序。
    :param sitename(`str`) : 站点名称
    :param index(`str`) : index.php目录
    :param api(`str`) : index.php路径
    :param index(`str`) : api.php路径
    :param username(`str`) : 用户名
    :param password(`str`) : 用户密码"""

    # 成员变量
    def __init__(
        self, sitename: str, api: str, index: str, username: str, password: str
    ):
        """同步构造函数"""
        self.sitename = sitename
        self.api = api
        self.index = index
        self.username = username
        self.password = password
        timeout = httpx.Timeout(10.0, connect=60.0, read=60.0, write=60.0, pool=60.0)
        self.client = httpx.AsyncClient(verify=False, timeout=timeout)
        self.headers = {"User-Agent": f"{self.username.encode('utf-8')}/mwbot"}

    async def __aexit__(self):
        """异步析构函数"""
        await self.client.aclose()

    async def call_get_api(self, action: str, **kwargs) -> dict:
        data = {"action": action, "format": "json"}
        data.update(kwargs)

        act = await self.client.get(url=self.api, params=data, headers=self.headers)
        act.raise_for_status()
        return act.json()

    async def call_post_api(self, action: str, **kwargs) -> dict:
        data = {"action": action, "format": "json"}
        data.update(kwargs)

        act = await self.client.post(url=self.api, data=data, headers=self.headers)
        act.raise_for_status()
        return act.json()

    async def fetch_token(self, type: str) -> str:
        """根据不同的type类型返回对应的token
        :param: type(`str`)  token的类型"""

        params = {"action": "query", "meta": "tokens", "type": type, "format": "json"}
        token = await self.client.get(url=self.api, params=params)
        token.raise_for_status()
        token = token.json()
        location = type + "token"
        return token["query"]["tokens"][location]

    async def login(self) -> None:
        """登录
        :use: await bot.login()"""

        data = {
            "action": "login",
            "lgname": self.username,
            "lgpassword": self.password,
            "lgtoken": await self.fetch_token(type="login"),
            "format": "json",
        }
        login = await self.client.post(url=self.api, data=data, headers=self.headers)
        login.raise_for_status()
        login = login.json()
        if login["login"]["result"] == "Success":
            logger.success(f'您已登录至{self.sitename}, {login["login"]["lgusername"]}！')
        else:
            raise error.mwbotLoginError(
                f"用户{self.username}登录至{self.sitename}中出现了错误。\n{login}"
            )

    async def get_data(self, title: str) -> dict:
        """获取页面的数据
        :use: data = await bot.get_data(title)
        :params: title(`str`)：页面名
        :return: `dict`"""

        data = {
            "action": "query",
            "prop": "revisions",
            "titles": title,
            "rvslots": "*",
            "rvprop": "content",
            "formatversion": 2,
            "format": "json",
        }
        text = await self.client.post(url=self.api, data=data, headers=self.headers)
        text.raise_for_status()
        text = text.json()
        text = text["query"]["pages"][0]
        return text

    async def get_page_text(
        self, title: str, section: Union[str, int] = ""
    ) -> Union[str, None]:
        """获取页面中的文本
        :use: text = bot.get_page_text(title)
        :params: title(`str`)：页面标题
        :params: section(`Union[str,int]`)：*可选项* 编辑章节号
        :return: str/None"""
        act = await self.client.post(
            url=f"{self.index}?action=raw&title={urllib.parse.quote(title)}&section={str(section)}",
            headers=self.headers,
        )
        act.raise_for_status()
        return str(act.text)

    async def edit_page(self, title: str, **kwargs):
        """编辑一个页面
        :use: await bot.edit_page(title,text,summary)
        :params: title(`str`) : 编辑页面的标题，不自动重定向
        :params: text(`str`) : 编辑页面的内容
        :params: summary(`str`) : 编辑摘要
        :params: ...
        :return: None"""

        data = {
            "action": "edit",
            "minor": True,
            "bot": True,
            "format": "json",
            "token": await self.fetch_token(type="csrf"),
            "title": title,
        }
        data.update(kwargs)
        act = await self.client.post(url=self.api, data=data, headers=self.headers)
        logger.info(f"已向{self.sitename}发送页面[[{title}]]的编辑请求。")
        act.raise_for_status()
        act: dict = act.json()
        if act.get("edit", {}).get("result", None) is not None:
            if act["edit"]["result"] == "Success":
                logger.success(f'成功编辑页面 [[{data["title"]}]]。')
            else:
                logger.debug(act)
                return False
        else:
            logger.debug(act)
            return False

    async def create_page(self, title: str, text: str, summary: str = "") -> bool:
        """创建页面
        :use: bot.create_page(title,text,summary)
        :params: title(`str`) : 创建页面的标题
        :params: text(`str`) : 创建页面的内容
        :params: summary(`str`) : 编辑摘要
        :return: bool：指示创建是否成功（True为成功，False为失败）"""

        deal = await self.get_data(title=title)
        if "missing" in deal:
            await self.edit_page(title=title, text=text, summary=summary)
            return True
        else:
            logger.warning(f"跳过创建[[{title}]]。")
            return False

    async def upload_local(
        self, filepath, servername=None, text="", comment="", **kwargs
    ) -> bool:
        """从本地上传一个文件。"""
        if servername is None:
            servername = os.path.basename(filepath)
        data = {
            "action": "upload",
            "filename": servername,
            "token": await self.fetch_token(type="csrf"),
            "text": text,
            "comment": comment,
            "ignorewarnings": True,
            "watchlist": "nochange",
            "async": True,
            "format": "json",
        }
        data.update(kwargs)
        FILE = {
            "file": (
                os.path.basename(filepath),
                open(filepath, "rb"),
                "multipart/form-data",
            )
        }
        act = await self.client.post(
            url=self.api, data=data, headers=self.headers, files=FILE
        )
        act.raise_for_status()
        act = act.json()
        if act.get("upload", {}).get("result", None) is not None:
            if act["upload"]["result"] == "Success":
                logger.success(
                    f"成功上传本地文件 {filepath} 至 [[{self.sitename}:文件:{servername}]]。"
                )
                return True
            else:
                logger.debug(
                    f"上传本地文件 {filepath} 至 [[{self.sitename}:文件:{servername}]]失败。\n{act}"
                )
                return False
        else:
            logger.debug(act)
            return False

    async def purge(self, title: str, **kwargs) -> None:
        """刷新页面"""

        data = {"action": "purge", "titles": title, "format": "json"}
        data.update(kwargs)
        act = await self.client.post(url=self.api, data=data, headers=self.headers)
        act.raise_for_status()
        act = act.json()
        logger.success(f"成功刷新页面 [[{title}]]。")

    async def move_page(self, frompage: str, topage: str, **kwargs):
        """移动一个页面
        :use: await bot.move_page(frompage,topage)
        :params: frompage(`str`) : 移动的页面
        :params: topage(`str`) : 到的页面
        :params: reason(`str`) : 移动原因
        :params: movetalk(`str`) : 重命名讨论页，如果存在
        :params: movesubpages(`str`) : 重命名子页面，如果存在
        :params: noredirect(`str`) : 不创建重定向
        :params: ...
        :return: None"""

        data = {
            "action": "move",
            "token": await self.fetch_token(type="csrf"),
            "from": frompage,
            "to": topage,
            "format": "json",
        }
        data.update(kwargs)
        act = await self.client.post(url=self.api, data=data, headers=self.headers)
        logger.info(f"已向{self.sitename}发送移动页面[[{frompage}]]至[[{topage}]]的请求。")
        act.raise_for_status()
        act: dict = act.json()
        if act.get("edit", {}).get("result", None) is not None:
            if act["move"]["from"] and act["move"]["to"]:
                logger.success(f"成功移动页面[[{frompage}]]至[[{topage}]]！")
            else:
                logger.debug(act)
                return False
        else:
            logger.debug(act)
            return False

    async def delete_page(self, title: str, **kwargs):
        """移动一个页面
        :use: await bot.delete_page(title, reason)
        :params: title(`str`) : 删除页面的标题
        :params: reason(`str`) : 删除理由
        :params: ...
        :return: None"""

        data = {
            "action": "delete",
            "token": await self.fetch_token(type="csrf"),
            "title": title,
            "format": "json",
        }
        data.update(kwargs)
        act = await self.client.post(url=self.api, data=data, headers=self.headers)
        logger.info(f"已向{self.sitename}发送删除页面[[{title}]]的请求。")
        act.raise_for_status()
        act: dict = act.json()
        if act.get("edit", {}).get("result", None) is not None:
            if act["delete"]["title"]:
                logger.success(f"成功删除页面[[{title}]]！")
            else:
                logger.debug(act)
                return False
        else:
            logger.debug(act)
            return False

    async def parse(self, title, **kwargs):
        """解析"""

        data = {"format": "json", "page": title, "action": "parse"}
        data.update(kwargs)
        act = await self.client.post(url=self.api, data=data, headers=self.headers)
        act.raise_for_status()
        return act.json()

    async def get_sections(self, title: str) -> Union[WikiSectionList, bool]:
        result = await self.parse(title=title, prop="sections")
        result = result["parse"]["sections"]
        result_list = []
        for i in result:
            result_list.append(i["line"])
        if result_list:
            return WikiSectionList(result_list)
        else:
            logger.warning(f"页面 [[{title}]] 中没有子章节！")
            return False

    async def deal_flow(self, title, cotmoderationState, cotreason="标记"):
        data = {
            "action": "flow",
            "page": str(title),
            "submodule": "lock-topic",
            "cotmoderationState": cotmoderationState,
            "cotreason": cotreason,
            "format": "json",
            "token": await self.fetch_token(type="csrf"),
        }
        act = await self.client.post(url=self.api, data=data, headers=self.headers)
        act.raise_for_status()
        act = act.json()
        logger.success(
            f"{cotmoderationState} the flow {title} successfully.({cotreason})"
        )

    async def reply_flow(self, title, content, **kwargs):
        data = {
            "action": "flow",
            "submodule": "reply",
            "page": title,
            "repreplyTo": str(title),
            "repcontent": str(content),
            "repformat": "wikitext",
            "format": "json",
            "token": await self.fetch_token(type="csrf"),
        }
        data.update(kwargs)
        act = await self.client.post(url=self.api, data=data, headers=self.headers)
        act.raise_for_status()
        act = act.json()
        logger.success(f"Reply the flow {title} successfully.")

    async def rc(
        self,
        namespace: str = "0",
        limit: Union[str, int] = 50,
        days: Union[str, int] = 5,
    ):
        from xmltodict import parse as XMLParse

        data = {
            "action": "feedrecentchanges",
            "days": days,
            "feedformat": "atom",
            "limit": limit,
            "namespace": namespace,
            "urlversion": "2",
        }
        act = await self.client.post(
            url=self.index, data=data, headers=self.headers
        )
        act.raise_for_status()
        act = act.json()
        return XMLParse(act.content)["feed"]["entry"]

    async def search(
        self, txt: str, namespace: str = "0", sroffset: str = "0", **kwargs
    ):
        data = {
            "action": "query",
            "list": "search",
            "srsearch": txt,
            "srlimit": "max",
            "utf8": "",
            "srnamespace": namespace,
            "srwhat": "text",
            "sroffset": sroffset,
            "format": "json",
        }
        data.update(kwargs)
        act = await self.client.post(url=self.api, data=data, headers=self.headers)
        act.raise_for_status()
        act = act.json()
        rl = []
        if act["query"]["search"] is not False:
            for i in act["query"]["search"]:
                rl.append(i["title"])
        if "continue" in act:
            temp = await self.search(
                txt=txt, namespace=namespace, sroffset=(int(sroffset) + 1), **kwargs
            )
            for i in temp:
                rl.append(i)
        return rl

    async def ask(self, query: str, api_version: int = 2):
        data = {
            "action": "ask",
            "query": query,
            "api_version": api_version,
            "format": "json",
        }
        act = await self.client.post(url=self.api, data=data, headers=self.headers)
        act.raise_for_status()
        act = act.json()
        return act["query"]

    async def protect(
        self, title, protections, expiry: str = "infinite", reason: str = "", **kwargs
    ):
        data = {
            "action": "protect",
            "format": "json",
            "title": title,
            "protections": protections,
            "expiry": expiry,
            "reason": reason,
        }
        data.update(kwargs)
        data["token"] = await self.fetch_token(type="csrf")
        # data["reason"] += " //Protect by Bot."
        act = await self.client.post(url=self.api, data=data, headers=self.headers)
        act.raise_for_status()
        act = act.json()
        return act["protect"]

    async def user_contributions(
        self, user: str, uccontinue: str = "", **kwargs
    ) -> list:
        data = {
            "action": "query",
            "list": "usercontribs",
            "ucuser": user,
            "uclimit": "max",
            "ucprop": "title|ids|size|sizediff|tags|timestamp",
            "ucnamespace": "*",
            "format": "json",
        }
        if uccontinue != "":
            data["uccontinue"] = uccontinue
        data.update(kwargs)
        act = await self.client.post(url=self.api, data=data, headers=self.headers)
        act.raise_for_status()
        act = act.json()
        rl = []
        if act["query"]["usercontribs"] is not False:
            for i in act["query"]["usercontribs"]:
                rl.append(i)
        if "continue" in act:
            temp = await self.user_contributions(
                user=user, uccontinue=act["continue"]["uccontinue"], **kwargs
            )
            for i in temp:
                rl.append(i)
        return rl
