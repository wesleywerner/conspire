# parts available for use per level number.
LEVEL_PARTS = {
    1: ('human male torso', 'human male head', 
        'human male left arm', 'human male right arm', 
        'human male left leg', 'human male right leg',
        ),
    2: ('alien torso', 'alien head', 
        'alien left arm', 'alien right arm', 
        'alien left leg', 'alien right leg',
        ),
}

# parts a level may start off with as in use
DEFAULT_PARTS = {
    1: (),
    2: (),
}

# parts required to complete a level
COMPLETION_PARTS = {
    1: ('human male torso', 'human male head', 
        'human male left arm', 'human male right arm', 
        'human male left leg', 'human male right leg',
        ),
    2: ('alien torso', 'alien head', 
        'alien left arm', 'alien right arm', 
        'alien left leg', 'alien right leg',
        ),
}

LEVEL_SCENARIOS = (
    "Welcome to Conspiracy-101, soldier! " \
    "We represent some -ahem- secretive global interests. " \
    "The best way to predict the future, is to invent it. " \
    "But you know all this, hence why you are here, soldier. " \
    " " \
    "Your first job is to construct a facade corpse. " \
    " " \
    "",
)

class Builder(object):
    """
    Provides the body / item builder data and logic.
    
    """
    
    def __init__(self, model):
        
        self.model = model
        self.used_parts = []
    
    def refresh_parts(self):
        self.used_parts = list(DEFAULT_PARTS.get(self.model.level, []))

    def get_level_parts(self):
        """
        Get a list of all the parts that are allowed on the current level.
        
        """

        combined = []
        for k, v in LEVEL_PARTS.items():
            if k <= self.model.level:
                combined.extend(v)
        return combined
