from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal as QSignal
from PyQt6.QtCore import pyqtSlot as QSlot
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

from AbstractDrawable import AbstractDrawable


class MenuWidget(AbstractDrawable, QWidget):
    started = QSignal()
    exited = QSignal()

    def __init__(self, parent: QWidget = None):
        super(AbstractDrawable, self).__init__()
        super(QWidget, self).__init__(parent=parent)

        self.__main_layout = QVBoxLayout()
        self.__button_layout = QVBoxLayout()
        self.__start_button = QPushButton("Start Game", self)
        self.__exit_button = QPushButton("Exit", self)

    def align_components(self) -> AbstractDrawable:
        self.setLayout(self.__main_layout)

        self.__button_layout.addWidget(self.__start_button)
        self.__button_layout.addWidget(self.__exit_button)

        self.__main_layout.addItem(self.__button_layout)

        return self

    def customize_components(self) -> AbstractDrawable:
        self.__button_layout.setSpacing(10)
        self.__button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return self

    def connect_components(self) -> AbstractDrawable:
        self.__start_button.clicked.connect(self.start_pressed)
        self.__exit_button.clicked.connect(self.exit_pressed)
        return self

    @QSlot()
    def start_pressed(self) -> None:
        # noinspection PyUnresolvedReferences
        self.started.emit()
        self.close()

    @QSlot()
    def exit_pressed(self) -> None:
        # noinspection PyUnresolvedReferences
        self.exited.emit()
        self.close()
