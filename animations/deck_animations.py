import pyxel

from animation import Animation, DurationFrameMap, FrameMap, test_animation
from war_deck import CardValue

CARD_ICON_SIZE = 16
SHUFFLE_EXTEND_OFFSET = 6
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


class ShuffleAnimation(Animation):
    def __init__(self, initial_location: tuple[int, int], repeat: bool = True, background: int | None = None):
        super().__init__(initial_location, repeat)
        self.x, self.y = initial_location
        self.location = initial_location
        self.background = background

    def neutral_state(self):
        if self.background is not None:
            pyxel.rect(self.x, self.y - SHUFFLE_EXTEND_OFFSET, CARD_ICON_SIZE,
                       CARD_ICON_SIZE + SHUFFLE_EXTEND_OFFSET, self.background)
        draw_card(self.location, CardValue.CARD_BACK)

    def shuffle_extended_frame(self):
        draw_card(self.location, CardValue.CARD_BACK)
        draw_card((self.x, self.y - SHUFFLE_EXTEND_OFFSET),
                  CardValue.CARD_BACK)

    def shuffle_switched_frame(self):
        draw_card((self.x, self.y - SHUFFLE_EXTEND_OFFSET),
                  CardValue.CARD_BACK)
        draw_card(self.location, CardValue.CARD_BACK)

    @property
    def duration_frame_map(self) -> DurationFrameMap:
        return {(0, 4): self.neutral_state,
                (4, 10): self.shuffle_extended_frame,
                (10, 16): self.shuffle_switched_frame,
                (16, 22): self.shuffle_extended_frame,
                (22, 28): self.shuffle_switched_frame,
                (28, 30): self.neutral_state}

    @property
    def frame_map(self) -> FrameMap:
        return self.flatten_frame_map(self.duration_frame_map)


if __name__ == '__main__':
    test_animation(ShuffleAnimation((10, 10), background=0))
