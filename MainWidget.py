from PyQt6.QtCore import pyqtSlot as QSlot, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from AbstractDrawable import AbstractDrawable
from GameWidget import GameWidget
from MenuWidget import MenuWidget


class MainWidget(AbstractDrawable, QWidget):
    """
    Main window class
    """

    def __init__(self, parent: QWidget = None):
        """
        Constructor
        :param parent: is passed to base Qt class
        """
        super(AbstractDrawable, self).__init__()
        super(QWidget, self).__init__(parent=parent)

        self.__main_layout = QVBoxLayout()
        self.__menu_layout = QVBoxLayout()

        self.__menu_widget = MenuWidget(self)
        self.__game_widget = None

    def align_components(self) -> AbstractDrawable:
        """
        Align drawable items in layouts/scenes
        :return self:
        """
        self.setLayout(self.__main_layout)

        self.__main_layout.addItem(self.__menu_layout)
        self.__menu_layout.addWidget(self.__menu_widget)
        return self

    def customize_components(self) -> AbstractDrawable:
        """
        Set custom properties to drawable items
        :return self:
        """
        self.__menu_widget.init()
        return self

    def connect_components(self) -> AbstractDrawable:
        """
        Connect QSignals to QSlots
        :return self:
        """
        self.__menu_widget.started.connect(self.started)
        self.__menu_widget.exited.connect(self.close)
        # self.__game_widget.exited.connect(self.close)
        return self

    @QSlot()
    def started(self) -> None:
        """
        QSlot for handling start signal
        :return:
        """
        self.__game_widget = GameWidget(self)
        self.__game_widget.init()
        self.__main_layout.addWidget(self.__game_widget)
