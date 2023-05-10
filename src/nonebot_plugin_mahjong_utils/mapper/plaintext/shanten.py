from collections import defaultdict
from typing import TextIO, cast, List

from mahjong_utils.models.tile import tiles_text, Tile
from mahjong_utils.shanten import ShantenWithoutGot, CommonShantenResult, FuroChanceShantenResult, ShantenWithFuroChance

from nonebot_plugin_mahjong_utils.mapper.plaintext.hand import map_hand


def map_shanten_without_got(io: TextIO, shanten: ShantenWithoutGot):
    if shanten.shanten == 1:
        io.write(
            f"进张：{tiles_text(sorted(shanten.advance))} ({shanten.advance_num}张，好型{shanten.good_shape_advance_num}张)")
    else:
        io.write(f"进张：{tiles_text(sorted(shanten.advance))} ({shanten.advance_num}张)")

    if shanten.improvement:
        io.write("\n改良：")

        improvement = []

        for t in shanten.improvement:
            imp = t, [x.discard for x in shanten.improvement[t]], shanten.improvement[t][0].advance_num
            improvement.append(imp)

        improvement.sort(key=lambda x: x[0])

        for i, (t, discard, advance_num) in enumerate(improvement):
            io.write(f"{t}（打{'/'.join(map(str, discard))}，听{advance_num}张）")
            if i != len(improvement) - 1:
                io.write("\n")


def map_common_shanten_result(io: TextIO, result: CommonShantenResult, tiles: List[Tile]):
    map_hand(io, tiles)
    io.write('\n\n')

    if not result.with_got:
        if result.shanten == -1:
            io.write("和牌\n")
        elif result.shanten == 0:
            io.write("听牌：\n")
        else:
            io.write(f"{result.shanten}向听：\n")

        map_shanten_without_got(io, cast(ShantenWithoutGot, result.shanten_info))
    else:
        grouped_shanten = defaultdict(dict)

        for discard, shanten_after_discard in result.discard_to_advance.items():
            grouped_shanten[shanten_after_discard.shanten][("discard", discard)] = shanten_after_discard

        for ankan, ankan_after_discard in result.ankan_to_advance.items():
            grouped_shanten[ankan_after_discard.shanten][("ankan", ankan)] = ankan_after_discard

        records = 0
        tot_records = sum(map(lambda x: len(x), grouped_shanten.values()))

        for shanten_num in sorted(grouped_shanten.keys()):
            if result.shanten == -1:
                io.write("和牌\n")
                break
            elif shanten_num == 0:
                io.write("听牌：\n")
            elif shanten_num != result.shanten:
                io.write(f"{shanten_num}向听（退向）：\n")
            else:
                io.write(f"{shanten_num}向听：\n")

            ordered_shanten = sorted(grouped_shanten[shanten_num].items(), key=lambda x: x[1].advance_num, reverse=True)

            for action, shanten_after_discard in ordered_shanten:
                if action[0] == 'discard':
                    io.write(f"[打{action[1]}]  ")
                elif action[0] == 'ankan':
                    io.write(f"[暗杠{action[1]}]  ")

                map_shanten_without_got(io, shanten_after_discard)
                io.write("\n")

                records += 1

                if records >= 10:
                    break

            io.write("\n")

            if records >= 10:
                break

        if records < tot_records:
            io.write("（只显示最优的前10种打法）")


def map_furo_chance_shanten_result(io: TextIO, result: FuroChanceShantenResult, tiles: List[Tile], chance_tile: Tile,
                                   tile_from: int):
    map_hand(io, tiles)
    if tile_from == 1:
        io.write("下家打")
    elif tile_from == 2:
        io.write("对家打")
    elif tile_from == 3:
        io.write("上家打")
    io.write(str(chance_tile))
    io.write('\n\n')

    grouped_shanten = defaultdict(dict)

    shanten_info = cast(ShantenWithFuroChance, result.shanten_info)

    if shanten_info.pass_ is not None:
        grouped_shanten[shanten_info.pass_.shanten][("pass",)] = shanten_info.pass_

    if shanten_info.pon is not None:
        for discard, shanten_after_pon_discard in shanten_info.pon.discard_to_advance.items():
            grouped_shanten[shanten_after_pon_discard.shanten][("pon", discard)] = shanten_after_pon_discard

    if shanten_info.minkan is not None:
        grouped_shanten[shanten_info.minkan.shanten][("minkan",)] = shanten_info.minkan

    for tatsu, shanten_after_chi in shanten_info.chi.items():
        for discard, shanten_after_chi_discard in shanten_after_chi.discard_to_advance.items():
            grouped_shanten[shanten_after_chi_discard.shanten][("chi", tatsu, discard)] = shanten_after_chi_discard

    records = 0
    tot_records = sum(map(lambda x: len(x), grouped_shanten.values()))

    for shanten_num in sorted(grouped_shanten.keys()):
        if result.shanten == -1:
            io.write("和牌\n")
            break
        elif shanten_num == 0:
            io.write("听牌：\n")
        elif shanten_num != result.shanten:
            io.write(f"{shanten_num}向听（退向）：\n")
        else:
            io.write(f"{shanten_num}向听：\n")

        ordered_shanten = sorted(grouped_shanten[shanten_num].items(), key=lambda x: x[1].advance_num, reverse=True)

        for action, shanten_after_action in ordered_shanten:
            if action[0] == 'pass':
                io.write("[PASS]  ")
            elif action[0] == 'chi':
                io.write(f"[{action[1]}吃打{action[2]}]  ")
            elif action[0] == 'pon':
                io.write(f"[碰打{action[1]}]  ")
            elif action[0] == 'minkan':
                io.write("[杠]  ")

            map_shanten_without_got(io, shanten_after_action)
            io.write("\n")

            records += 1

            if records >= 10:
                break

        io.write("\n")

        if records >= 10:
            break

    if records < tot_records:
        io.write("（只显示最优的前10种打法）")
