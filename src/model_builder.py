from const import *

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
