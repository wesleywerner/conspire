import os
import random
from model_builder import Builder

STATE_MENU = 1
STATE_BUILD = 2
STATE_UFO = 3
STATE_BURY = 4
STATE_RESULTS = 5

class Model(object):
    """
        The model that manages the game state."""
    def __init__(self, seed=None):
        """ 
        
        """
        
        self.state = STATE_MENU
        self.score = 0
        self._level = 0
        self.builder = Builder(self)
        
        # listeners get notified of model events
        self.listeners = []
        
        # allow replaying a game
        if seed:
            random.seed(seed)

    def register_listener(self, listener):
        self.listeners.append(listener)

    def notify(self, event_name, data):
        for listener in self.listeners:
            listener(event_name, data)
    
    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self, value):
        self._level = value
        self.builder.refresh_parts()
        self.notify('levelup', value)

    def set_state(self, new_state):
        """
        Set a new game state, as given by the STATE_ constants above.
        """
        
        self.state = new_state
        self.notify('state', new_state)
        
    def turn(self):
        """
        Perform a game turn as determined by the FPS of the view.
        """
        
        pass
