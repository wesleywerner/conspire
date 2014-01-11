# parts available for use per level number.
LEVEL_PARTS = {
    1: ('human torso', 'human head', 
        'human left arm', 'human right arm', 
        'human left leg', 'human right leg',
        ),
    2: ('alien torso', 'alien head', 
        'alien left arm', 'alien right arm', 
        'alien left leg', 'alien right leg',
        ),
}

# parts a level may start off with as in use
DEFAULT_PARTS = {
    1: ('human head',),
}

# parts required to complete a level
COMPLETION_PARTS = {
    1: ('human torso', 'human head', 
        'human left arm', 'human right arm', 
        'human left leg', 'human right leg',
        ),
    2: ('alien torso', 'alien head', 
        'alien left arm', 'alien right arm', 
        'alien left leg', 'alien right leg',
        ),
}

LEVEL_SCENARIOS = (
    "Welcome to Conspiracy 101, agent!" \
    "\n" \
    "We represent certain global interests that affect " \
    "life as we know it. These interests are kept above top secret, " \
    "privately funded with access to any level of govt, we aim to " \
    "predict the future." \
    "\n" \
    "And the best way to predict the future, is to invent it. " \
    "So you could say our business is the future.",
)

class Builder(object):
    """
    Provides the body / item builder data and logic.
    
    """
    
    def __init__(self, model):
        
        self.model = model
        self._used_parts = []
    
    def refresh_parts(self):
        self._used_parts = list(DEFAULT_PARTS.get(self.model.level, []))

    def get_level_parts(self):
        """
        Get a list of all the parts that are allowed on the current level.
        
        """

        self.refresh_parts()
        combined = []
        for k, v in LEVEL_PARTS.items():
            if k <= self.model.level:
                combined.extend(v)
        return combined

    def add_part(self, part):
        """
        Add a part to be used in buidling a body or item.
        
        """
        
        if self._used_parts.count(part) == 0:
            self._used_parts.append(part)
            print('added part %s' % (part,))
    
    def remove_part(self, part):
        """
        Remove a part from construction.
        
        """
        
        if part in self._used_parts:
            self._used_parts.remove(part)
            print('removed part %s' % (part,))

    def part_used(self, part):
        """
        Returns if a part is in use.
        
        """
        
        return part in self._used_parts

    @property
    def accuracy(self):
        """
        Gets a percentage of accuracy of the build body
        as determined by the completion parts.
        
        """
        
        matches = 0.0
        for part in self._used_parts:
            if part in COMPLETION_PARTS[self.model.level]:
                matches += 1.0
        if matches == 0.0:
            return 0
        else:
            return round(matches / len(COMPLETION_PARTS[self.model.level]) * 100)
