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

    def align_components(self) -> AbstractDrawable:
        return self

    def customize_components(self) -> AbstractDrawable:
        self.setShapeMode(QGraphicsPixmapItem.ShapeMode.BoundingRectShape)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
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

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.face_up()
        event.accept()
        return

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        return
