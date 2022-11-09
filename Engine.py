from Actor import Actor

class Engine:
    actors:Actor = []

    def __init__(self):
        pass

    def AddActor(self, actor:Actor):
        self.actors.append(actor)

    def Start(self):
        for i in range(len(self.actors)):
            self.actors[i].Start()

    def Update(self, dt:float):
        for i in range(len(self.actors)):
            self.actors[i].Update(dt)

    def Render(self, screen):
        for i in range(len(self.actors)):
            self.actors[i].Render(screen)
