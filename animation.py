from abc import ABC, abstractmethod
from typing import Callable
import pyxel
from main import basic_load

type FrameMap = dict[int, Callable[[], None]]
type DurationFrameMap = dict[tuple[int, int], Callable[[], None]]


class Animation(ABC):
    def __init__(self,
                 initial_location: tuple[int, int], repeat: bool = True):
        self.x, self.y = initial_location
        self.location = initial_location
        self.repeat = repeat

    @property
    @abstractmethod
    def frame_map(self) -> FrameMap:
        pass

    @property
    def cycle_size(self) -> int:
        return len(self.frame_map)

    def draw(self, frame: int):
        if not self.repeat and frame >= self.cycle_size:
            return
        self.frame_map[frame % self.cycle_size]()

    @staticmethod
    def flatten_frame_map(frame_map: DurationFrameMap) -> FrameMap:
        return {
            frame: func for (start, end), func in frame_map.items()
            for frame in range(start, end)
        }


def test_animation(animation: Animation):
    basic_load()
    pyxel.run(lambda: None, lambda: animation.draw(pyxel.frame_count))
