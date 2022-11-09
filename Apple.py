from Actor import Actor
import pygame

class Apple(Actor):
    render:bool

    img:pygame.image.load

    pos:pygame.math.Vector2
    size:pygame.math.Vector2

    def __init__(self, tag:str, imgPath:str):
        super().__init__(tag)

        self.pos = pygame.math.Vector2(500, 400)
        self.size = pygame.math.Vector2(100, 100)

        self.img = pygame.image.load(imgPath)
        self.img = pygame.transform.scale(self.img, self.size)

        self.render = False
        self.pos = pygame.math.Vector2(0, 0)
        

    def RenderAt(self, pos):
        self.pos.x = pos[0] - (self.size.x / 2)
        self.pos.y = pos[1] - (self.size.y / 2)
        self.render = True

    def Eat(self):
        self.render = False

    def GetState(self):
        return self.render

    def Render(self, screen):
        if self.render:
            screen.blit(self.img, self.pos)