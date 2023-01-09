from __future__ import annotations
from typing import Union

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem, QGraphicsSceneMouseEvent

from AbstractDrawable import AbstractDrawable


class CardWidget(QGraphicsPixmapItem, AbstractDrawable):
    """
    Class representing a card
    """
    class Type:
        """
        Enum for card types
        """
        Invalid = 0
        Clubs = 1
        Hearts = 2
        Diamonds = 3
        Spades = 4

    class Colour:
        """
        Enum for card colors
        """
        Invalid = 0
        Red = 1
        Black = 2

    @property
    def colour(self):
        """
        Get color based on card type
        :return:
        """
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
        """
        Utility class for deck moving opeations
        """
        currently_moved = None
        previous = None

    @staticmethod
    def init_card_faces():
        """
        Set card images
        :return:
        """
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
        """
        Constructor. Initialize containing items
        :param parent: is passed to the base Qt class
        :param board: reference to the game area
        """
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
        """
        Get image
        :return:
        """
        if self.__face_down:
            return CardWidget.back
        return CardWidget.faces[self.type][self.value]

    @property
    def is_face_down(self) -> bool:
        """
        Check if card is facing down
        """
        return self.__face_down

    @property
    def is_face_up(self) -> bool:
        """
        Check if card is facing up
        """
        return not self.is_face_down

    def reverse_face(self):
        """
        Reverse facing of the card
        """
        self.__face_down = not self.__face_down
        self.setPixmap(self.image)

    @property
    def value(self):
        """
        Get value of the card
        :return:
        """
        return self.__value

    @value.setter
    def value(self, v):
        """
        Set value of the card
        """
        self.__value = v

    @property
    def type(self):
        """
        Get type of card
        :return:
        """
        return self.__type

    @type.setter
    def type(self, value):
        """
        Set value of the card
        :param value:
        """
        self.__type = value

    @property
    def leaf(self) -> Union['CardWidget', None]:
        """
        Get the child card
        :return:
        """
        return self.__leaf

    @leaf.setter
    def leaf(self, value):
        self.__leaf = value

    @property
    def parent(self) -> Union['CardWidget', None]:
        """
        Get parent card
        :return:
        """
        return self.__parent

    @parent.setter
    def parent(self, value):
        """
        Set parent card
        :param value:
        :return:
        """
        self.__parent = value

    def draw_face(self, x, y, z):
        """
        Paint card on board
        :param x: x pos
        :param y: y pos
        :param z: z pos
        :return:
        """
        self.setPos(x, y)
        self.setZValue(z)

    def reveal_leaf(self):
        """
        Turn leaf card face up
        :return:
        """
        if self.leaf is None:
            self.reverse_face()
        else:
            self.leaf.reveal_leaf()

    def reset(self):
        """
        Reset positioning of the cards
        :return:
        """
        if self.__leaf is None:
            return

        self.__leaf.setPos(self.x(), self.y() + 15)
        self.__leaf.setZValue(self.zValue() + 1)
        self.__leaf.reset()

    def reset_for_upper_pile(self):
        """
        Reset positioning of the cards from upper pile
        :return:
        """
        if self.__leaf is None:
            return

        self.__leaf.setPos(self.x(), self.y())
        self.__leaf.setZValue(self.zValue() + 1)
        self.__leaf.reset_for_upper_pile()

    def reset_pile(self):
        """
        Reset positioning of the card from pile
        :return:
        """
        if self.__leaf is None:
            return

        self.__leaf.setPos(self.x(), self.y())
        self.__leaf.setZValue(self.zValue() + 1)
        self.__leaf.reset_pile()

    def orphan(self):
        """
        Remove card's parent
        :return:
        """
        self.__parent = None

    def set_leaf(self, card, x=0, y=0, z=0) -> CardWidget:
        """
        Set a card's child
        :param card: child
        :param x: x pos
        :param y: y pos
        :param z: z pos
        :return: card's child
        """

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
        """
        Set a card's child in upper piles
        :param card: child
        :param x: x pos
        :param y: y pos
        :param z: z pos
        :return: card's child
        """
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
        """
        Align drawable items in layouts/scenes
        :return self:
        """
        return self

    def customize_components(self) -> AbstractDrawable:
        """
        Set custom properties to drawable items
        :return self:
        """
        self.setShapeMode(QGraphicsPixmapItem.ShapeMode.BoundingRectShape)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsScenePositionChanges)
        return self

    def connect_components(self) -> AbstractDrawable:
        """
        Connect QSignals to QSlots
        :return self:
        """
        return self

    def init(self) -> AbstractDrawable:
        """
        Initialize drawable item
        :return self:
        """
        super().init()
        return self

    def is_movable(self) -> bool:
        """
        Check if a card can be moved from its deck
        :return:
        """
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
        """
        Check if a card can be placed on the top of this
        :param card:
        :return:
        """
        return self.colour != card.colour and self.value == card.value + 1

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Handle mouse moving event
        :param event:
        :return:
        """
        dist = event.pos() - event.lastPos()

        node = self.__leaf
        while node is not None:
            node.moveBy(dist.x(), dist.y())
            node = node.__leaf

        super(QGraphicsPixmapItem, self).mouseMoveEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Handle mouse press events
        :param event:
        :return:
        """
        if not self.is_movable():
            event.ignore()
            return

        node = self
        i = 0
        while node is not None:
            node.setZValue(10000 + i)
            i += 1
            node = node.__leaf

        CardWidget.DeckMoveAttributes.currently_moved = self
        CardWidget.DeckMoveAttributes.previous = self.__parent
        if self.__parent is None:
            CardWidget.DeckMoveAttributes.previous = self.__board.container(self)

        super(QGraphicsPixmapItem, self).mousePressEvent(event)

    def get_leaf(self):
        """
        Get the last card child in a recursive manner
        :return:
        """
        if self.__leaf is None:
            return self
        return self.__leaf.get_leaf()

    def release(self):
        """
        Release a card from its deck
        :return:
        """
        if self.__leaf is not None:
            self.__leaf.__parent = None
        self.__leaf = None
        self.__board.do_draw_deck_cleanup(self)

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
        """
        Release a card to a given deck
        :param deck:
        :return:
        """
        if deck.can_receive(self):
            if CardWidget.DeckMoveAttributes.previous is not None:
                CardWidget.DeckMoveAttributes.previous.release()
            deck.receive(self)
        else:
            CardWidget.DeckMoveAttributes.previous.reset()

    def release_to_pile(self, deck):
        """
        Release a card to a given pile
        :param deck:
        :return:
        """
        if deck.can_receive(self):
            CardWidget.DeckMoveAttributes.previous.release()
            deck.receive(self)
        else:
            CardWidget.DeckMoveAttributes.previous.reset_pile()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Handle mouse release events
        :param event:
        :return:
        """
        if event.button() is Qt.MouseButton.LeftButton:
            match = self.__board.nearest_deck(self)
            if match is None:
                if CardWidget.DeckMoveAttributes.previous is not None:
                    CardWidget.DeckMoveAttributes.previous.reset()
            else:
                self.release_to(match)

            CardWidget.DeckMoveAttributes.previous = None
            CardWidget.DeckMoveAttributes.currently_moved = None

            self.__board.stupid_print()
            self.__board.realign_piles()

        elif event.button() is Qt.MouseButton.RightButton:
            print(f'type{self.__type}value{self.__value}')
            self.__board.draw_container.place_first(self)
            CardWidget.DeckMoveAttributes.previous = None
            CardWidget.DeckMoveAttributes.currently_moved = None

        super(QGraphicsPixmapItem, self).mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Handle mouse double click events
        :param event:
        :return:
        """
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
