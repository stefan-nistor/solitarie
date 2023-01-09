from typing import Union

from PyQt6.QtCore import QRectF, QPointF
from PyQt6.QtWidgets import QGraphicsRectItem

from AbstractDrawable import AbstractDrawable
from CardWidget import CardWidget


class DeckWidget(QGraphicsRectItem, AbstractDrawable):

    def __init__(self, parent=None, x=0, y=0):
        super(QGraphicsRectItem, self).__init__()
        super(AbstractDrawable, self).__init__()

        self.__parent = parent
        self.__x = x
        self.__y = y

        self.__root_card: Union[CardWidget, None] = None
        self.__leaf = None
        self.__ignored = False

    @property
    def ignored(self) -> bool:
        return self.__ignored

    @property
    def root_card(self):
        return self.__root_card

    @property
    def leaf(self):
        if self.__leaf is None:
            return self
        return self.__leaf

    def can_receive(self, card: CardWidget) -> bool:
        if self.__root_card is None:
            return True

        return self.__leaf.can_receive(card)

    def reset(self):
        if self.__root_card is not None:
            self.__root_card.draw_face(self.__x, self.__y, 1)
            self.__root_card.reset()

    def release(self):
        self.__root_card = None
        self.__leaf = None

    def receive(self, card):
        self.add_card(card)
        self.__root_card.reset()

    def add_card(self, card):
        if self.__root_card is None:
            card.orphan()
            self.__root_card = card
            self.__root_card.draw_face(self.__x, self.__y, 1)
            self.__leaf = card.get_leaf()
        else:
            self.__leaf = self.__root_card.set_leaf(card, x=self.__x, y=self.__y + 15, z=2).get_leaf()

    def intersects(self, card) -> bool:
        leaf = None
        if self.__leaf is not None:
            leaf = self.__leaf
        else:
            leaf = self

        leaf_pos: QPointF = leaf.pos()
        leaf_rect: QRectF = leaf.boundingRect()
        adapted_leaf_rect = QRectF(
            leaf_pos.x(),
            leaf_pos.y(),
            leaf_rect.width(),
            leaf_rect.height()
        )

        card_pos: QPointF = card.pos()
        card_rect: QRectF = card.boundingRect()
        adapted_card_widget_rect = QRectF(
            card_pos.x(),
            card_pos.y(),
            card_rect.width(),
            card_rect.height()
        )

        return self.__leaf != card and adapted_leaf_rect.intersects(adapted_card_widget_rect)

    @property
    def self(self):
        return self.__leaf

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

    def stupid_print(self) -> str:
        if self.__root_card is None:
            return f'root -> empty, leaf -> {"empty" if self.__leaf is None else "invalid"}'
        return 'root -> ' + self.__root_card.stupid_print() + ", leaf ->" + self.__leaf.stupid_print()

    def update_leaf(self, root_card, new_leaf):
        if self.__root_card is root_card:
            self.__leaf = new_leaf.get_leaf()

        if self.__root_card is not None:
            self.__root_card.reset()


class UpperDeckWidget(DeckWidget):

    def __init__(self, parent = None, x = 0, y = 0):
        super().__init__(parent)
