from __future__ import annotations

from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsItem

from AbstractDrawable import AbstractDrawable
from CardWidget import CardWidget


class DeckWidget(AbstractDrawable, QGraphicsRectItem):

    def __init__(self, parent: QGraphicsItem = None):
        super(AbstractDrawable, self).__init__()
        super(QGraphicsItem, self).__init__(parent=parent)

        self.setRect(QRectF(0, 0, 80, 116))
        self.__cards = []

    def add_card(self, card: CardWidget) -> None:
        self.__cards.append(card)

    def remove_card(self, card: CardWidget) -> None:
        card.__stack = None
        self.__cards.remove(card)

    def remove_all_cards(self):
        for card in self.__cards[:]:
            card.__stack = None
        self.__cards = []

    def align_components(self) -> AbstractDrawable:
        return self

    def customize_components(self) -> AbstractDrawable:
        return self

    def connect_components(self) -> AbstractDrawable:
        return self
