from Actor import Actor
import pygame
from transitions import Machine, State
from transitions.extensions import MachineFactory, GraphMachine

diagram_cls = MachineFactory.get_predefined(graph=True)

class Player(Actor, object):
    defaultImgNoArm:pygame.image.load
    defaultImgArm:pygame.image.load
    currImg:pygame.image.load

    pos:pygame.math.Vector2
    midPos:pygame.math.Vector2
    size:pygame.math.Vector2
    angle:float

    vectRight:pygame.math.Vector2
    forward:pygame.math.Vector2
    currVelo:pygame.math.Vector2

    moveSpeed:float
    rotateSpeed:float

    playerState:str

    machine:Machine
    states = []

    arm:bool

    def __init__(self, tag:str, imagePath1:str, imagePath2:str):
        super().__init__("tag")

        self.pos = pygame.math.Vector2(500, 400)
        self.size = pygame.math.Vector2(100, 100)
        self.midPos = self.pos + (self.size / 2)
        self.angle = 0

        self.defaultImgNoArm = pygame.image.load(imagePath1)
        self.defaultImgNoArm = pygame.transform.scale(self.defaultImgNoArm, self.size)

        self.defaultImgArm = pygame.image.load(imagePath2)
        self.defaultImgArm = pygame.transform.scale(self.defaultImgArm, self.size)

        self.currImg = self.defaultImgNoArm

        self.moveSpeed = 200
        self.rotateSpeed = 150

        self.vectRight = pygame.math.Vector2(1, 0)
        self.forward = pygame.math.Vector2(1, 0)

        self.arm = False

        self.states.append(State("NoArm", self.ChangeBoolState))
        self.states.append(State("Arm", self.ChangeBoolState))
        
        self.machine = diagram_cls(model=self, states=self.states, initial="NoArm", show_auto_transitions=True, show_conditions=True, show_state_attributes=True)

        self.machine.add_transition("transition", "NoArm", "Arm")
        self.machine.add_transition("transition", "Arm", "NoArm")

    def SetPos(self, pos:float):
        self.pos = pos

    def ChangeBoolState(self):
        self.arm = not self.arm
        if self.arm:
            self.currImg = self.defaultImgArm
        else:
            self.currImg = self.defaultImgNoArm

    def SetState(self, state:str):
        self.playerState = state
        print("current state = " + self.playerState)

    def ChangeState(self):
        self.trigger("transition")

    def Rotate(self, dir:int, dt:float):
        self.angle += dir * self.rotateSpeed * dt

        self.forward = self.vectRight.rotate(-self.angle)

    def Move(self, dir:int, dt:float):
        self.pos += dir * self.forward * self.moveSpeed * dt
        self.midPos = self.pos + (self.size / 2)

    def Render(self, screen):
        img = pygame.transform.rotate(self.currImg, self.angle)

        screen.blit(img, self.pos - pygame.math.Vector2(int(img.get_width() / 2), int(img.get_height() / 2)))

    def Update(self, dt:float):
        if pygame.key.get_pressed()[pygame.K_a]:
            self.Rotate(1, dt)
        if pygame.key.get_pressed()[pygame.K_d]:
            self.Rotate(-1, dt)
        if pygame.key.get_pressed()[pygame.K_w]:
            self.Move(1, dt)
        if pygame.key.get_pressed()[pygame.K_s]:
            self.Move(-1, dt)     
