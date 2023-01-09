from __future__ import annotations

from typing import Union

from PyQt6.QtWidgets import QGraphicsRectItem

from AbstractDrawable import AbstractDrawable
from CardWidget import CardWidget


class PileWidget (QGraphicsRectItem, AbstractDrawable):
    def __init__(self, parent=None, x=0, y=0):
        super(QGraphicsRectItem, self).__init__()
        super(AbstractDrawable, self).__init__()

        self.__parent = parent
        self.__x = x
        self.__y = y

        self.__root_card: Union[CardWidget, None] = None
        self.__leaf: Union[CardWidget, None] = None

    def reset(self):
        if self.__root_card is not None:
            self.__root_card.reset_for_upper_pile()

    def align_components(self) -> AbstractDrawable:
        return self

    def customize_components(self) -> AbstractDrawable:
        return self

    def connect_components(self) -> AbstractDrawable:
        return self

    def init(self) -> AbstractDrawable:
        super().init()

        self.setRect(0, 0, 75, 110)
        self.setPos(self.__x, self.__y)

        return self

    def can_receive(self, card: CardWidget) -> bool:
        if self.__root_card is None and card.value == 1:
            return True
        if self.__leaf is not None:
            return self.__leaf.type == card.type and self.__leaf.value == card.value - 1
        return False

    def receive(self, card):
        self.add_card(card)
        self.__root_card.reset_pile()

    def add_card(self, card):
        if self.__root_card is None:
            card.orphan()
            self.__root_card = card
            self.__root_card.draw_face(self.__x, 50, 1)
            self.__leaf = card.get_leaf()
        else:
            self.__leaf = self.__root_card.set_leaf_pile(card, x=self.__x, y=self.__y, z=2).get_leaf()

