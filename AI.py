from Actor import Actor
import pygame
import random
import math
from Apple import Apple
from transitions import Machine, State
from transitions.extensions import MachineFactory, GraphMachine
from Player import Player

diagram_cls = MachineFactory.get_predefined(graph=True)

class AI(Actor):
    img:pygame.image.load
    defaultImg:pygame.image.load

    pos:pygame.math.Vector2
    midPos:pygame.math.Vector2
    size:pygame.math.Vector2
    angle:float

    vectRight:pygame.math.Vector2
    forward:pygame.math.Vector2
    currVelo:pygame.math.Vector2
    initialVelo:pygame.math.Vector2

    destination:pygame.math.Vector2

    aiState:str

    maxSpeed:float
    minSpeed:float

    isMoving:bool

    initialPos:pygame.math.Vector2
    lenghtDest:float

    accelerateAndDecelerateTime:float
    currTime:float
    distDecelerate:float
    distMoveWander:float
    wanderSet:bool
    distFlee:float

    apple:Apple
    player:Player

    machine:Machine
    states = []

    def __init__(self, tag:str, imagePath:str):
        super().__init__("tag")

        self.aiState = "Wander"

        self.size = pygame.math.Vector2(100, 100)
        self.pos = pygame.math.Vector2(100, 100)
        self.midPos = pygame.math.Vector2(self.pos + (self.size / 2))

        self.angle = 0
        self.vectRight = pygame.math.Vector2(1, 0)
        self.forward = pygame.math.Vector2(1, 0)
        self.currVelo = pygame.math.Vector2()
        self.initialVelo = pygame.math.Vector2()

        self.defaultImg = pygame.image.load(imagePath)
        self.defaultImg = pygame.transform.scale(self.defaultImg, self.size)
        self.img = self.defaultImg

        self.destination = pygame.math.Vector2(self.midPos)
        self.isMoving = False

        self.maxSpeed = 4
        self.minSpeed = 2

        self.lenghtDest = 0
        self.initialPos = pygame.math.Vector2(self.midPos)

        self.accelerateAndDecelerateTime = 0.5
        self.currTime = 0
        self.distDecelerate = 200
        self.distMoveWander = 300
        self.wanderSet = False
        self.distFlee = 300

        self.states.append(State("Seek", self.OnSeek, self.OnExit))
        self.states.append(State("Flee", self.OnFlee, self.OnExit))
        self.states.append(State("Wander", self.OnWander, self.OnExit))
        
        self.machine = diagram_cls(model=self, states=self.states, initial="Wander", show_auto_transitions=True, show_conditions=True, show_state_attributes=True)

        self.machine.add_transition("Seek", "Flee", "Seek")
        self.machine.add_transition("Seek", "Wander", "Seek")
        self.machine.add_transition("Seek", "Seek", "Seek")

        self.machine.add_transition("Flee", "Seek", "Flee", conditions=["PlayerArm"])
        self.machine.add_transition("Flee", "Wander", "Flee", conditions=["PlayerArm"])
        self.machine.add_transition("Flee", "Flee", "Flee", conditions=["PlayerArm"])

        self.machine.add_transition("Wander", "Seek", "Wander")
        self.machine.add_transition("Wander", "Flee", "Wander")
        self.machine.add_transition("Wander", "Wander", "Wander")

    def SetApple(self, apple:Apple):
        self.apple = apple

    def SetPlayer(self, player:Player):
        self.player = player

    def SetPos(self, pos:float):
        self.pos = pos

    def UpdateDest(self, dest:float):
        self.destination.x = dest[0]
        self.destination.y = dest[1]

    def SetDestination(self):
        #ici je set la longeur du trajet et la position initial
        vectDist = self.destination - self.midPos
        self.lenghtDest = vectDist.length()
        self.initialPos = self.midPos
        self.distDecelerate = (vectDist.length() / 100) * 50
        self.accelerateAndDecelerateTime = vectDist.length() / 1000

        self.SetRotation()

    def SetRotation(self):
        #pour eviter un bug car on ne peux pas normalizer un vecteur d'une longueur de 0
        if (self.destination - self.midPos).length() > 0:
            self.forward = self.destination - self.midPos
            self.forward = self.forward.normalize()

        #ici j'inverse l'angle car ca me donne l'angle dans l'autre sens
        self.angle = -self.vectRight.angle_to(self.forward)


    def SetState(self, state:str):
        self.aiState = state
        print("current state = " + self.aiState)

    def ResetCurrVelo(self):
        self.initialVelo = self.forward * self.minSpeed
        self.currVelo = self.initialVelo
        self.currTime = 0

    def Seek(self, dt:float):
        distArrive:float = (self.midPos - self.destination).magnitude()
        if distArrive <= self.distDecelerate:
            self.currTime -= dt
            if self.currTime < 0:
                self.currTime = 0
            self.currVelo = self.initialVelo.lerp(self.initialVelo * self.maxSpeed, self.currTime / self.accelerateAndDecelerateTime)
        elif self.currVelo.magnitude() < (self.initialVelo * self.maxSpeed).magnitude():
            self.currTime += dt
            if self.currTime > self.accelerateAndDecelerateTime:
                self.currTime = self.accelerateAndDecelerateTime
            self.currVelo = self.initialVelo.lerp(self.initialVelo * self.maxSpeed, self.currTime / self.accelerateAndDecelerateTime)

        self.Move(self.currVelo)

    def Flee(self, dt:float):
        self.Seek(dt)

    def Wander(self, dt:float):
        if not self.isMoving or self.wanderSet:
            #je fais foi 50 car 1 degree na pas un gros impact
            angle = self.angle + ((random.random() - random.random()) * 50)

            #ici j'inverse l'angle car l'angle ce fais inverser lorsque je prends l'angle selon la
            #destination dans la fonction SetRotation(self):
            angle = -angle

            radAngle = math.radians(angle)
            x = math.cos(radAngle)
            y = math.sin(radAngle)

            vectAngle = pygame.math.Vector2(x, y)

            destination = self.midPos + (vectAngle * self.distMoveWander)

            self.UpdateDest(destination)
            self.SetDestination()
            self.ResetCurrVelo()

            self.wanderSet = False

        self.Seek(dt)

    def Move(self, velo:pygame.math.Vector2):
        vectAI = self.midPos - self.initialPos
        lengthAI = vectAI.length()

        if lengthAI >= self.lenghtDest:
            self.isMoving = False
            if self.aiState == "Seek":
                self.apple.Eat()
            if self.aiState != "Wander":
                if self.apple.GetState():
                    self.destination = self.apple.pos + (self.apple.size / 2)
                    self.SetTransition("Seek")
                else:
                    self.SetTransition("Wander")
        else:
            self.isMoving = True

        if self.isMoving:
            self.pos += velo
            self.midPos = self.pos + (self.size / 2)

    def AppleIsEat(self):
        return self.apple.GetState()

    def PlayerArm(self):
        return self.player.arm

    def SetTransition(self, transition:str):
        self.trigger(transition)

    def OnSeek(self):
        self.apple.RenderAt(self.destination)
        self.SetDestination()
        self.aiState = "Seek"
        self.ResetCurrVelo()

    def OnFlee(self):
        temp = self.midPos - self.destination
        self.destination = self.midPos + temp
        self.SetDestination()
        self.aiState = "Flee"
        self.ResetCurrVelo()

    def OnWander(self):
        self.wanderSet = True
        self.UpdateDest(self.destination + (self.forward * 100))
        self.SetDestination()
        self.aiState = "Wander"
        self.ResetCurrVelo()


    def OnExit(self):
        pass
        

    def Render(self, screen):
        if self.img != None:
            img = pygame.transform.rotate(self.defaultImg, self.angle)

            screen.blit(img, self.pos)

            pygame.draw.line(screen, pygame.Color(255, 255, 255), self.midPos, self.destination, 5)

    def Update(self, dt:float):
        if self.midPos.distance_to(self.player.midPos) <= self.distFlee:
            if self.aiState != "Flee" and self.PlayerArm():
                self.UpdateDest(self.player.midPos)
                self.SetTransition("Flee")
        
        match(self.aiState):
            case "Seek":
                self.Seek(dt)
            case "Flee":
                self.Flee(dt)
            case "Wander":
                self.Wander(dt)
