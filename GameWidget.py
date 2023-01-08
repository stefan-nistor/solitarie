from __future__ import annotations

import random

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtCore import pyqtSignal as QSignal
from PyQt6.QtCore import pyqtSlot as QSlot
from PyQt6.QtGui import QPixmap, QBrush
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsView, QGraphicsScene

from AbstractDrawable import AbstractDrawable
from CardWidget import CardWidget
from DeckWidget import DeckWidget
from PileWidget import PileWidget


class GameWidget(AbstractDrawable, QWidget):
    exited = QSignal()
    suits = ['C', 'D', 'H', 'S']

    def __init__(self, parent: QWidget = None):
        super(AbstractDrawable, self).__init__()
        super(QWidget, self).__init__(parent=parent)

        self.__graphics_view = QGraphicsView(self)
        self.__scene = QGraphicsScene(self)

        self.__deal = DeckWidget()
        self.__cards = []
        self.__piles = []
        self.__decks = []

        for i in range(4):
            pile = PileWidget()
            self.__piles.append(pile)

        for i in range(7):
            deck = DeckWidget()
            self.__decks.append(deck)

        for suit in self.suits:
            for value in range(1, 14):
                card = CardWidget(value, suit)
                self.__cards.append(card)

    def align_components(self) -> AbstractDrawable:
        self.__scene.setSceneRect(QRectF(0, 0, 1280, 720))
        self.__graphics_view.setScene(self.__scene)
        self.__scene.addItem(self.__deal)

        for pile in self.__piles:
            self.__scene.addItem(pile)

        for deck in self.__decks:
            self.__scene.addItem(deck)

        for card in self.__cards:
            self.__scene.addItem(card)

        return self

    def customize_components(self) -> AbstractDrawable:
        self.__scene.setBackgroundBrush(QBrush(QPixmap('images/background.png')))
        self.__deal.setPos(50, 50)

        for i, pile in enumerate(self.__piles):
            pile.setPos(340 + 110 * (4 + i), 50)

        for i, deck in enumerate(self.__decks):
            deck.setPos(340 + 110 * i, 200)

        return self

    def connect_components(self) -> AbstractDrawable:
        return self

    @QSlot()
    def exit_pressed(self) -> None:
        # noinspection PyUnresolvedReferences
        self.exited.emit()
        self.close()

    def spread_cards(self):
        cards = self.__cards
        for n, deck in enumerate(self.__decks, 1):
            for a in range(n):
                card = cards.pop()
                deck.add_card(card)
                card.face_down()
                if a == n-1:
                    card.face_up()
