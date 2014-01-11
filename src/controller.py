import os
import pygame
from pygame.locals import *
from model import *
from view import View

class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = True
        
    def process_input(self):
        
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                self.running = False
        
            elif event.type == KEYDOWN:
        
                if event.key == K_ESCAPE:
                    self.running = False
                else:
                    view.keyDown(event.key)
                    
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    view.mouseWheelUp()
                elif event.button == 5:
                    view.mouseWheelDown()
                else:
                    view.mouseDown()
                
            elif event.type == MOUSEBUTTONUP:
                view.mouseUp()
                    

if __name__ == "__main__":
    # switch to this path to point relative paths to resources
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    model = Model()
    view = View(1024, 768, model)
    controller = Controller(model, view)
    
    # move along debugging
    model.level = model.level + 1
    model.set_state(STATE_BUILD)
    
    while controller.running:
        controller.process_input()
        model.turn()
        view.blit()
