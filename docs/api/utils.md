本模块储存了一些通用的工具。
#### _method_ `get_all_links(content)`  :id=method-get_all_links
* 说明：本方法传入一段`wikitext`，返回这段wikitext中所有的链接。
* 参数
    * `content`(`str`)：一段wikitext
* 返回值：`list`

<details><summary>示例</summary>

```python
...
wikitext = """
[[页面1]]
[[页面2|xxx]]
[[页面3|jbsh]]
""" 
pagelist = get_all_links(content=wikitext)
# 从该段wikitext获取所有的页面
# pagelist = ['页面1', '页面2', '页面3']
```
</details>