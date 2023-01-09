from __future__ import annotations

from PyQt6.QtCore import QRectF
from PyQt6.QtCore import pyqtSlot as QSlot
from PyQt6.QtGui import QPixmap, QBrush
from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QMessageBox

from AbstractDrawable import AbstractDrawable
from DeckWidget import DeckWidget
from DrawDeck import DrawDeck
from PileWidget import PileWidget


class GameWidget(QWidget, AbstractDrawable):
    """
    Game window class
    """

    def __init__(self, parent=None):
        """
        Constructor. Initialize containing items
        :param parent: is passed to base Qt class
        """

        super(QWidget, self).__init__(parent=parent)
        super(AbstractDrawable, self).__init__()

        self.__graphics_view = QGraphicsView(self)
        self.__scene = QGraphicsScene(self)
        self.__draw_deck = DrawDeck(self)

        self.__deck_containers = [DeckWidget(parent=self, x=340 + 110 * i, y=200) for i in range(7)]
        self.__pile_containers = [PileWidget(parent=self, x=340 + 110 * (4 + i), y=50) for i in range(4)]

        self.__draw_container = DeckWidget(parent=self, x=50, y=50)

    def container(self, card):
        """
        Returns the container in which the card exists
        :param card:
        """
        for cont in self.deck_containers:
            if cont.root_card is card:
                return cont
        return None

    def realign_piles(self):
        """
        Reset pile card position
        :return:
        """
        for pile in self.__pile_containers:
            pile.reset()

    def nearest_deck(self, card):
        """
        Find the nearest deck in which the card could be placed
        :param card:
        """
        best_match = None
        for deck in self.__deck_containers:

            if deck.x() != deck.leaf.x():
                continue

            if deck.intersects(card) and not deck.ignored:
                if best_match is None:
                    best_match = deck
                else:

                    midpoint_card = card.pos().x() + card.boundingRect().width() / 2
                    midpoint_best_match = best_match.leaf.pos().x() + best_match.leaf.boundingRect().width() / 2
                    midpoint_deck = deck.leaf.pos().x() + deck.leaf.boundingRect().width() / 2

                    if abs(midpoint_deck - midpoint_card) < abs(midpoint_best_match - midpoint_card):
                        best_match = deck

        return best_match

    @property
    def draw_container(self):
        """
        Get draw_container
        """
        return self.__draw_container

    @property
    def scene(self):
        """
        Get scene
        """
        return self.__scene

    @property
    def deck_containers(self) -> list:
        """
        Get deck_containers
        """
        return self.__deck_containers

    @property
    def pile_containers(self) -> list:
        """
        Get pile_containers
        """
        return self.__pile_containers

    def align_components(self) -> AbstractDrawable:
        """
        Align drawable items in layouts/scenes
        :return self:
        """

        self.__scene.setSceneRect(QRectF(0, 0, 1280, 720))
        self.__graphics_view.setScene(self.__scene)

        for container in self.__deck_containers:
            self.__scene.addItem(container)

        for container in self.__pile_containers:
            self.__scene.addItem(container)

        self.__scene.addItem(self.__draw_container)

        return self

    def customize_components(self) -> AbstractDrawable:
        """
        Set custom properties to drawable items
        :return self:
        """
        self.__scene.setBackgroundBrush(QBrush(QPixmap('images/background.png')))

        return self

    def connect_components(self) -> AbstractDrawable:
        """
        Connect QSignals to QSlots
        :return self:
        """
        # PileWidget.check_win.connect(self.is_win)
        return self

    def init(self) -> AbstractDrawable:
        """
        Initialize drawable item
        :return self:
        """
        super().init()

        self.resize(1280, 720)

        for container in self.__deck_containers:
            container.init()

        for container in self.__pile_containers:
            container.init()

        for cards_for_deck, deck_container in enumerate(self.__deck_containers, 1):
            while cards_for_deck > 0:
                cards_for_deck -= 1
                card = self.__draw_deck.draw()
                deck_container.add_card(card)
                self.scene.addItem(card)

        for deck_container in self.__deck_containers:
            deck_container.root_card.reveal_leaf()

        self.__draw_container.init()

        for _ in range(len(self.__draw_deck.cards)):
            card = self.__draw_deck.draw()
            self.__draw_container.add_card(card)
            self.scene.addItem(card)

        self.__draw_container.root_card.reveal_leaf()

        return self

    def stupid_print(self):
        """
        Foolish method for Russian debug
        :return:
        """
        for i, deck in enumerate(self.deck_containers):
            print(f'{i} : {deck.stupid_print()}')

    def update_deck_leaf(self, root_card, new_leaf):
        """
        Update the leaf(last card) of a deck based by root_card
        :param root_card:
        :param new_leaf:
        """
        for deck in self.deck_containers:
            deck.update_leaf(root_card, new_leaf)

    def do_draw_deck_cleanup(self, card):
        """
        Clean draw container node references to avoid unexpected behaviour
        :param card:
        :return:
        """
        node = self.__draw_container.root_card
        last = None
        do_clean = False
        while node is not None:
            if node is card:
                do_clean = True
            last = node
            node = node.leaf

        if do_clean:
            self.__draw_container.leaf = last

    def is_win(self):
        """
        Determine if game is completed
        :return:
        """
        won = True
        for pile in self.__pile_containers:
            if pile.count != 13:
                won = False
        # won = True
        if won is True:
            QMessageBox().information(self, "Game won", "Congratulations. You won")



