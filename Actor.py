from abc import abstractmethod

class Actor:
    tag:str

    def __init__(self, tag:str):
        self.tag = tag

    @abstractmethod
    def Render(self, screen):
        pass

    @abstractmethod
    def Start(self):
        pass

    @abstractmethod
    def Update(self, dt:float):
        pass

    def GetTag(self):
        return self.tag
