from dataclasses import dataclass

from war_deck import WarDeck


class WarGame:
    def __init__(self, player1: WarDeck, player2):
        self.player1 = player1
        self.player2 = player2

    def round(self):
        card1 = self.player1.draw_card()
        card2 = self.player2.draw_card()

        if card1 == card2:
            return self.war([card1], [card2])
        winner = -1
        if card1 > card2:
            self.player1.add_to_discard(card1, card2)
            winner = 1
        elif card2 > card1:
            self.player2.add_to_discard(card1, card2)
            winner = 2
        return RoundResult([card1], [card2], winner)

    def war(self, player1_cards, player2_cards):
        if not self.player1.has_cards or not self.player2.has_cards:
            return
        if self.player1.has_cards:
            player1_cards.extend([self.player1.draw_card() for _ in range(3)])
        if self.player2.has_cards:
            player2_cards.extend([self.player2.draw_card() for _ in range(3)])

        if player1_cards[-1] == player2_cards[-1]:
            return self.war(player1_cards, player2_cards)
        winner = -1
        if player1_cards[-1] > player2_cards[-1]:
            self.player1.add_to_discard(*(player1_cards + player2_cards))
            winner = 1
        elif player2_cards[-1] > player1_cards[-1]:
            self.player2.add_to_discard(*(player1_cards + player2_cards))
            winner = 2
        return RoundResult(player1_cards, player2_cards, winner, is_war=True)

    def is_over(self):
        return not self.player1.has_cards or not self.player2.has_cards


@dataclass
class RoundResult:
    player1_cards: list[str]
    player2_cards: list[str]
    winner: int
    is_war: bool = False
