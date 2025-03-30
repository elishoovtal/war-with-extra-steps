import pyxel

from war_deck import CardValue, WarDeck
from war_game import WarGame

CARD_ICON_SIZE = 16
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
PLAYER1 = 1
PLAYER2 = 2
PLAYER1_START = (61, 66)
PLAYER2_START = (76, 66)
OFFSET_SIZE = 2
PADDING_SIZE = 3


class App:
    def __init__(self):
        basic_load()
        self.player1 = WarDeck()
        self.player2 = WarDeck()
        self.war_game = WarGame(self.player1, self.player2)
        self.in_play_cards = []
        self.current_round = None
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.frame_count % 15 == 0 and not self.war_game.is_over():
            self.current_round = self.war_game.round()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(47, 21, "WAR NEVER CHANGES", pyxel.frame_count % 16)
        pyxel.rect(10, 65, 40, 20, 7)
        pyxel.text(
            11, 66, f"Player1:\nDECK:{len(self.player1.deck)}\nDISCARD:{len(self.player1.discard)}", 0)
        pyxel.rect(100, 65, 40, 20, 7)
        pyxel.text(
            101, 66, f"Player2:\nDECK:{len(self.player2.deck)}\nDISCARD:{len(self.player2.discard)}", 0)
        if self.current_round:
            offset = 0
            if self.current_round.is_war:
                pyxel.text(70, 41, "WAR!", pyxel.frame_count % 16)
                draw_card(PLAYER1, offset - 1,
                          self.current_round.player1_cards[0], padding=PADDING_SIZE)
                for _ in range(len(self.current_round.player1_cards) - 2):
                    offset += 1
                    draw_card(PLAYER1, offset,
                              CardValue.CARD_BACK, padding=PADDING_SIZE)
                draw_card(PLAYER1, offset,
                          self.current_round.player1_cards[-1], padding=PADDING_SIZE)
                draw_card(PLAYER2, offset - 1,
                          self.current_round.player2_cards[0], padding=PADDING_SIZE)
                for _ in range(len(self.current_round.player2_cards) - 2):
                    offset += 1
                    draw_card(PLAYER2, offset, CardValue.CARD_BACK,
                              padding=PADDING_SIZE)
                draw_card(PLAYER2, offset,
                          self.current_round.player2_cards[-1], padding=PADDING_SIZE)
            else:
                draw_card(PLAYER1, 0, self.current_round.player1_cards[-1])
                draw_card(PLAYER2, 0, self.current_round.player2_cards[-1])


def draw_card(player: int, offset: int, card: CardValue, padding=0):
    player_start_x, player_start_y = PLAYER1_START if player == 1 else PLAYER2_START
    size = (CARD_ICON_SIZE, CARD_ICON_SIZE) if card != CardValue.CARD_BACK else (
        OFFSET_SIZE, CARD_ICON_SIZE)
    cardx, cardy = VALUE_TO_BITMAP_LOCATION[card]
    pyxel.blt(player_start_x + offset * OFFSET_SIZE, player_start_y, 0,
              cardx * CARD_ICON_SIZE + padding, cardy * CARD_ICON_SIZE, *size)


def basic_load():
    pyxel.init(160, 120, title="Hello Pyxel")
    pyxel.load("assets/card.pyxres")


def main():
    App()


if __name__ == "__main__":
    main()
