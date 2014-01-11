import random

class UFOTactical(object):
    
    def __init__(self, model):
        self.model = model
        self.distance_from_goal = 0
        self.fighter_jets = []
        self.new_jets = 0
        self.clock = 0

    def reset_goal(self):
        self.clock = 0
        self.distance_from_goal = 750
        self.fighter_jets = []
    
    @property
    def max_jets(self):
        return 1 + int(self.model.level / 2.0)
    
    def deploy_jet(self):
        self.new_jets -= 1
    
    def update(self):
        self.clock += 1
        self.distance_from_goal -= 1
        if self.distance_from_goal < 0:
            self.distance_from_goal = 0
        
        if self.clock > 26:

            if len(self.fighter_jets) < self.max_jets:
                if random.randint(1, 100) < 10:
                    self.fighter_jets.append(random.randint(150, 300))
            
            for index, dist in enumerate(self.fighter_jets):
                if dist > 0:
                    dist -= 1
                    self.fighter_jets[index] = dist
                    if dist == 0:
                        self.new_jets += 1

    @property
    def jet_distances(self):
        return self.fighter_jets
