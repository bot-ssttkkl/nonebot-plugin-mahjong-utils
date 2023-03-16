from typing import TextIO, Optional

from mahjong_utils.point_by_han_hu import ParentPoint, ChildPoint


def get_point_tag(point: int) -> str:
    if point == 32000 * 6:
        return '6倍役满'
    elif point == 32000 * 5:
        return '5倍役满'
    elif point == 32000 * 4:
        return '4倍役满'
    elif point == 32000 * 3:
        return '3倍役满'
    elif point == 32000 * 2:
        return '2倍役满'
    elif point == 32000:
        return '役满'
    elif point == 24000:
        return '三倍满'
    elif point == 16000:
        return '倍满'
    elif point == 12000:
        return '跳满'
    elif point == 8000:
        return '满贯'
    else:
        return ''


def get_ron_text(ron: int, is_parent: bool) -> str:
    ron_text = f'{ron}点' if ron else ''
    ron_tag = get_point_tag(ron // 1.5 if is_parent else ron)
    if ron_tag:
        ron_text += f'（{ron_tag}）'
    return ron_text


def get_tsumo_text(tsumo_parent: int,
                   tsumo_child: int,
                   is_parent: bool) -> str:
    tsumo_text = ''
    if tsumo_child:
        tsumo_text += f'子家{tsumo_child}点'
    if tsumo_child and tsumo_parent:
        tsumo_text += '，'
    if tsumo_parent:
        tsumo_text += f'亲家{tsumo_parent}点'

    tsumo_total = tsumo_child * 3 if is_parent else tsumo_child * 2 + tsumo_parent

    tsumo_tag = '，'.join(filter(lambda x: x, [
        get_point_tag(tsumo_total // 1.5 if is_parent else tsumo_total),
        f'共{tsumo_total}点' if tsumo_total else ''
    ]))
    if tsumo_tag:
        tsumo_text += f'（{tsumo_tag}）'
    return tsumo_text


def get_han_hu_text(ron: int,
                    tsumo_parent: int,
                    tsumo_child: int,
                    is_parent: bool) -> str:
    ron_text = get_ron_text(ron, is_parent)
    tsumo_text = get_tsumo_text(tsumo_parent, tsumo_child, is_parent)

    if ron_text and tsumo_text:
        return f'荣和：{ron_text}\n自摸：{tsumo_text}'
    elif ron_text:
        return f'荣和：{ron_text}'
    elif tsumo_text:
        return f'自摸：{tsumo_text}'


def map_point_by_han_hu(io: TextIO,
                        parent_point: Optional[ParentPoint],
                        child_point: Optional[ChildPoint]):
    if parent_point is not None:
        io.write("亲家和牌时：\n")
        io.write(get_han_hu_text(parent_point.ron, 0, parent_point.tsumo, True))

    if parent_point and child_point:
        io.write('\n\n')

    if child_point is not None:
        io.write("子家和牌时：\n")
        io.write(get_han_hu_text(child_point.ron, child_point.tsumo_parent, child_point.tsumo_child, False))
