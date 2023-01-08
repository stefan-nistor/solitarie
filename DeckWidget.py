from __future__ import annotations

from PyQt6.QtCore import QRectF, QPointF
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsItem

from AbstractDrawable import AbstractDrawable
from CardWidget import CardWidget


class DeckWidget(AbstractDrawable, QGraphicsRectItem):

    def __init__(self, parent: QGraphicsItem = None):
        super(AbstractDrawable, self).__init__()
        super(QGraphicsItem, self).__init__(parent=parent)

        self.setRect(QRectF(0, 0, 75, 110))
        self.__cards = []

    def add_card(self, card: CardWidget) -> None:
        if self.__cards:
            card.setParentItem(self.__cards[-1])
        else:
            card.setParentItem(self)

        self.__cards.append(card)
        offset = 0
        for n, card in enumerate(self.cards):
            card.setPos(0, offset)
            if card.is_face_up:
                offset = 20
            else:
                offset = 10

    def remove_card(self, card: CardWidget) -> None:
        card.__stack = None
        self.__cards.remove(card)

    def remove_all_cards(self):
        for card in self.__cards[:]:
            card.__stack = None
        self.__cards = []

    @property
    def cards(self):
        return self.__cards

    def top_card(self) -> CardWidget:
        card = self.__cards[-1]
        self.remove_card(card)
        return card

    def align_components(self) -> AbstractDrawable:
        return self

    def customize_components(self) -> AbstractDrawable:
        return self

    def connect_components(self) -> AbstractDrawable:
        return self
