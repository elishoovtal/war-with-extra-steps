import random
from enum import IntEnum


class CardValue(IntEnum):
    A = 14
    K = 13
    Q = 12
    J = 11
    TEN = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2
    CARD_BACK = -1000


CARD_OPTIONS = [CardValue.A, CardValue.K, CardValue.Q, CardValue.J, CardValue.TEN,
                CardValue.NINE, CardValue.EIGHT, CardValue.SEVEN, CardValue.SIX, CardValue.FIVE,
                CardValue.FOUR, CardValue.THREE, CardValue.TWO]


class WarDeck:
    def __init__(self):
        self.deck = CARD_OPTIONS * 4
        self.discard: list[str] = []
        random.shuffle(self.deck)

    def draw_card(self) -> str:
        if not self.deck:
            self.deck = self.discard
            self.discard = []
            random.shuffle(self.deck)
        return self.deck.pop()

    def add_to_discard(self, *cards: str) -> None:
        self.discard.extend(cards)

    @property
    def has_cards(self) -> bool:
        return self.deck or self.discard
