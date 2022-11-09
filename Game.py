import pygame
from Engine import Engine
from AI import AI
from Timer import Timer
from Player import Player
from Apple import Apple

class Game:
    isRun:bool

    width:int = 1000
    height:int = 800
    size:float = []

    screen:pygame.display.set_mode

    BGColor:int = [2, 0, 102]

    engine:Engine

    timer:Timer

    AI:AI

    player:Player

    apple:Apple

    def __init__(self):
        self.isRun = True
        self.engine = Engine()
        self.timer = Timer()
        pygame.init()
        self.GameInit()

    def GameInit(self):
        self.size = [self.width, self.height]
        self.screen = pygame.display.set_mode(self.size)

        self.apple = Apple("Apple", "Image\\Apple.png")
        self.engine.AddActor(self.apple)

        self.player = Player("Player", "Image\\hitman1_stand.png", "Image\\hitman1_gun.png")
        self.engine.AddActor(self.player)

        self.AI = AI("AI", "Image\\Zombi.png")
        self.AI.SetApple(self.apple)
        self.AI.SetPlayer(self.player)
        self.engine.AddActor(self.AI)

        self.engine.Start()

    def GameLoop(self):
        self.timer.Update()
        
        self.ProcessInput()

        self.engine.Update(self.timer.GetDeltaTime())

        self.Render()

        return self.isRun

    def ProcessInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRun = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    self.AI.UpdateDest(pygame.mouse.get_pos())
                    self.AI.SetTransition("Seek")

            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    self.player.ChangeState()



    def Render(self):
        self.screen.fill(self.BGColor)

        self.engine.Render(self.screen)

        pygame.display.flip()

    def ChangeMode(self, mode:str):
        self.AI.SetState(mode)
