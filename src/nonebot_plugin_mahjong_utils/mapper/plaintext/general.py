from mahjong_utils.models.wind import Wind
from mahjong_utils.yaku.common import *
from mahjong_utils.yaku.extra import *
from mahjong_utils.yaku.yakuman import *

num_mapping = {
    1: "一",
    2: "两",
    3: "三",
    4: "四",
    5: "五",
    6: "六"
}

wind_mapping = {
    Wind.east: "东",
    Wind.south: "南",
    Wind.west: "西",
    Wind.north: "北"
}

yaku_mapping = {
    tsumo: "门清自摸",
    pinhu: "平和",
    tanyao: "断幺",
    ipe: "一杯口",
    self_wind: "自风",
    round_wind: "场风",
    haku: "白",
    hatsu: "发",
    chun: "中",
    sanshoku: "三色同顺",
    ittsu: "一气通贯",
    chanta: "混全带幺九",
    chitoi: "七对子",
    toitoi: "对对和",
    sananko: "三暗刻",
    honroto: "混老头",
    sandoko: "三色同刻",
    sankantsu: "三杠子",
    shosangen: "小三元",
    honitsu: "混一色",
    junchan: "纯全带幺九",
    ryanpe: "两杯口",
    chinitsu: "清一色",
    richi: "立直",
    ippatsu: "一发",
    rinshan: "岭上开花",
    chankan: "枪杠",
    haitei: "海底摸月",
    houtei: "河底捞鱼",
    w_richi: "两立直",
    tenhou: "天和",
    chihou: "地和",
    kokushi: "国士无双",
    suanko: "四暗刻",
    daisangen: "大三元",
    tsuiso: "字一色",
    shousushi: "小四喜",
    lyuiso: "绿一色",
    chinroto: "清老头",
    sukantsu: "四杠子",
    churen: "九莲宝灯",
    daisushi: "大四喜",
    churen_nine_waiting: "纯正九莲宝灯",
    suanko_tanki: "四暗刻单骑",
    kokushi_thirteen_waiting: "国士无双十三面"
}
