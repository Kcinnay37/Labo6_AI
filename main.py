import sys
from PySide2.QtWidgets import QApplication
from Game import Game
from Window import Window

def main():
    app = QApplication(sys.argv)

    game = Game()
    win = Window(game)

    app.setActiveWindow(win)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()