import math
import random
import statistics


def get_random_class():
    class_list = ["Barbarian", "Bard", "Cleric",
                 "Druid", "Fighter", "Monk",
                 "Paladin", "Ranger", "Rogue",
                 "Sorcerer", "Warlock", "Wizard"]
    return random.choice(class_list)

def get_random_race():
    subrace_list = ["Hill Dwarf", "Mountain Dwarf",
                   "High Elf", "Wood Elf", "Drow",
                   "Lightfoot Halfling", "Stout Halfling",
                   "Regular Human", "Variant Human",
                   "Dragonborn",
                   "Forest Gnome", "Rock Gnome",
                   "Half-Elf",
                   "Half-Orc",
                   "Tiefling"]
    return random.choice(subrace_list)

def stat_roll_4d6d1():
    x = [random.randint(1,6) for _ in range(4)]
    return sum(sorted(x, reverse=True)[0:3])

def generate_stat_block():
    x = sorted([stat_roll_4d6d1() for _ in range(6)], reverse=True)
    return x

def get_race_dex_bonus(race):
    dex_bonuses = {"Hill Dwarf":0, "Mountain Dwarf":0,
                   "High Elf":2, "Wood Elf":2, "Drow":2,
                   "Lightfoot Halfling":2, "Stout Halfling":2,
                   "Regular Human":1, "Variant Human":1,
                   "Dragonborn":0,
                   "Forest Gnome":1, "Rock Gnome":0,
                   "Half-Elf":1,
                   "Half-Orc":0,
                   "Tiefling":0}
    return dex_bonuses[race]

def get_dex_priority(player_class):
    priorities = {"Barbarian":2, "Bard":2, "Cleric":3,
                 "Druid":2, "Fighter":0, "Monk":0,
                 "Paladin":2, "Ranger":0, "Rogue":0,
                 "Sorcerer":2, "Warlock":2, "Wizard":1}
    return priorities[player_class]

def get_dex_bonus(score_array, player_class, race):
    priority = get_dex_priority(player_class)
    # I should probably assume nobody will dump DEX, but if it's not seriously important it's randomly selected here
    if priority > 1:
        priority = random.randint(2, 5)
    return score_to_bonus(score_array[priority] + get_race_dex_bonus(race))

def score_to_bonus(score):
    return math.floor(score/2 - 5)

def ac(armor, dex_bonus, shield):
    shield_bonus = 0
    if shield:
        shield_bonus = 2
    if armor == "None":
        return 10 + dex_bonus + shield_bonus
    heavy = {"Ring Mail": 14, "Chain Mail": 16, "Splint": 17, "Plate": 18}
    if armor in heavy.keys():
        return heavy[armor] + shield_bonus
    light = {"Padded":11+dex_bonus, "Leather":11+dex_bonus, "Studded Leather":12+dex_bonus}
    if armor in light.keys():
        return light[armor] + shield_bonus
    medium = {"Hide":12+min(2, dex_bonus), "Chain Shirt":13+min(2, dex_bonus),
              "Scale Mail":14+min(2, dex_bonus), "Breastplate":14+min(2, dex_bonus),
              "Half Plate":15+min(2, dex_bonus)}
    if armor in medium.keys():
        return medium[armor] + shield_bonus
    print(armor, dex_bonus, shield)
    raise ValueError

def get_armor(player_class):
    if player_class == "Bard" or player_class == "Druid" or player_class == "Rogue" or player_class == "Warlock":
        return "Leather"
    elif player_class == "Paladin":
        return "Chain Mail"
    elif player_class == "Cleric":
        return random.choice(["Scale Mail", "Leather", "Chain Mail"])
    elif player_class == "Fighter":
        return random.choice(["Chain Mail", "Leather"])
    elif player_class == "Ranger":
        return random.choice(["Scale Mail", "Leather"])
    else:
        return "None"

def get_shield(player_class):
    if player_class == "Cleric" or player_class == "Druid":
        return True
    elif player_class == "Fighter" or player_class == "Paladin":
        return random.choice([True, False])
    else:
        return False

def random_character():
    stat_block = generate_stat_block()
    race = get_random_race()
    player_class = get_random_class()
    armor = get_armor(player_class)
    shield = get_shield(player_class)
    ac_score = ac(armor, get_dex_bonus(stat_block, player_class, race), shield)
    return ac_score

print(statistics.mean([random_character() for _ in range(10000)]))
