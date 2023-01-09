from __future__ import annotations

from PyQt6.QtCore import QRectF
from PyQt6.QtCore import pyqtSignal as QSignal
from PyQt6.QtCore import pyqtSlot as QSlot
from PyQt6.QtGui import QPixmap, QBrush
from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene

from AbstractDrawable import AbstractDrawable
from DeckWidget import DeckWidget
from DrawDeck import DrawDeck
from PileWidget import PileWidget


class GameWidget(QWidget, AbstractDrawable):

    def __init__(self, parent=None):

        super(QWidget, self).__init__(parent=parent)
        super(AbstractDrawable, self).__init__()

        self.__graphics_view = QGraphicsView(self)
        self.__scene = QGraphicsScene(self)
        self.__draw_deck = DrawDeck(self)

        self.__deck_containers = [DeckWidget(parent=self, x=340 + 110 * i, y=200) for i in range(7)]
        self.__pile_containers = [PileWidget(parent=self, x=340 + 110 * (4 + i), y=50) for i in range(4)]

    def container(self, card):
        for cont in self.deck_containers:
            if cont.root_card is card:
                return cont
        return None

    def realign_piles(self):
        for pile in self.__pile_containers:
            pile.reset()

    def nearest_deck(self, card):
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
    def scene(self):
        return self.__scene

    @property
    def deck_containers(self) -> list:
        return self.__deck_containers

    @property
    def pile_containers(self) -> list:
        return self.__pile_containers

    def align_components(self) -> AbstractDrawable:

        self.__scene.setSceneRect(QRectF(0, 0, 1280, 720))
        self.__graphics_view.setScene(self.__scene)
        for container in self.__deck_containers:
            self.__scene.addItem(container)

        for container in self.__pile_containers:
            self.__scene.addItem(container)

        return self

    def customize_components(self) -> AbstractDrawable:
        self.__scene.setBackgroundBrush(QBrush(QPixmap('images/background.png')))

        return self

    def connect_components(self) -> AbstractDrawable:
        return self

    def init(self) -> AbstractDrawable:
        super().init()

        self.resize(1280, 720)

        for container in self.__deck_containers:
            container.init()

        for container in self.__pile_containers:
            container.init()

        for cards_for_deck, deck_container in enumerate(self.__deck_containers, 1):
            while cards_for_deck > 0:
                cards_for_deck -= 1
                deck_container.add_card(self.__draw_deck.draw())

        for deck_container in self.__deck_containers:
            deck_container.root_card.reveal_leaf()

        return self

    def stupid_print(self):
        for i, deck in enumerate(self.deck_containers):
            print(f'{i} : {deck.stupid_print()}')

    def update_deck_leaf(self, root_card, new_leaf):
        for deck in self.deck_containers:
            deck.update_leaf(root_card, new_leaf)
