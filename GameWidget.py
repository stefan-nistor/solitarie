from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal as QSignal
from PyQt6.QtCore import pyqtSlot as QSlot
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from AbstractDrawable import AbstractDrawable


class GameWidget(AbstractDrawable, QWidget):
    exited = QSignal()

    def __init__(self, parent: QWidget = None):
        super(AbstractDrawable, self).__init__()
        super(QWidget, self).__init__(parent=parent)

        self.__main_layout = QVBoxLayout()
        self.__deck_layout = QHBoxLayout()
        self.__board_layout = QHBoxLayout()
        self.__control_layout = QHBoxLayout()

        self.__exit_button = QPushButton("Exit", self)

    def align_components(self) -> AbstractDrawable:
        self.setLayout(self.__main_layout)

        self.__main_layout.addItem(self.__deck_layout)
        self.__main_layout.addItem(self.__board_layout)
        self.__main_layout.addItem(self.__control_layout)

        self.__control_layout.addWidget(self.__exit_button)

        return self

    def customize_components(self) -> AbstractDrawable:
        self.__control_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        return self

    def connect_components(self) -> AbstractDrawable:
        return self

    @QSlot()
    def exit_pressed(self) -> None:
        # noinspection PyUnresolvedReferences
        self.exited.emit()
        self.close()
