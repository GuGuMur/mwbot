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
import asyncio
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
    * `type`(str)：所需的token类型（如所需`csrftoken`，则传入`csrf`）
* 返回值：`str`
* 参见：[MW:API:Tokens](https://www.mediawiki.org/wiki/API:Tokens)

<details><summary>示例</summary>

```python
...
token = await bot.fetch_token(type="login") #用于登录的token
token = await bot.fetch_token(type="csrf")  #用于编辑的token
```
</details>


#### _async method_ `login()`  :id=method-bot-login
* 说明：本函数用于登录站点。**必须调用本函数后才能进行后续操作**。
* 参见：[MW:API:Login](https://www.mediawiki.org/wiki/API:Login)

<details><summary>示例</summary>

```python
...
bot.login()
```
</details>