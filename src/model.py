import os
import random
from model_builder import *
from const import *

class UFOTactical(object):
    
    # game ticks
    TIME_TO_WAIT_BEFORE_ENGAGING_JETS = 200
    
    def __init__(self, model):
        self.model = model
        self.distance_from_goal = 0
        self.fighter_jets = []
        self.new_jets = 0
        self.clock = 0

    def reset_goal(self):
        self.clock = 0
        self.distance_from_goal = random.randint(1000, 2000)
        self.fighter_jets = []
    
    @property
    def max_jets(self):
        return 2 + int(self.model.level / 2.0)
    
    def deploy_jet(self):
        self.new_jets -= 1
    
    def update(self):
        self.clock += 1
        self.distance_from_goal -= 1
        if self.distance_from_goal < 0:
            self.distance_from_goal = 0
        
        if self.clock > self.TIME_TO_WAIT_BEFORE_ENGAGING_JETS:

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
        self.ufotactical = UFOTactical(self)
        self.mission_success = False
        self.results = ''
        self.is_new_level = False
        
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
        if value > len(LEVEL_SCENARIOS):
            #self._level = 0
            self.set_state(STATE_END)
        else:
            self._level = value
            self.is_new_level = True
            self.builder.refresh_parts()
            self.ufotactical.reset_goal()
            self.notify('levelup', value)
            self.set_state(STATE_BUILD)
            self.is_new_level = False

    def set_state(self, new_state):
        """
        Set a new game state, as given by the STATE_ constants above.
        """
        
        if self.state != new_state:
            self.state = new_state
            if new_state == STATE_RESULTS:
                self.analyze_results()
            self.notify('state', new_state)
    
    def analyze_results(self):
        """
        Build the results from all played values.
        
        """
        
        if self.level >= len(ITEM_TYPES):
            print('Warning: no item types defined for level %s' % self.level)
            return
        if self.level >= len(TACTICAL_TYPE):
            print('Warning: no tactical types defined for level %s' % self.level)
            return
        
        # set item types
        item_type = ITEM_TYPES[self.level]
        mission_type = TACTICAL_TYPE[self.level]
        
        replacers = {
            'item': item_type,
            'accuracy': self.builder.accuracy,
        }
        
        # analyze tactical outcome
        if self.mission_success:
            replacers['outcome'] = 'SUCCESS'
        else:
            replacers['outcome'] = 'FAILURE'
    
        # intro
        intro = random.choice((
            'Today, Scientists have discovered one %(item)s ' \
            'during a recent excavation near a historic ruin.',
            'Students who got lost during a school trip, stumbled ' \
            'upon a remarkable %(item)s yesterday.',
            'A demolition site has unearthed a rare %(item)s, which ' \
            'was luckily not damaged during the detonation.',
            'Oil drilling company F.U. accidentally unearthed a %(item)s, ' \
            'officials report. They are using it as a diversion from ' \
            'recent oil spills.'
            ))
        
        replacers['intro'] = (intro % replacers)
        
        # weirdness determines public opinion.
        # accuracy of the item built sets the base for believability.
        # other minor incidents will affect it thereafter.
        weirdness = 10 - int(self.builder.accuracy / 10.0)
        
        # mission failure increase weirdness
        if not self.mission_success:
            weirdness += 3
        
        # bodies have arms & legs swapped around
        
        opinion = random.choice((
            '"The world is very excited about this discovery!", ' \
            'expers said. "It will change everything, it is a great ' \
            'moment for mankind indeed!"',
            'Newspapers and internet blogs proclaim this the biggest ' \
            'discovery since sliced bread, and say it heralds in a ' \
            'new age for humankind.',
            'Popularity over this event is causing stocks to rise ' \
            'as collectors flock at the opportunity for this rare ' \
            'item. Investors say the world will be a better place ' \
            'after all.'
            ))
            
        if weirdness > 0:
            if weirdness <= 3:
                opinion = 'Conspiracist websites are venting about ' \
                    'the authenticity of the %(item)s. Authorities ' \
                    'can neither substantiate nor deny these claims, ' \
                    'and the %(item)s will be wondered about for many ' \
                    'decades to come.'
            elif weirdness <= 6:
                opinion = 'The %(item)s in question seems to be authentic, ' \
                    'yet minor details leave experts dumbfounded and ' \
                    'questioning the legitimacy of it. ' \
                    'It will remain another unanswered mystery unless ' \
                    'more evidence comes to light.'
            elif weirdness <= 9:
                opinion = 'The %(item)s seems to bea faux, enough ' \
                    'inconsistencies exist to make the scientific ' \
                    'community unbelievers, but the loyal ' \
                    'cult followers and conspiracists refuse to deny ' \
                    'this discovery as a sign of the truth.'
            else:
                opinion = 'Experts found multiple flaws in the ' \
                    '%(item)s, it is known to be falsified. Authorities ' \
                    'have opened investigations, your reputation is tarnished. ' \
                    'Hordes of conspiracists fall to the streets in uproar ' \
                    'for something they now know is a lie!'
        
        opinion = opinion % replacers
        replacers['opinion'] = opinion
        
        chance = ''
        if self.builder.accuracy >= 100:
            chance = 'very high'
        elif self.builder.accuracy >= 70:
            chance = 'high'
        elif self.builder.accuracy >= 50:
            chance = 'medium'
        elif self.builder.accuracy >= 30:
            chance = 'low'
        elif self.builder.accuracy >= 0:
            chance = 'terrible'
        replacers['chance'] = chance
        
        self.results = 'Briefing and preperation' \
            '\n' \
            'One %(item)s was constructed, it\'s authenticity was determined ' \
            'to be %(accuracy)s percent, giving us a believability ' \
            'rating of "%(chance)s".' \
            '\n' \
            'Mission Result: %(outcome)s' \
            '\n' \
            'MEDIA STATEMENT EXTRACT' \
            '\n' \
            '%(intro)s %(opinion)s' \
            '\n' \
            ''
        
        self.results = (self.results % replacers)
        print(self.results)

    def turn(self):
        """
        Perform a game turn as determined by the FPS of the view.
        """
        
        if self.state in (STATE_UFO, STATE_FLIGHT):
            self.ufotactical.update()
            if self.ufotactical.new_jets:
                self.ufotactical.deploy_jet()
                self.notify('deploy fighter jet', None)
