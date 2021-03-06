# Just some global vars for caps (dont have to use them)
resi_cap = 26
stat_cap = 75
skill_cap = 11


# Evaluation function samples
def f0(x): return 0.1 * x
def linear(x): return x
def must_cap_stat(x):
    if x < stat_cap:
        return 0
    else:
        return x

def resi(x):
    if x < 15:
        return 0.4 * x
    else:
        return 1.2 * x

# Define attributes (you are interested in) and their cap (your cap) here
# Format: 'ATTRIBUTE': {CAP, EVALUATION_FUNCTION}, ...
attributes = {
    'Crush Resist': (resi_cap, resi),
    'Slash Resist': (resi_cap, resi),
    'Thrust Resist': (resi_cap, resi),
    'Heat Resist': (resi_cap, resi),
    'Cold Resist': (resi_cap, resi),
    'Matter Resist': (resi_cap, resi),
    'Energy Resist': (resi_cap, resi),
    'Spirit Resist': (resi_cap, resi),
    'Body Resist': (resi_cap, resi),
    'Strength Resist': (stat_cap, f0),
    'Constitution': (stat_cap, linear),
    'Dexterity': (stat_cap, must_cap_stat),
    'Empathy': (stat_cap, linear),
    'Hits': (200, f0),
    'Regrowth': (skill_cap, linear),
    'Nurture': (skill_cap, linear),
    'Nature': (skill_cap, linear)
}

# Synonyms for slots
slot_synonyms = {
    'Chest':    ['Chest', 'Hauberk', 'Torso'],
    'Arms':     ['Sleeves'],
    'Legs':     ['Greaves'],
    'Head':     ['Helm'],
    'Hands':    ['Gloves', 'Gauntlets'],
    'Feet':     ['Boots'],
    'Neck':     ['Necklace', 'Choker'],
    'Jewel':    ['Gem'],
    'Cloak':    ['Cloak'],
    'Ring':     ['Ring'],
    'Wrist':    ['Bracer'],
    'Belt':     ['Belt'],
    'RHand':    ['Weapon', 'Hammer', 'Sword', 'Dagger', 'Rapier', 'Shillelagh'],
    'LHand':    ['Shield', 'Buckler']
}

# Synonyms for attributes
attribute_synonyms = {
    'Acuity': ['Empathy'],
    'All magic skills': ['Regrowth', 'Nurture', 'Nature'],
    'All melee skills': ['Blades']
}