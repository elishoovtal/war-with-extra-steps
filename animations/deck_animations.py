import functools

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


class DrawAnimation(Animation):
    def __init__(self, initial_location: tuple[int, int], repeat: bool = True, direction=(-1, 0), distance=5, background: int | None = None, final_card_value=CardValue.CARD_BACK):
        super().__init__(initial_location, repeat)
        self.background = background
        self.direction = direction
        self.distance = distance
        self.final_card_value = final_card_value
        self.direction_x, self.direction_y = self.direction
        if self.direction_x < 0:
            self.new_start_x = self.x + self.direction_x * self.distance
        else:
            self.new_start_x = self.x
        if self.direction_y < 0:
            self.new_start_y = self.y + self.direction_y * self.distance
        else:
            self.new_start_y = self.y
        self.full_animation_size_x = CARD_ICON_SIZE + self.distance * abs(self.direction_x)
        self.full_animation_size_y = CARD_ICON_SIZE + self.distance * abs(self.direction_y)
    
    def _distance_frame(self, distance, card_value: CardValue = CardValue.CARD_BACK):
        if self.background is not None:
            pyxel.rect(self.new_start_x, self.new_start_y, self.full_animation_size_x, self.full_animation_size_y, self.background)
        draw_card((self.x, self.y), CardValue.CARD_BACK)
        draw_card((self.x + self.direction_x * distance, self.y + self.direction_y * distance), card_value)

    @property
    def frame_map(self):
        return {
            i: functools.partial(self._distance_frame, i // 2)  # type: ignore
            for i in range(2 * self.distance)
        } | self.flatten_frame_map({
            (2 * self.distance, int(2.5 * self.distance) + 4): functools.partial(self._distance_frame, self.distance, self.final_card_value),
        })

if __name__ == '__main__':
    test_animation(DrawAnimation((40, 15), background=0, direction=(3, 0), distance=10, final_card_value=CardValue.A))
