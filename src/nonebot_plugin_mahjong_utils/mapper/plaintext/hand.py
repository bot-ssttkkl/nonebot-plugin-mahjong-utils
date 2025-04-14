from typing import TextIO, Optional, Sequence

from mahjong_utils.models.furo import Furo
from mahjong_utils.models.tile import Tile, tiles_text


def map_hand(io: TextIO, tiles: Sequence[Tile], furo: Optional[Sequence[Furo]] = None):
    if len(tiles) % 3 == 2:
        got = tiles[-1]
        tiles = [*sorted(tiles[:-1]), got]
    else:
        tiles = sorted(tiles)

    io.write(tiles_text(tiles))
    io.write(" ")

    if furo:
        for fr in furo:
            io.write(str(fr))
            io.write(" ")
