from __future__ import annotations
from typing import Union

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem, QGraphicsSceneMouseEvent

from AbstractDrawable import AbstractDrawable


class CardWidget(QGraphicsPixmapItem, AbstractDrawable):
    class Type:
        Invalid = 0
        Clubs = 1
        Hearts = 2
        Diamonds = 3
        Spades = 4

    class Colour:
        Invalid = 0
        Red = 1
        Black = 2

    @property
    def colour(self):
        return {
            CardWidget.Type.Invalid: CardWidget.Colour.Invalid,
            CardWidget.Type.Clubs: CardWidget.Colour.Black,
            CardWidget.Type.Hearts: CardWidget.Colour.Red,
            CardWidget.Type.Spades: CardWidget.Colour.Black,
            CardWidget.Type.Diamonds: CardWidget.Colour.Red
        }[self.type]

    back = None
    faces = None

    faces_init = False

    class DeckMoveAttributes:
        currently_moved = None
        previous = None

    @staticmethod
    def init_card_faces():
        if CardWidget.faces_init:
            return

        CardWidget.faces_init = True
        CardWidget.back = QPixmap('images/card_background.svg')
        CardWidget.faces = {
            type: {
                value: QPixmap(f"images/{['', 'C', 'H', 'D', 'S'][type]}_{value}.svg") for value in range(1, 14)
            } for type in
            [CardWidget.Type.Clubs, CardWidget.Type.Hearts, CardWidget.Type.Diamonds, CardWidget.Type.Spades]
        }

    def __init__(self, parent=None, board=None):
        super(QGraphicsPixmapItem, self).__init__(parent=parent)
        super(AbstractDrawable, self).__init__()

        CardWidget.init_card_faces()

        self.__type = CardWidget.Type.Invalid
        self.__value = 0
        self.__face_down: bool = True
        self.setPixmap(self.image)
        self.setZValue(1)
        self.__parent = None
        self.__board = board

        self.__leaf: Union[CardWidget, None] = None

    @property
    def image(self) -> QPixmap:
        if self.__face_down:
            return CardWidget.back
        return CardWidget.faces[self.type][self.value]

    @property
    def is_face_down(self) -> bool:
        return self.__face_down

    @property
    def is_face_up(self) -> bool:
        return not self.is_face_down

    def reverse_face(self):
        self.__face_down = not self.__face_down
        self.setPixmap(self.image)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, v):
        self.__value = v

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def leaf(self) -> Union['CardWidget', None]:
        return self.__leaf

    def draw_face(self, x, y, z):
        self.setPos(x, y)
        self.setZValue(z)

    def reveal_leaf(self):
        if self.leaf is None:
            self.reverse_face()
        else:
            self.leaf.reveal_leaf()

    def reset(self):
        if self.__leaf is None:
            return

        self.__leaf.setPos(self.x(), self.y() + 15)
        self.__leaf.setZValue(self.zValue() + 1)
        self.__leaf.reset()

    def reset_for_upper_pile(self):
        if self.__leaf is None:
            return

        self.__leaf.setPos(self.x(), self.y())
        self.__leaf.setZValue(self.zValue() + 1)
        self.__leaf.reset_for_upper_pile()

    def reset_pile(self):
        if self.__leaf is None:
            return

        self.__leaf.setPos(self.x(), self.y())
        self.__leaf.setZValue(self.zValue() + 1)
        self.__leaf.reset_pile()

    def orphan(self):
        self.__parent = None

    def set_leaf(self, card, x=0, y=0, z=0) -> CardWidget:

        if x == 0:
            x = self.x()
            y = self.y() + 15
            z = self.zValue()

        if self.is_face_up:
            y += 10

        if self.__leaf is not None:
            self.__leaf.__parent = self
            return self.__leaf.set_leaf(card, x, y + 15, z + 1)
        else:
            self.__leaf = card
            card.__parent = self
            self.__leaf.draw_face(x, y, z)
            return card

    def set_leaf_pile(self, card, x=0, y=50, z=0) -> CardWidget:
        if x == 0:
            x = self.x()
            y = self.y()
            z = self.zValue()

        if self.__leaf is not None:
            self.__leaf.__parent = self
            return self.__leaf.set_leaf_pile(card, x, y, z + 1)
        else:
            self.__leaf = card
            card.__parent = self
            self.__leaf.draw_face(x, y, z)
            return card

    def align_components(self) -> AbstractDrawable:
        return self

    def customize_components(self) -> AbstractDrawable:
        self.setShapeMode(QGraphicsPixmapItem.ShapeMode.BoundingRectShape)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsScenePositionChanges)
        return self

    def connect_components(self) -> AbstractDrawable:
        return self

    def init(self) -> AbstractDrawable:
        super().init()

        return self

    def is_movable(self) -> bool:

        if self.is_face_down:
            return False
        prev = self
        node = self.leaf
        while node is not None:
            if not prev.can_receive(node):
                return False
            prev = node
            node = node.leaf

        return True

    def can_receive(self, card: CardWidget) -> bool:
        return self.colour != card.colour and self.value == card.value + 1

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        dist = event.pos() - event.lastPos()

        node = self.__leaf
        while node is not None:
            node.moveBy(dist.x(), dist.y())
            node = node.__leaf

        super(QGraphicsPixmapItem, self).mouseMoveEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:

        if not self.is_movable():
            event.ignore()
            return

        node = self
        i = 0
        while node is not None:
            node.setZValue(100 + i)
            i += 1
            node = node.__leaf

        CardWidget.DeckMoveAttributes.currently_moved = self
        CardWidget.DeckMoveAttributes.previous = self.__parent
        if self.__parent is None:
            CardWidget.DeckMoveAttributes.previous = self.__board.container(self)

        super(QGraphicsPixmapItem, self).mousePressEvent(event)

    def get_leaf(self):
        if self.__leaf is None:
            return self
        return self.__leaf.get_leaf()

    def release(self):
        if self.__leaf is not None:
            self.__leaf.__parent = None
        self.__leaf = None

        if self.is_face_down:
            self.reverse_face()

        root = self.__parent
        parent = self.__parent
        while parent is not None:
            root = parent
            parent = parent.__parent

        if root is None:
            root = self

        self.__board.update_deck_leaf(root, self)

    def release_to(self, deck):
        if deck.can_receive(self):
            CardWidget.DeckMoveAttributes.previous.release()
            deck.receive(self)
        else:
            CardWidget.DeckMoveAttributes.previous.reset()

    def release_to_pile(self, deck):
        if deck.can_receive(self):
            CardWidget.DeckMoveAttributes.previous.release()
            deck.receive(self)
        else:
            CardWidget.DeckMoveAttributes.previous.reset_pile()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:

        match = self.__board.nearest_deck(self)
        if match is None:
            if CardWidget.DeckMoveAttributes.previous is not None:
                CardWidget.DeckMoveAttributes.previous.reset()
        else:
            # match.ignore_in_search()
            self.release_to(match)
            # match.consider_in_search()

        CardWidget.DeckMoveAttributes.previous = None
        CardWidget.DeckMoveAttributes.currently_moved = None

        self.__board.stupid_print()
        self.__board.realign_piles()

        super(QGraphicsPixmapItem, self).mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if not self.is_movable():
            event.ignore()
            return

        match = self.__board.pile_containers[self.type - 1]

        if not match.can_receive(self):
            event.ignore()
            return

        CardWidget.DeckMoveAttributes.currently_moved = self
        CardWidget.DeckMoveAttributes.previous = self.__parent
        if self.__parent is None:
            CardWidget.DeckMoveAttributes.previous = self.__board.container(self)

        self.release_to_pile(match)
        CardWidget.DeckMoveAttributes.previous = None
        CardWidget.DeckMoveAttributes.currently_moved = None

        super(QGraphicsPixmapItem, self).mouseDoubleClickEvent(event)

    def stupid_print(self) -> str:
        return ('<h>' if self.is_face_down else '') + {
            1: 'A',
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: '6',
            7: '7',
            8: '8',
            9: '9',
            10: '10',
            11: 'J',
            12: 'Q',
            13: 'K',
        }[self.value] + '-' + {
                   CardWidget.Type.Clubs: 'C',
                   CardWidget.Type.Diamonds: 'D',
                   CardWidget.Type.Spades: 'S',
                   CardWidget.Type.Hearts: 'H'
               }[self.type] + ((' -> ' + self.__leaf.stupid_print()) if self.__leaf is not None else "")
