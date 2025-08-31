首先，请你回忆一下我们是如何在一个`Mediawiki`网站中进行编辑的：
1. 找到一个wiki
2. 注册一个账号，设置密码并登录(WMF项目中可以直接使用IP匿名用户编辑)
3. 打开一个页面
4. 点击页面顶部/某个章节标题旁的`编辑`/`编辑源代码`，获取对应页面(章节)的wikitext
5. 进行编辑
6. 提交编辑
7. 自动刷新页面并得到反馈

那么，我们的mwbot的编辑过程与此类似：
1. [建立python文件的基本架构](fornew/quickstart.md)
2. 找到一个wiki，获取`api.php`, `index.php`的路径
3. 注册一个(`Bot`)账号并获取一套BotPasswords
4. 获取一个页面的文本(`text = await bot.get_page_text(title=x,sextion=y/"")`)
5. 对这个文本进行编辑
    > 假设我们在第20行后加入了一段文字，这个过程可以等效理解成替换第20行的文本并加入内容
6. 提交编辑(`await bot.edit_page(title=x,section=y,text=text,...`))
7. 获得Logger的反馈：INFO类为成功，DEBUG类为*不正常*

思维转变以后，请你阅读之后的文档了解mwbot的更多用法！