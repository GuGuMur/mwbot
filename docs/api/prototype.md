本模块定义了一些针对特殊场景的原型。
#### _class_ `WikiSectionList(ABC)`  :id=WikiSectionList
* 介绍：用于`Bot.get_section()`方法的列表类，覆写了`list.index()`方法，输出可直接用于`bot.edit(section)`的值。样例参见[`Bot.get_sections()`](/api/bot.md#method-bot-get_sections)