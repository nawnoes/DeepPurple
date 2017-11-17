

class Observer:

    def update(self):
        #업데이트
        None
class Publisher:
    def add(self, observer):
        None
    def delete(self, observer):
        None
    def notifyObserver(self):
        None
class NewsMachin(Publisher):

    def __init__(self):
        self.obersers = []
        self. title
        self. news

    def add(self,observer):
        self.obersers.add(observer)
    def delete(self, observer):
        self.obersers.remove(observer)
    def notifyObserver(self):
        for ob in self.obersers:
            ob.update()
