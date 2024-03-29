本模块定义了MediawikiBot必需的主程序。
### _class_ `Bot(sitename,api,index,username,password)`  :id=class-bot
* 说明：实例化一个Bot程序，并基于他进行该站点的后续编辑。
* 参数
    * `sitename`(str)：对应站点的名称。
    * `api`(str)：[快速开始](../fornew/quickstart.md)中获取的api.php地址。
    * `index`(str)：[快速开始](../fornew/quickstart.md)中获取的index.php地址。
    * `username`(str)：[快速开始](../fornew/quickstart.md)中获取的机器人账号。
    * `password`(str)：[快速开始](../fornew/quickstart.md)中获取的机器人密码。

<details><summary>示例</summary>

```python
from mwbot import Bot
bot = Bot(
        sitename="my_wiki", 
        api="api", 
        index="index", 
        username="User",
        password="BotName@BotPassword")
```
</details>

#### _async method_ `fetch_token(type)`  :id=method-Bot-fetch_token
* 说明：本方法通过传入所需的token值来获取部分操作的必需参数。
* 参数
    * `type`(`str`)：所需的token类型（如所需`csrftoken`，则传入`csrf`）
* 返回值：`str`
* 参见：[MW:API:Tokens](https://www.mediawiki.org/wiki/API:Tokens)

<details><summary>示例</summary>

```python
...
token = await bot.fetch_token(type="login") #用于登录的token
token = await bot.fetch_token(type="csrf")  #用于编辑的token
```
</details>


#### _async func_ `login()`  :id=method-bot-login
* 说明：本函数用于登录站点。**必须调用本函数后才能进行后续操作**。
* 参见：[MW:API:Login](https://www.mediawiki.org/wiki/API:Login)

<details><summary>示例</summary>

```python
...
bot.login()
# > SUCCESS : 您已登录至{self.sitename}, {login["login"]["lgusername"]}！
# > DEBUG : 用户{self.username}登录至{self.sitename}中出现了错误。\n{<错误json>}: 
```
</details>

#### _async method_ `get_data(title)`  :id=method-bot-get_data
* 说明：本方法用于获取站点中某个页面的信息
* 参数
    * title(`str`)：页面名
* 参见：
    * [MW:API:Query](https://www.mediawiki.org/wiki/API:Query)
    * [MW:API:Meta](https://www.mediawiki.org/wiki/API:Meta)
    * [MW:API:Properties](https://www.mediawiki.org/wiki/API:Properties)
    * [MW:API:List](https://www.mediawiki.org/wiki/API:Lists)
    * 对应wiki的 `api.php?action=help&modules=query` 页面

<details><summary>返回值 & 示例</summary>

```python
...
title      = bot.get_data(title="用户:User")
           ={
                'pageid': 41211,                            # 页面ID
                'ns': 2,                                    # 页面对应名字空间
                'title':'用户:User',                        # 最后转换的页面名（例如：`User:user`在mediawiki-zh-cn版本中的结果是`用户:User`
                'revisions': [{
                    'slots': {
                        'main': {
                            'contentmodel': 'wikitext',     # 页面内容类型
                            'contentformat': 'text/x-wiki', # 页面内容格式
                            'content': '<wikitext>'
                        }
                    }
                }]
            } 
```
</details>

#### _async method_ `get_page_text(title,section)`  :id=method-bot-get_page_text
* 说明：本函数用于获取wiki某个页面（的某个段落的）文本。
* 参数
    * `title`(`str`)：某个页面的名称。
    * `section`(`Union[str,int]`)：章节标识符，可借助[`get_sections()`](#method-bot-get_sections)获取。

* 参考：[MW:Manual:Parameters_to_index.php#Raw](https://www.mediawiki.org/wiki/Manual:Parameters_to_index.php#Raw)
* 返回值：`str`/`None`

<details><summary>示例</summary>

```python
...
full_page = await bot.get_page_text(title="Test")
foreword_text = await bot.get_page_text(title="Test",section=0)
section_text = await bot.get_page_text(title="Test",section=x)
None_page = await bot.get_page_text(title=None)
# > RETURN：None
# > WARNING：请检查get_page_text传入的页面是否在{self.sitename}存在。
```
</details>

#### _async method_ `edit_page(title,text,summary="",**kwargs)`  :id=method-bot-edit_page
* 说明：本方法用于编辑某个页面（的指定章节）。
* 参数
    * ***必填项***`title`(`str`)：编辑页面的标题。
    * ***必填项***`text`(`str`)：处理后的页面内容
    * *选填项*`summary=""`(`str`)：编辑页面的摘要，会自动在后方加入`//Edit via Bot.`字样。
    * *参考项* `section`(`Union[str,int]`)：章节标识符（参见上方[`get_page_text`方法](#method-bot-get_page_text)，也可选用`new`字符创建新章节）。
    * *参考项* `sectiontitle`(`str`)：选用`section=new`时对应的章节标题。
    * ...
* 参考：[MW:API:Edit](https://www.mediawiki.org/wiki/API:Edit)

<details><summary>示例</summary>

```python
...
pagetext = await bot.get_page_text(title="Test").replace("test","Test")
await bot.edit_page(title=Test,text=pagetext,summary="令全部test字样首字母大写")
# > INFO : 已向{self.sitename}发送页面[[{title}]]的编辑请求。
# > wait...
# > LOGGER ：成功编辑页面 [[{title}]]。
```
</details>

#### _async method_ `create_page(title,text,summary)`  :id=method-bot-create_page
* 说明：用于**创建**一个页面
* 参数
    * `title`(`str`)：要编辑的标题
    * `text`(`str`)：编辑页面的内容
    * `summary=""`(`str`)：编辑页面的摘要，会自动在后方加入`//Edit via Bot.`字样。
* 返回值：`bool`：当页面创建成功时返回`True`，当要创建的页面中已有内容时返回`False`

<details><summary>示例</summary>

```python
...
await bot.create_page(title=old,text=xxx) 
# > RETURN : False
# > WARNING : 跳过创建[[{title}]]。
await bot.create_page(title=new,text=xxx) 
# > RETURN : True
```
</details>

#### _async method_ `upload_local(filepath,servername=None,text="",comment="",**kwargs)`  :id=method-bot-upload_local
* 说明：用于从**本地**上传一个文件。
* 参数
    * `filepath` (`str`) : 文件的本地路径
    * `servername=None` (`str`) : 文件上传至服务器后的名称。
        * 默认值为None，即不赋值时在函数执行时自动调整为`filepath`中的文件名
        * 赋值后则覆盖`filepath`中的文件名
    * `text=""` (`str`): 用于新文件的初始页面文本。
    * `comment=""` (`str`): 上传注释。如果没有指定text，那么它也被用于新文件的初始页面文本。
* 参考：[MW:API:Upload](https://www.mediawiki.org/wiki/API:Upload)
* 返回值：`bool`

<details><summary>示例</summary>

```python
...
b = await bot.upload_local(filepath="test.png",text="test",comment="comment")
# > RETURN : True
# > SUCCESS : '成功上传本地文件 {filepath} 至 [[{self.sitename}:文件:{servername}]]。'
e = await bot.upload_local(filepath="?",text="test",comment="comment")
# > RETURN : False
# > DEBUG : 上传本地文件 {filepath} 至 [[{self.sitename}:文件:{servername}]]失败。\n{<错误json>}
```
</details>

#### _async method_ `purge(title)`  :id=method-bot-purge
* 说明：本函数用于刷新一个页面。
* 参数
    * `title`(`str`)：刷新页面的标题
* 参考：[MW:API:Purge](https://www.mediawiki.org/wiki/API:Purge)

<details><summary>示例</summary>

```python
...
await bot.purge(title)
# > SUCCESS : 成功刷新页面 [[{title}]]。
```
</details>

#### _async method_ `get_sections(title)`  :id=method-bot-get_sections
* 说明：本函数用于获取一个**已存在的**页面中的所有标题。
> 假设有wikitext：
> 
> ```
本页面作为mwbot.Bot.get_page_text的示例页面。
== 二级标题 1 ==
114514
=== 三级标题 1 ===
2
==== 四级标题 1 ====
3
=== 三级标题 2 ===
4
== 二级标题 2 ==
> ```
> 
> 则页面全篇的序号为`*空*`
> 
> 页面从顶部到第一个标题之间的部分(即序言)的序号为`0`
> 
> **从上到下**标题的`序数`为对应序号
> > `二级标题 1` => `1`
> >
> > `三级标题 1` => `2` 
> >
> > `四级标题 1` => `3`
> >
> > `三级标题 2` => `4`
> >
> > `二级标题 2` => `5`
> >
> !>不是标题等级的序数！

* 参数
    * `title`(`str`)：待获取标题的页面名
* 返回值：[prototype.WikiSectionList](/api/prototype.md#WikiSectionList)/`False`

<details><summary>示例</summary>

```python
...
sections = await bot.get_sections(title="above")
# > sections:WikiSectionList = ["二级标题 1","三级标题 1","四级标题 1","三级标题 2","二级标题 2"]
index = section.index("二级标题 2")
# index:int = 5
sections = await bot.get_sections(title="not")
# WARNING ：页面 [[{title}]] 中没有子章节!
```
</details>

#### _async method_ `search(txt,namespace=0)`  :id=method-bot-search
* 说明：搜索站点并返回**所有**结果
* 参数
    * `txt`(`str`)：搜索的文本。
    * `namespace`(`str`)：搜索所在的名字空间（默认0，即主空间）
* 参考：[MW:API:Search](https://www.mediawiki.org/wiki/API:Search)
* 返回值：`list`

<details><summary>示例</summary>

```python
...
a = await bot.search(txt,namespace=0)
```
</details>

#### _async method_ `ask(query,api_version=3)`  :id=method-bot-ask
* 说明：使用SMW ask站点
* 参数
    * `query`(`str`):SMW语句
    * `api_version`(`int`):返回的结果类型
* 参考：[SMW:Help:API:Ask](https://www.semantic-mediawiki.org/wiki/Help:API:ask)
* 返回值：`Dict`

<details><summary>示例</summary>

```python
...
a = await bot.ask(query="",api_version=3)
# > 
```
</details>