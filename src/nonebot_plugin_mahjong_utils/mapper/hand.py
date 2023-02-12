from typing import TextIO, Optional

from mahjong_utils.models.hand_pattern import HandPattern, RegularHandPattern
from mahjong_utils.models.tile import tiles_text, Tile


def map_hand(io: TextIO, hand: HandPattern, *, got: Optional[Tile] = None):
    tiles = sorted(hand.tiles)

    if hasattr(hand, 'furo'):
        for fr in hand.furo:
            for t in fr.tiles:
                tiles.remove(t)

    if got is not None:
        tiles.remove(got)
        tiles.append(got)

    io.write(tiles_text(tiles))
    io.write(' ')

    if hasattr(hand, 'furo'):
        for fr in hand.furo:
            io.write(str(fr))
            io.write(' ')
