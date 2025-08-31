本模块定义了用于明日方舟国服wiki-[PRTS wiki](https://prts.wiki/)编辑的工具。
### 前备工作

1. 本地`git clone git@github.com:Kengxxiao/ArknightsGameData.git`
2. 记录其中 [zh_CN/gamedata](https://github.com/Kengxxiao/ArknightsGameData/tree/master/zh_CN/gamedata) 的路径
> 假设我在`/home/bot`目录clone了该仓库，则路径为`/home/bot/ArknightsGameData/zh_CN/gamedata`
3. 
 ```python
from mwbot import arktool
arktool.GameDataPosition = "您获取到的路径"
...
```

### 具体文档

#### _method_ `get_item_name(id)`  :id=method-get_item_name
* 说明：输入`id`，获取对应道具的名称
* 参数
    * `id`(`str`)：道具ID。
* 参考：[/excel/item_table.json](https://github.com/Kengxxiao/ArknightsGameData/blob/master/zh_CN/gamedata/excel/item_table.json)
* 返回值：对应道具的名称(`str`)

<details><summary>示例</summary>

```python
...
arktool.get_item_name(id="30012") #固源岩
```
</details>
