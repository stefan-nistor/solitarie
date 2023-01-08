from __future__ import annotations

from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsItem

from AbstractDrawable import AbstractDrawable
from PyQt6.QtCore import pyqtSignal as QSignal

from CardWidget import CardWidget


class PileWidget(AbstractDrawable, QGraphicsRectItem):
    completed = QSignal()

    def __init__(self, parent: QGraphicsRectItem = None):
        super(AbstractDrawable, self).__init__()
        super(QGraphicsItem, self).__init__(parent=parent)

        self.setRect(QRectF(0, 0, 75, 110))
        self.cards = []
        self.__suit = None
        self.__last_value = 0

    def is_valid(self, card: CardWidget) -> bool:
        if self.__suit is None:
            return True

        if card.suit == self.__suit and card.value == self.__last_value + 1:
            return True

        return False

    def add_card(self, card) -> None:
        self.__suit = card.suit
        self.__last_value = self.__last_value + 1
        if self.__last_value == 13:
            # noinspection PyUnresolvedReferences
            self.completed.emit()

    @property
    def is_completed(self):
        return self.__last_value == 13

    def align_components(self) -> AbstractDrawable:
        pass

    def customize_components(self) -> AbstractDrawable:
        pass

    def connect_components(self) -> AbstractDrawable:
        pass

