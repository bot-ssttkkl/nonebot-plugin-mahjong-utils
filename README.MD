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

~~实际上对家打出和下家打出是一样的（不能吃），这里区分是为了命令的工整性~~

对每种打法（包括吃、碰、大明杠与PASS）计算向听数与进张。一向听的手牌还会计算好型与愚型进张数。

![furo_shanten_1](img/furo_shanten_1.png)

![furo_shanten_2](img/furo_shanten_2.png)

![furo_shanten_3](img/furo_shanten_3.png)

#### 和牌分析

输入的手牌为3k+2张，且已和牌（向听数等于-1）时。

手牌代码的最后一张牌作为所和的牌，手牌代码后可通过空格分割输入副露、自风、场风、dora、额外役。暗杠通过0990m的格式输入。

![hora_1](img/hora_1.png)

### 番符点数查询

- 输入x番y符，输出亲家/子家的自摸/荣和得点

## 速度优化

目前本插件是以动态库形式调用[mahjong-utils](https://github.com/ssttkkl/mahjong-utils)的Native产物，实测在我的云服务器上对于已摸牌的一向听手牌，每次计算耗时约为1s上下。如果需要速度优化，可选切换为以HTTP形式调用JVM产物，计算耗时能降低到原来的50%左右。

安装Java环境（Java 11以上）。然后从 https://github.com/ssttkkl/mahjong-utils/releases/tag/v0.6.5 下载mahjong-utils-webapi-all.jar文件，放置到你的bot根目录即可。

## 配置项

### mahjong_utils_send_image

将结果以图片形式发送（若将此项设置为True，请安装nonebot-plugin-mahjong-utils[htmlrender]以安装必需依赖）

默认值：`False`

## Special Thanks

-  [nonebot/nonebot2](https://github.com/nonebot/nonebot2)
-  [ssttkkl/mahjong-utils](https://github.com/ssttkkl/mahjong-utils) ~~我谢我自己~~

## 在线乞讨

<details><summary>点击请我打两把maimai</summary>

![](https://github.com/ssttkkl/ssttkkl/blob/main/afdian-ssttkkl.jfif)

</details>

## LICENSE

> MIT License
> 
> Copyright (c) 2022 ssttkkl
> 
> Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
> 
> The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
> 
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
