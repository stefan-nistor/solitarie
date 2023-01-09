from typing import Union

from PyQt6.QtCore import QRectF, QPointF
from PyQt6.QtWidgets import QGraphicsRectItem

from AbstractDrawable import AbstractDrawable
from CardWidget import CardWidget


class DeckWidget(QGraphicsRectItem, AbstractDrawable):
    """
    Class for working decks on board
    """

    def __init__(self, parent=None, x=0, y=0):
        """
        Constructor. Initialize containing items
        :param parent: is passed to base Qt class
        :param x: position in board
        :param y: position in board
        """
        super(QGraphicsRectItem, self).__init__()
        super(AbstractDrawable, self).__init__()

        self.__parent = parent
        self.__x = x
        self.__y = y

        self.__root_card: Union[CardWidget, None] = None
        self.__leaf: Union[CardWidget, None] = None
        self.__ignored = False

    @property
    def ignored(self) -> bool:
        """
        Get ignored
        """
        return self.__ignored

    @property
    def root_card(self):
        """
        Get root_card
        """
        return self.__root_card

    @property
    def leaf(self):
        """
        Get leaf
        """
        if self.__leaf is None:
            return self
        return self.__leaf

    @leaf.setter
    def leaf(self, value):
        self.__leaf = value
        if self.__root_card is None:
            self.__root_card = value

    def can_receive(self, card: CardWidget) -> bool:
        """
        Validate if a card can be added to the deck in a recursive manner
        :param card:
        """
        if self.__root_card is None:
            return True

        return self.__leaf.can_receive(card)

    def reset(self):
        """
        Reset positions of the cards
        :return:
        """
        if self.__root_card is not None:
            self.__root_card.draw_face(self.__x, self.__y, 1)
            self.__root_card.reset()

    def release(self):
        """
        Release a card from the deck
        :return:
        """
        self.__root_card = None
        self.__leaf = None

    def receive(self, card):
        """
        Recevie a card to the deck and reset
        :param card:
        :return:
        """
        self.add_card(card)
        self.__root_card.reset()

    def add_card(self, card):
        """
        Add a card to the linked list of cards
        :param card:
        :return:
        """
        if self.__root_card is None:
            card.orphan()
            self.__root_card = card
            self.__root_card.draw_face(self.__x, self.__y, 1)
            self.__leaf = card.get_leaf()
        else:
            self.__leaf = self.__root_card.set_leaf(card, x=self.__x, y=self.__y + 15, z=2).get_leaf()

    def place_first(self, card: CardWidget):
        """
        Place a card at the beginning of the deck
        :param card:
        :return:
        """
        leaf = self.__leaf
        self.__leaf = leaf.parent
        self.__leaf.leaf = None
        leaf.leaf = self.__root_card
        self.__root_card.parent = leaf
        leaf.parent = None
        self.__root_card = leaf
        self.__root_card.reset()
        self.__root_card.reverse_face()
        self.__leaf.reverse_face()

        print(f'left: {self.__root_card.stupid_print()}')

        y = 50
        node = self.__root_card
        while node != None:
            node.setPos(50, y)
            y += 15
            node = node.leaf

    def intersects(self, card) -> bool:
        """
        Checks if a card intersects an area of a deck
        :param card:
        :return:
        """
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
        """
        Get leaf
        :return:
        """
        return self.__leaf

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

        self.setRect(0, 0, 75, 110)
        self.setPos(self.__x, self.__y)

        return self

    def stupid_print(self) -> str:
        """
        Foolish method for Russian Debug
        :return:
        """
        if self.__root_card is None:
            return f'root -> empty, leaf -> {"empty" if self.__leaf is None else "invalid"}'
        return 'root -> ' + self.__root_card.stupid_print() + ", leaf ->" + self.__leaf.stupid_print()

    def update_leaf(self, root_card, new_leaf):
        """
        Update the leaf(last card) of a deck based by root_card
        :param root_card:
        :param new_leaf:

        """
        if self.__root_card is root_card:
            self.__leaf = new_leaf.get_leaf()

        if self.__root_card is not None:
            self.__root_card.reset()

