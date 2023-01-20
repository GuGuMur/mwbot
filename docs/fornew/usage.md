### 获取Bot信息
> 参见[快速上手](quickstart.md)

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
    # 我们后续的讲解均在此处进行
    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
```
#### 参考目录架构
```shell
.
├── 🐍 main.py
├── 📜 pagelist.txt
└── 📦 templates
```

### 获取某页面文本并对该页面进行批量替换
```python 
pagetext = await bot.get_page_text(title="Test")
#用于获取Test页面的信息
pagetext = pagetext.replace("test","Test")
#替换文本中所有`test`为`Test`
await bot.edit_page(title=Test,text=pagetext,summary="令全部test字样首字母大写")
# 编辑操作：标题为Test，文本为替换后的pagetext，摘要为"令全部test字样首字母大写//Edit via bot."
```

### 获取某个章节的内容并进行覆盖编辑
```python
sections = await bot.get_sections(title="Test")
# 获取一个页面中所有的章节
section_index = sections.index("标题")
# 获取该页面`标题`的序号
await bot.edit_page(title="test",text="OVERRIDE",summary=f"覆盖{section_index}章节",section=section_index)
# 编辑操作：标题为`Test`，章节序号为{section_index}，文本为"OVERRIDE"，摘要为"覆盖{section_index}章节//Edit via bot."
```

### 从pagelist.txt中获取所有的页面并进行刷新
```pagelist.txt
页面1
分类:2
模板:3
widget:4
Mediawiki:5
Topic:6
```

```python
from mwbot.utils import get_page_links_from_pagelist_txt
pagelist = get_page_links_from_pagelist_txt("当前文件夹的路径")
# 从 `./pagelist.txt` 获取每一行对应的页面
# pagelist = ['页面1', '分类:2', '模板:3', 'widget:4', 'Mediawiki:5', 'Topic:6']
for i in pagelist:
    await bot.purge(titles=i)
    # 刷新每一个页面
```

### 从一段wikitext中获取其中所有的页面并删除所有的`Test`章节
```python
from mwbot.utils import get_all_links
wikitext = """
[[页面1]]
[[页面2|xxx]]
[[页面3|jbsh]]
""" 
pagelist = get_all_links(content=wikitext)
# 从该段wikitext获取所有的页面
# pagelist = ['页面1', '页面2', '页面3']
for i in pagelist:
    sections = await bot.get_sections(title=i)
    # 获取一个页面中所有的章节
    section_index = sections.index("Test")
    # 获取该页面`标题`的序号
    await bot.edit_page(title="test",text="",summary=f"删除Test章节",section=section_index)
    # 编辑操作：标题为`i`，章节序号为{section_index}，文本为""，摘要为"删除Test章节//Edit via bot."
```
*施工中......*