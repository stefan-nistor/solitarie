from __future__ import annotations

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem, QGraphicsSceneMouseEvent

from AbstractDrawable import AbstractDrawable


class CardWidget(AbstractDrawable, QGraphicsPixmapItem):
    def __init__(self, value: int, suit, parent: QGraphicsItem = None):
        super(AbstractDrawable, self).__init__()
        super(QGraphicsItem, self).__init__(parent=parent)

        self.__stack = None
        self.__child = None

        self.__value = value
        self.__suit = suit
        self.__side = None

        self.__face = QPixmap('images/' + '%s_%s' % (self.__suit, self.__value))
        self.__back = QPixmap('images/card_background.svg')

        self.init()

    def align_components(self) -> AbstractDrawable:
        return self

    def customize_components(self) -> AbstractDrawable:
        self.setShapeMode(QGraphicsPixmapItem.ShapeMode.BoundingRectShape)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsScenePositionChanges)
        return self

    def connect_components(self) -> AbstractDrawable:
        return self

    def face_up(self) -> CardWidget:
        self.__side = 1
        self.setPixmap(self.__face)
        return self

    def face_down(self) -> CardWidget:
        self.__side = 0
        self.setPixmap(self.__back)
        return self

    @property
    def is_face_up(self) -> bool:
        return self.__side

    @property
    def get_color(self) -> str:
        if self.__suit in ('H', 'D'):
            return 'r'
        return 'b'

    @property
    def suit(self):
        return self.__suit

    @property
    def value(self):
        return self.__value

    @property
    def stack(self):
        return self.__stack

    @stack.setter
    def stack(self, value):
        self.__stack = value

    def mousePressEvent(self, event) -> None:
        if self.__stack and self != self.__stack.cards[-1]:
            event.ignore()
            return
        print(self.value, self.suit)
        self.face_up()

        self.stack.setZValue(1000)
        event.accept()
        super(CardWidget, self).mouseReleaseEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self.stack.setZValue(-1)
        items = self.collidingItems()
        if items:
            for item in items:
                if isinstance(item, CardWidget) and item.stack != self.stack:
                    cards = self.stack.remove_card(self)
                    item.stack.add_cards(cards)
                    break

        self.stack.refresh()
        super(CardWidget, self).mouseReleaseEvent(event)

