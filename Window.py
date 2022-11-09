from Game import Game
from PySide2.QtWidgets import QWidget, QPushButton, QSlider, QComboBox,QHBoxLayout
from PySide2.QtCore import QTimer

class Window(QWidget):
    game:Game
    timer:QTimer

    FPS:int

    def __init__(self, game:Game, FPS:int=60):
        super().__init__()
        self.FPS = 1000 / FPS
        self.game = game
        self.InitUI()
        self.InitPygame(game)

    def InitUI(self):
        self.setWindowTitle("Labo5")
        self.setGeometry(10, 10, 300, 200)

        self.layout = QHBoxLayout()

        self.combotBox = QComboBox()
        self.combotBox.addItem("Seek")
        self.combotBox.addItem("Flee")
        self.combotBox.addItem("Wander")
        self.combotBox.currentIndexChanged.connect(self.ChangeMode)

        self.layout.addWidget(self.combotBox)
        self.setLayout(self.layout)

        self.show()

    def InitPygame(self, game:Game):
        self.game = game

        self.timer = QTimer()
        self.timer.timeout.connect(self.IsRun)
        self.timer.start(self.FPS)

    def IsRun(self):
        if not self.game.GameLoop():
            self.close()

    def ChangeMode(self):
        pass
        #combotBox = self.sender()
        #self.game.ChangeMode(combotBox.itemText(combotBox.currentIndex()))
