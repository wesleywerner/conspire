import random

class UFOTactical(object):
    
    def __init__(self, model):
        self.model = model
        self.distance_from_goal = 0
        self.fighter_jets = []
        self.new_jets = 0
        self.clock = 0

    def reset_goal(self):
        self.distance_from_goal = 10 + self.model.level + random.randint(0, 2)
        self.fighter_jets = []
    
    @property
    def max_jets(self):
        return 1 + int(self.model.level / 2.0)
    
    def deploy_jet(self):
        self.new_jets -= 1
    
    def update(self):
        self.clock += 1
        
        if self.clock > 260:

            if len(self.fighter_jets) < self.max_jets:
                if random.randint(1, 100) < 1:
                    self.fighter_jets.append(random.randint(150, 500))
            
            for index, dist in enumerate(self.fighter_jets):
                if dist > 0:
                    dist -= 1
                    self.fighter_jets[index] = dist
                    if dist == 0:
                        self.new_jets += 1

    @property
    def jets_distances(self):
        return self.fighter_jets
