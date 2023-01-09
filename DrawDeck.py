from CardWidget import CardWidget
import random


class DrawDeck:
    def __init__(self, parent):

        self.__cards = []
        for suite in [CardWidget.Type.Clubs, CardWidget.Type.Diamonds, CardWidget.Type.Hearts, CardWidget.Type.Spades]:
            for value in range(1, 14):
                card = CardWidget(board=parent)
                card.init()
                card.type = suite
                card.value = value
                parent.scene.addItem(card)
                self.__cards.append(card)
        random.shuffle(self.__cards)

    def draw(self) -> CardWidget:
        card = self.__cards[0]
        self.__cards.pop(0)
        return card

    def append(self, card):
        self.__cards.append(card)

