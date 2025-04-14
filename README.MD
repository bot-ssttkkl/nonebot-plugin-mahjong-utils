nonebot-plugin-mahjong-utils
========

## 安装

```shell
nb plugin install nonebot-plugin-mahjong-utils
```

如果需要麻将牌截图识别功能，需要额外安装：

```shell
pip install nonebot-plugin-mahjong-utils[detect]
```

## 功能

### 手牌分析

`/牌理 <手牌代码> [...附加选项]`

- 输入手牌代码，根据输入手牌输出向听数（未摸牌状态）、牌理（已摸牌、未和牌状态）、副露分析（未摸牌状态+他家打出的牌）或和牌分析（已摸牌、已和牌状态）。

- 开启嗅探模式时（默认开启），可直接输入手牌代码：`<手牌代码> [...附加选项]`

- 支持图像识别模式，从截图中识别手牌进行计算。
只保证对雀魂截图的识别率 ~~因为训练模型只喂了雀魂截图~~ 。效果如下图所示：

![shanten_img_detect.png](img/shanten_img_detect.png)

#### 向听数分析（未摸牌状态）

输入的手牌为3k+1张时。

计算向听数与进张。一向听的手牌还会计算好型与愚型进张数。

![shanten_1233334679m_input.png](img%2Fshanten_1233334679m_input.png)

![shanten_1233334679m.jpg](img%2Fshanten_1233334679m.jpg)

#### 牌理（已摸牌状态）

输入的手牌为3k+2张，且未和牌（向听数大于-1）时。

对每种打法（包括打出与暗杠）计算向听数与进张。一向听的手牌还会计算好型与愚型进张数。

![shanten_34567778m123457p_input.png](img%2Fshanten_34567778m123457p_input.png)

![shanten_34567778m123457p.png](img%2Fshanten_34567778m123457p.png)

#### 副露分析（未摸牌状态+他家打出的牌）

格式：`手牌代码<上家打出的牌`、`手牌代码^对家打出的牌`或`手牌代码>下家打出的牌`，其中输入的手牌为3k+1张。

~~实际上对家打出和下家打出是一样的（不能吃），这里区分是为了命令的工整性~~

对每种打法（包括吃、碰、大明杠与PASS）计算向听数与进张。一向听的手牌还会计算好型与愚型进张数。

![furo_335678m3457p_7m_input.png](img%2Ffuro_335678m3457p_7m_input.png)

![furo_335678m3457p_7m.jpg](img%2Ffuro_335678m3457p_7m.jpg)

#### 和牌分析

输入的手牌为3k+2张，且已和牌（向听数等于-1）时。

手牌代码的最后一张牌作为所和的牌，手牌代码后可通过空格分割输入副露、自风、场风、dora、额外役。暗杠通过0990m的格式输入。

![hora_11123456789999p_input.png](img%2Fhora_11123456789999p_input.png)

![hora_11123456789999p.jpg](img%2Fhora_11123456789999p.jpg)

### 番符点数查询

`/番符 <x>番<y>符`

- 输入x番y符，输出亲家/子家的自摸/荣和得点

- 开启嗅探模式时（默认开启），可直接输入番符数目：`<x>番<y>符`

![3han40hu.png](img%2F3han40hu.png)

## 配置项

### mahjong_utils_send_image

将结果以图片形式发送，设置为False可节省图片渲染和发送时间，提高响应速度

默认值：`True`

### mahjong_utils_sniff_mode

开启嗅探模式，支持直接输入手牌代码触发指令

默认值：`True`

### mahjong_utils_command_mode

开启指令模式，支持通过指令方式触发指令

默认值：`True`

## 优化计算用时

参考：[https://github.com/ssttkkl/mahjong-utils/blob/main/python-lib/README.md#%E6%8C%87%E5%AE%9A%E7%BB%91%E5%AE%9A%E6%96%B9%E5%BC%8F]

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
