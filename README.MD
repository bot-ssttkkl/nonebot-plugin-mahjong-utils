nonebot-plugin-mahjong-utils
========

## 功能

### 手牌分析

- 输入手牌代码，根据输入手牌输出向听数（未摸牌状态）、牌理（已摸牌、未和牌状态）、副露分析（未摸牌状态+他家打出的牌）或和牌分析（已摸牌、已和牌状态）。

#### 向听数分析（未摸牌状态）

输入的手牌为3k+1张时。

计算向听数与进张。一向听的手牌还会计算好型与愚型进张数。

![shanten_without_got](img/shanten_without_got.png)

#### 牌理（已摸牌状态）

输入的手牌为3k+2张，且未和牌（向听数大于-1）时。

对每种打法（包括打出与暗杠）计算向听数与进张。一向听的手牌还会计算好型与愚型进张数。

![shanten_with_got_1](img/shanten_with_got_1.png)

![shanten_with_got_2](img/shanten_with_got_2.png)

#### 副露分析（未摸牌状态+他家打出的牌）

格式：`手牌代码<上家打出的牌`、`手牌代码^对家打出的牌`或`手牌代码>下家打出的牌`，其中输入的手牌为3k+1张。

对每种打法（包括吃、碰、大明杠与PASS）计算向听数与进张。一向听的手牌还会计算好型与愚型进张数。

![furo_shanten_1](img/furo_shanten_1.png)

![furo_shanten_2](img/furo_shanten_2.png)

![furo_shanten_3](img/furo_shanten_3.png)

#### 和牌分析

输入的手牌为3k+2张，且已和牌（向听数等于-1）时。

手牌代码的最后一张牌作为所和的牌，手牌代码后可通过空格分割输入副露、自风、场风、dora、额外役。暗杠通过0990m的格式输入。

![hora_1](img/hora_1.png)

![hora_2](img/hora_2.png)

![hora_3](img/hora_3.png)

![hora_4](img/hora_4.png)

### 番符点数查询

- 输入x番y符，输出亲家/子家的自摸/荣和得点

## Special Thanks

-  [nonebot/nonebot2](https://github.com/nonebot/nonebot2)
-  [ssttkkl/mahjong-utils-py](https://github.com/ssttkkl/mahjong-utils-py) ~~我谢我自己~~

## LICENSE

MIT
