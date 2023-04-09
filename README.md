## mwbot(Python)
mwbot是一个基于Python的异步 Mediawiki API库，同时封装了用于[PRTS wiki](https://prts.wiki)的[部分方法](https://github.com/GuGuMur/mwbot/blob/main/mwbot/arktool.py)

## 快速使用
### 前备工作
#### 安装
    pip install mwbot -i https://pypi.org/simple/
#### 获取Bot应有的参数
1. 前往对应wiki的 特殊:版本 页面获取wiki的index.php, api.php的路径
2. 前往对应wiki的 特殊:BotPasswords 创建一套机器人密码

<details><summary>详细过程</summary>

1. 填入“机器人名称”。（如：BotName）

2. 选择下方的权限
    - 这将能够限制通过机器人密码登录后的账户权限，尤其是当你的人工账户和机器人是同一账户时，这将有效保护你的账户。
    - bot只能使用您选中的与您拥有的权限的交集。
    
3. 创建成功，获得机器人密码，你将有两种登录机器人的方式，任意一种都能登录至机器人账户：
    - 登录名为User@BotName，密码为BotPassword
    - 登录名为User，密码为BotName@BotPassword
</details>

### 开始使用
```python
from mwbot import Bot
import asyncio
async def main():
    bot = Bot(
            sitename="my_wiki", # 替换为你所在的Wiki名，便于参考
            api="api", # 替换为对应Wiki的api.php路径
            index="index", #替换为对应Wiki的index.php路径
            username="User",
            password="BotName@BotPassword")
            # 将username和password替换为你刚才获得的机器人登录名和密码
            # 你只能选择一种登录方式，并填入对应登录方式的登录名和密码
    await bot.login()
    
    # 样例：打印页面 用户:User 的内容
    r = await bot.get_page_text(title="用户:User")
    print(r)

if __name__ == "__main__":
    asyncio.run(main())
```
## 深入
* [示例](https://github.com/GuGuMur/mwbot/tree/main/examples)
* [文档](https://gugumur.github.io/mwbot)
