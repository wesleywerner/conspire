STATE_MENU = 1
STATE_BUILD = 2
STATE_UFO = 3
STATE_FLIGHT = 4
STATE_RESULTS = 5

# parts available for use per level number.
LEVEL_PARTS = {
    1: ('tax returns', 'shopping list', 'todo list',
        'ludum dare comments', 'bank accounts',
        'website passwords', 'IP address scamlist',
        ),
    2: ('human torso', 'human head', 
        'human left arm', 'human right arm', 
        'human left leg', 'human right leg',
        ),
    3: ('alien torso', 'alien head', 
        'alien left arm', 'alien right arm', 
        'alien left leg', 'alien right leg',
        ),
    4: ('trex torso', 'trex head', 'trex tail', 'trex legs'),
    5: ('cyclops torso', 'cyclops skull', 
        'cyclops right arm', 'cyclops left arm', 
        'cyclops right leg', 'cyclops left leg',
        ),
    6: ('ptreodactyl torso', 'ptreodactyl skull',
        'ptreodactyl right wing', 'ptreodactyl left wing',
        ),
    
}

# parts a level may start off with as in use
DEFAULT_PARTS = {
    1: ('shopping list', 'ludum dare comments'),
}

# parts required to complete a level
COMPLETION_PARTS = {
    1: ('tax returns', 'bank accounts', 
        'website passwords', 'IP address scamlist',
        ),
    0: ('human torso', 'human head', 
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
    "Use your arrows or mouse wheel to scroll through this briefing." \
    "\n" \
    "We represent certain global interests that affect " \
    "life as we know it. These interests are kept above top secret, " \
    "privately funded with access to any level of government." \
    "\n" \
    "To start you off, we need to forge some papers. Our goal is to " \
    "discredit a high ranking official who is refusing cooperation " \
    "with our fine organization. We hope this move will make him " \
    "reconsider." \
    "\n" \
    "Compile papers for falsified tax returns and bank accounts. " \
    "These figures match up to a internet scamming operation this " \
    "individual is apparently running, so include lists of website " \
    "passwords and IP addresses." \
    "\n" \
    "Do this by placing the correct items in the green area below. " \
    "When you are done proceed to plant the evidence. " \
    "You will deploy it via a fake crash landing." \
    "\n" \
    "Good luck, and welcome to the team, Agent!",


    "We have 'collected' a problematic official we suspect is a double agent. " \
    "We are going to make them disappear by faking their death. " \
    "\n" \
    "Construct a fake human body in the green area, as accurately as possbile." \
    "\n" \
    
    "We are in the business of predicting the future, " \
    "and the best way to predict the future, is to invent it!" \
    "\n" \
    "We have a situation with one of our underground testing fascilities, " \
    "rumors are spreading of it's existence, and we cannot allow this. " \
    "We need a distraction for the media." \
    "",
    
    "scenario #3",
    "scenario #4",
    "scenario #5",
)

# determine the type of the item to build, maps to levels.
ITEM_TYPES = (
    'body',
    'body',
    'body',
)

# determine the method of evidence deployment
TACTICAL_TYPE = (
    0,
    STATE_FLIGHT,
    STATE_UFO,
)
