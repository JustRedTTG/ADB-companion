import threading
from drawing import *
from drawing.colorpallet import colorpallet
from drawing.images import images

class Halt:
    def __init__(self, command):
        self.active = False
        self.thread = threading.Thread(target=Halt.deamon, args=(self,), daemon=True)

    def deamon(self):
        while self.active:
            for pe.event.c in pe.event.get():
                pe.event.quitcheck()
            pe.fill.full(colorpallet['input-wait'])
            pe.display.update()

    def run(self):
        self.active = True
        self.thread.start()
    def stop(self): self.active = False