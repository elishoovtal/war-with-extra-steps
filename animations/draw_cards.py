import pyxel

from animation import Animation, test_animation
from war_deck import CardValue

CARD_ICON_SIZE = 16
CARD_ICON_PADDING = 3
SHUFFLE_EXTEND_OFFSET = 4
VALUE_TO_BITMAP_LOCATION = {
    CardValue.A: (0, 0),
    CardValue.K: (1, 0),
    CardValue.Q: (2, 0),
    CardValue.J: (3, 0),
    CardValue.TEN: (0, 1),
    CardValue.NINE: (1, 1),
    CardValue.EIGHT: (2, 1),
    CardValue.SEVEN: (3, 1),
    CardValue.SIX: (0, 2),
    CardValue.FIVE: (1, 2),
    CardValue.FOUR: (2, 2),
    CardValue.THREE: (3, 2),
    CardValue.TWO: (0, 3),
    CardValue.CARD_BACK: (1, 3),
}


def draw_card(location: tuple[int, int], card: CardValue, padding=0):
    start_x, start_y = location
    cardx, cardy = VALUE_TO_BITMAP_LOCATION[card]
    pyxel.blt(start_x, start_y, 0,
              cardx * CARD_ICON_SIZE + padding, cardy * CARD_ICON_SIZE, CARD_ICON_SIZE, CARD_ICON_SIZE)


class DeckAnimation:
    def __init__(self, location: tuple[int, int]):
        self.location = location

    def draw(self):
        draw_card(self.location, CardValue.CARD_BACK)

    def shuffle_extended_frame(self):
        x, y = self.location
        draw_card(self.location, CardValue.CARD_BACK, CARD_ICON_PADDING)
        draw_card((x, y - SHUFFLE_EXTEND_OFFSET),
                  CardValue.CARD_BACK, CARD_ICON_PADDING)

    def shuffle_switched_frame(self):
        x, y = self.location
        draw_card((x, y - SHUFFLE_EXTEND_OFFSET),
                  CardValue.CARD_BACK, CARD_ICON_PADDING)
        draw_card(self.location, CardValue.CARD_BACK, CARD_ICON_PADDING)

    @property
    def shuffle_animation(self) -> Animation:
        return Animation({0: self.draw,
                          4: self.shuffle_extended_frame,
                          8: self.shuffle_switched_frame,
                          12: self.draw}, self.location)


if __name__ == '__main__':
    test_animation(DeckAnimation((10, 10)).shuffle_animation)
