STATE_MENU = 1
STATE_BUILD = 2
STATE_UFO = 3
STATE_FLIGHT = 4
STATE_RESULTS = 5
STATE_END = 100

# parts available for use per level number.
LEVEL_PARTS = {
    1: ('tax returns', 'shopping list', 'todo list',
        'ludum dare comments', 'bank accounts',
        'website passwords', 'IP address scamlist',
        ),
    2: ('human torso', 'human head', 
        'human left arm', 'human right arm', 
        'human left leg', 'human right leg',
        'website passwords', 'todo list', 'alien left leg',
        ),
    3: ('alien torso', 'alien head', 
        'alien left arm', 'alien right arm', 
        'alien left leg', 'alien right leg',
        'human torso', 'human head', 'human left arm',
        ),
    4: ('codex page I', 'codex page II', 'codex page III',
        'codex page IV', 'codex page V', 'codex page VI',
        'biblical references', 'book of psalms', 'book of tomas',
        'todo list', 'ludum dare comments'
        ),
    5: ('ptreodactyl torso', 'ptreodactyl skull',
        'ptreodactyl right wing', 'ptreodactyl left wing',
        'cyclops right arm', 'cyclops left leg',
        'human left arm', 'human left leg',
        ),
    6: ('alien torso', 'alien head', 
        'alien left arm', 'alien right arm', 
        'alien left leg', 'alien right leg',
        'trex torso', 'trex head', 'trex tail', 'trex legs',
        'human torso', 'human head', 
        'human left arm', 'human right arm', 
        'human left leg', 'human right leg',
        ),
        
}

    #500: ('cyclops torso', 'cyclops skull', 
        #'cyclops right arm', 'cyclops left arm', 
        #'cyclops right leg', 'cyclops left leg',
        #),
    

# parts a level may start off with as in use
DEFAULT_PARTS = {
    1: ('shopping list', 'ludum dare comments'),
    3: ('human torso', 'human head', 'human left arm',),
    4: ('todo list', 'codex page I',),
    5: ('ptreodactyl left wing', 'cyclops right arm', 'human left leg',),
}

# parts required to complete a level
COMPLETION_PARTS = {
    1: ('tax returns', 'bank accounts', 
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
    4: ('codex page I', 'codex page II', 'codex page III',
        'codex page IV', 'codex page V', 'codex page VI',
        ),
    5: ('ptreodactyl torso', 'ptreodactyl skull',
        'ptreodactyl right wing', 'ptreodactyl left wing',
        ),
    6: ('alien torso', 'alien head', 
        'alien left arm', 'alien right arm', 
        'alien left leg', 'alien right leg',
        'trex torso', 'trex head', 'trex tail', 'trex legs'
        ),
}

LEVEL_SCENARIOS = (
    "skip",
    
    "Welcome to Conspiracy 101, agent!" \
    "\n" \
    "Use your arrows or mouse wheel to scroll through this briefing." \
    "\n" \
    "We represent certain global interests. " \
    "These interests are kept hidden from the public, they are " \
    "privately funded and have access to the top levels government." \
    "\n" \
    "To start you off, we need to forge some papers. Our goal is to " \
    "discredit a high ranking official who is refusing cooperation " \
    "with our fine organization. We hope this move will make him " \
    "reconsider." \
    "\n" \
    "Compile fake papers for tax returns and bank accounts. " \
    "These figures match up to a internet scamming operation this " \
    "individual is apparently running, so include lists of website " \
    "passwords and IP addresses." \
    "\n" \
    "Do this by placing the correct items in the green area below. " \
    "When you are done proceed to plant the evidence, " \
    "the evidence will be carried by aircraft via remote control. " \
    "At a critical moment, you will force crash the craft, ensuring " \
    "the evidence is discovered." \
    "\n" \
    "Good luck, and welcome to the team, Agent!",

    "...anyway, welcome back, Agent! We have a situation..." \
    "\n" \
    "A problematic official is suspected of being a double agent. " \
    "We are going to make him disappear from public by faking his death, " \
    "while keeping him under ground for 'questioning'." \
    "\n" \
    "Construct a fake human body, as accurately as possbile. " \
    "The body will be found at the air crash site you will coordinate. " \
    "\n" \
    "Report back after the mission for debriefing.",
    
    "We are in the business of predicting the future, Agent! " \
    "And the best way to predict the future, is to invent it!" \
    "\n" \
    "We have a situation with one of our underground testing fascilities, " \
    "rumors are spreading of it's existence, and we cannot allow this. " \
    "We need a distraction for the media, and conspiracy theorists love " \
    "nothing more than a good alien story! " \
    "\n" \
    "Contruct a faux alien corpse, you will be flying it remotely in " \
    "one of our top-secret super experimental aircraft. Remember to " \
    "down it in the green zone for optimal mission success." \
    "\n" \
    "Well what are you waiting for, you are not in preschool " \
    "any more!",
    
    "A pertinent problem has arisen regarding the highest persons " \
    "in state, specifically the ones involved in the secular movements. " \
    "\n" \
    "In exchange for invaluable information from these informants we " \
    "are doing them a favor." \
    "\n" \
    "Construct a faux codex book to decode ancient texts. " \
    "This will gain leverage over the public." \
    "\n" \
    "The codex will be taken from the crash site, by a fellow agent, " \
    "and secured in another location for discovery. " \
    "\n" \
    "Remember to dot your i's and cross your t's.",
    
    "Our friends over at the dept. of evolution made a very generous " \
    "donation in our behalf, gaining notoriety with very important " \
    "higher-ups. " \
    "\n" \
    "As a sign of good faith, you will construct a pterodactyl skeleton " \
    "to be flown out to an undisclosed location." \
    "\n" \
    "This will serve their agenda nicely.",

    "Good day, Agent!" \
    "\n" \
    "Today is a very special day, we are going to combine the ultimate " \
    "of myths. A lot of people are unsure about the existence of " \
    "extra terrestrials, and many others the same about dinosaurs. " \
    "We will play on their uncertainty of both and create a story " \
    "to distract everybody from what is really going on in the world! " \
    "\n" \
    "You must construct one alien corpse, and one T-rex skeleton. " \
    "The cover story is that dinosaurs were in fact alien of origin." \
    "\n" \
    "Keep this up, Agent, and one day you'll be the one making up these stories!",

)

# affects the wording used in reports.
# try these:
# political, myth
SCENARIO_TYPE = (
    'skip',
    'political',
    'political',
    'myth',
    'myth',
    'myth',
    'myth',
    '',
)

# determine the type of the item to build, maps to levels.
ITEM_TYPES = (
    'skip',
    'documents',
    'high ranking officials body',
    'alien corpse',
    'biblical codex',
    'pterodactyl skeleton',
    'alien corpse and T-rex skeleton',
    '',
)

# determine the method of evidence deployment
TACTICAL_TYPE = (
    0,
    STATE_FLIGHT,
    STATE_FLIGHT,
    STATE_UFO,
    STATE_FLIGHT,
    STATE_FLIGHT,
    STATE_UFO,
)
