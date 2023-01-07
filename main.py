from PyQt6.QtWidgets import QApplication

from MainWidget import MainWidget

if __name__ == '__main__':
    app = QApplication([])
    game = MainWidget()
    game.init()
    game.resize(1280, 720)
    game.show()
    app.exec()

