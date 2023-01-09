from PyQt6.QtWidgets import QGraphicsRectItem

from AbstractDrawable import AbstractDrawable
from CardWidget import CardWidget
import random


class DrawDeck(QGraphicsRectItem):
    """
    Class for draw cards
    """
    def __init__(self, parent=None):
        """
        Constructor. Create cards and shuffle the deck
        :param parent:
        """
        super(QGraphicsRectItem, self).__init__()

        self.__cards = []
        for suite in [CardWidget.Type.Clubs, CardWidget.Type.Diamonds, CardWidget.Type.Hearts, CardWidget.Type.Spades]:
            for value in range(1, 14):
                card = CardWidget(parent=self, board=parent)
                card.init()
                card.type = suite
                card.value = value
                # parent.scene.addItem(card)
                self.__cards.append(card)
        random.shuffle(self.__cards)

    def draw(self) -> CardWidget:
        """
        Draw a card from the list of cards
        :return: card
        """
        card = self.__cards[0]
        self.__cards.pop(0)
        return card

    def append(self, card):
        """
        Append a card to the list of cards
        :param card:
        """
        self.__cards.append(card)

    @property
    def cards(self):
        """
        Get cards
        """
        return self.__cards

