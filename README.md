## mwbot(Python)

## 入门
### 前备工作
#### 安装
    pip install -i https://pypi.org/simple/ mwbot
#### 获取Bot应有的参数
1. 前往对应wiki的 特殊:版本 页面获取wiki的index.php, api.php的路径
2. 前往对应wiki的 特殊:BotPasswords 创建一套机器人密码
<details><summary>详细过程</summary>
1. 填入“机器人名称”XXX
2. 选择下方的权限（bot只能使用您选中的与您拥有的权限的交集）
3. 创建成功：此时机器人名称为User@XXX(或User)，密码为YYY(或XXX@YYY)
</details>

### 开始使用
```python
from mwbot import Bot
import asyncio
async def main():
    bot = Bot(
            sitename="my_wiki",
            api="api",
            index="index",
            username="User", # 或User@XXX
            password="XXX@YYY") # 或YYY
    await bot.login()
    r = await bot.get_section(page_name="用户:User")
    print(r)
    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
```
## 深入
* [API](docs/api.md)