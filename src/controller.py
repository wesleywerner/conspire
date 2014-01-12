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
        self.last_state = STATE_BUILD
        
    def process_input(self):
        
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                self.running = False
        
            elif event.type == KEYDOWN:
        
                # Q KEY
                # Exit if we are in the menu state
                if event.key == K_q:
                    if self.model.state == STATE_MENU:
                        self.running = False
                
                # ESCAPE KEY
                # Always move to the menu
                # after remembering the current state for resume.
                elif event.key == K_ESCAPE:
                    if not self.model.state == STATE_MENU:
                        self.last_state = self.model.state
                        self.model.set_state(STATE_MENU)

                # SPACE BAR
                elif event.key == K_SPACE:
                    
                    # move to a game state, either the default state
                    if self.model.level == 0:
                        self.model.level = 1
                        
                    # or the last recorded state.
                    elif self.model.state == STATE_MENU:
                        self.model.set_state(self.last_state)
                    
                    # results screen moves to the next level
                    elif self.model.state == STATE_RESULTS:
                        self.model.level += 1
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
    view = View(600, 600, model)
    controller = Controller(model, view)

    while controller.running:
        controller.process_input()
        model.turn()
        view.blit()
