from typing import Callable
import pyxel


class Animation:
    def __init__(self, frame_map: dict[int, Callable[[int, int], None]],
                 initial_location: tuple[int, int], repeat: bool = True):
        self.x, self.y = initial_location
        self.frame_map = frame_map
        self.repeat = repeat

    @property
    def cycle_size(self) -> int:
        return len(self.frame_map)

    def draw(self, frame: int):
        if not self.repeat and frame >= self.cycle_size:
            return
        self.frame_map[frame % self.cycle_size](self.x, self.y)


def test_animation(animation: Animation):
    pyxel.run(lambda: None, lambda: animation.draw(pyxel.frame_count))
