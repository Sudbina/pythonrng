# RNG based weapon generator by Jack Gibson

import random
import math
from PIL import Image, ImageDraw, ImageFont

bases = ["Wand", "Sword", "Bow"]
rarities = [("Common",50), ("Uncommon",40), ("Magic",30), ("Rare",10), ("Legendary",3), ("Unique",1)]
prefixes = [("Screaming",20), ("Weeping",15),("Burning",10),("Almighty",5),("Dying",15),("Freezing",10),("Shocking",10)]
strength_suffixes = [("Strength",15),("Might",15),("Crushing",10),("Hulking",3)]
intelligence_suffixes = [("Focus",15),("Meditation",5),("Research",10),("Insight",15)]
dexterity_suffixes = [("Dodging", 15),("Swiftness",10),("Silence",10),("Cunning",15)]

def get_bgcolour_by_rarity(rarity_type):
    return {
        'Common': (255,255,255),
        'Uncommon': (5,255,63),
        'Magic': (15,143,255),
        'Rare': (255,255,15),
        'Legendary': (255,113,5),
        'Unique': (144,0,255)
    }[rarity_type]
    
def get_txtcolour_by_rarity(rarity_type):
    return {
        'Common': (0,0,0),
        'Uncommon': (0,0,0),
        'Magic': (255,255,255),
        'Rare': (0,0,0),
        'Legendary': (0,0,0),
        'Unique': (255,255,255)
    }[rarity_type]

def roll(list):
    # Pick from weighted list of prefixes
    choices = []
    for item, weight in list:
            choices.extend([item]*weight)
    return random.choice(choices)

def roll_rarity(rarity_type):
    # Generate rarity multiplier for damages and stats
    return {
        'Common': 1,
        'Uncommon': 1,
        'Magic': 1.3,
        'Rare': 2,
        'Legendary': 2.5,
        'Unique': 2.5
    }[rarity_type]

def roll_suffix(base_type, strength, intelligence, dexterity):
    # Make dictionary using weapon base base_type index to determine what skill type related suffix should be used
    return {
        'Sword': roll(strength),
        'Wand': roll(intelligence),
        'Bow': roll(dexterity)
    }[base_type]
    
def roll_base_damage(base_type, rarity_multiplier):
    # Roll base damage related to weapon base
    return {
        'Sword': random.randrange(6,11),
        'Wand': random.randrange(3,7),
        'Bow': random.randrange(4,9)
    }[base_type] * rarity_multiplier
    
def roll_enhanced_damage(base_damage, prefix, suffix, rarity_multiplier):
    # Generate random values for prefix and suffix damage modifiers
    a = {
        'Screaming': base_damage + random.randrange(2,7),
        'Weeping': base_damage + random.randrange(1,3),
        'Burning': base_damage + random.randrange(3,7),
        'Almighty': base_damage + random.randrange(7,14),
        'Dying': base_damage + random.randrange(1,7),
        'Freezing': base_damage + random.randrange(2,6),
        'Shocking': base_damage + random.randrange(3,7)
    }[prefix] * rarity_multiplier
    
    b = {
        'Strength': base_damage + random.randrange(1,8),
        'Might': base_damage + random.randrange(1,10),
        'Crushing': base_damage + random.randrange(1,12),
        'Hulking': base_damage + random.randrange(1,14),
        'Focus': base_damage + random.randrange(1,8),
        'Meditation': base_damage + random.randrange(1,13),
        'Research': base_damage + random.randrange(1,10),
        'Insight': base_damage + random.randrange(7,9),
        'Dodging': base_damage + random.randrange(1,8),
        'Swiftness': base_damage + random.randrange(1,8),
        'Silence': base_damage + random.randrange(1,8),
        'Cunning': base_damage + random.randrange(1,9),
    }[suffix] * rarity_multiplier
      
    return round(a + b)
    

class Weapon:
    # Build weapon with base type, modifiers, stats
    base = random.choice(bases)
    rarity = roll(rarities)
    rarity_multiplier = roll_rarity(rarity)
    prefix = roll(prefixes)
    suffix = roll_suffix(base, strength_suffixes, intelligence_suffixes, dexterity_suffixes)
    base_damage = roll_base_damage(base, rarity_multiplier)
    enhanced_damage = math.trunc(roll_enhanced_damage(base_damage, prefix, suffix, rarity_multiplier))

print(Weapon.prefix + " " + Weapon.base + " of " + Weapon.suffix)
print(Weapon.rarity)
print("Damage:",Weapon.enhanced_damage)

weapon_constructed_name = Weapon.prefix + " " + Weapon.base + " of " + Weapon.suffix


# Generate weapon card image

img = Image.new('RGB', (400, 700), color=get_bgcolour_by_rarity(Weapon.rarity))
 
name_font = ImageFont.truetype('/Library/Fonts/Inter-UI-BlackItalic.ttf', 22)
damage_font = ImageFont.truetype('/Library/Fonts/Inter-UI-BlackItalic.ttf', 20)
rarity_font = ImageFont.truetype('/Library/Fonts/Inter-LightItalic-BETA.ttf', 15)

d = ImageDraw.Draw(img)
d.text((10,10), weapon_constructed_name, font=name_font, fill=get_txtcolour_by_rarity(Weapon.rarity))
d.text((10,35), Weapon.rarity, font=rarity_font, fill=get_txtcolour_by_rarity(Weapon.rarity))
d.text((10,55), str(Weapon.enhanced_damage) + " Damage", font=damage_font, fill=get_txtcolour_by_rarity(Weapon.rarity))
 
img.save('generated-item.png')