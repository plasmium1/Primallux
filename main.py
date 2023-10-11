import os
from magic import effectDict, spellDict
import replit
from tiles import tilesDict, interactionDict, Interactible, dialogueDict
#import saveData
from playerInventory import identifierDict, recipeDict, Recipe
from replit import db
from random import randint, choices, choice, sample
from ansi.colour import fg
from ansi.colour.rgb import rgb256
from ansi.colour.fx import reset
from quests import Quest, questsDict, moonreachQuests, defaultQuests, defaultRep
import sys
from itertools import count

black = "\u001b[30m"
red = "\u001b[31m"
green = rgb256(0x00, 0xff, 0x09)
orange = rgb256(0xd4, 0x71, 0x00)
silver = rgb256(0xbf, 0xbf, 0xbf)
yellow = "\u001b[93m"
gold = rgb256(0xe6, 0xcb, 0x02)
blue = "\u001b[34m"
magenta = "\u001b[95m"
cyan = rgb256(0x61, 0xff, 0xf4)
light_purple = rgb256(0xb0, 0x42, 0xff)
purple = rgb256(0xbe, 0x03, 0xfc)
white = "\u001b[37m"
bold = "\u001b[1m"
underline = "\u001b[4m"
italic = "\u001b[3m"
tilesetLegals = (
    "h", "help", "look", "l", "search", "north", "south", "east", "west", "n",
    "s", "e", "w", "wander", "inv", "inventory", "magic", "m", "int",
    "interact", "stats", "save", "up", "down", "skills", "quests"
)  #Public tuple for allowing checkIn to check the right values for each tile

defaultTileRespawns = {
    "Tile 1": 240,
    "Tile 3": 210,
    "Tile 9": 210,
	"Tile 31": 210,
    "Tile 32": 300,
    "Tile 36": 210,
    "Dungeon Tile 1": 205,
    "Dungeon Tile 2": 200,
    "Dungeon Tile 3": 255,
    "Dungeon Tile 4": 140,
    "Dungeon Tile 5": 450, 
    "Dungeon Tile 6": 450,
    "Dungeon Tile 7": 400,
    "Dungeon Tile 8": 480
}
#Default Tile Respawn timers so the code can reset the respawns once they've respawned already

defaultTileItems = {
    "Tile 1": 4,
    "Tile 3": 6,
    "Tile 32": 5,
    "Tile 36": 4,
    "Dungeon Tile 2": 3
}  #Keeps track of how many items there are for each tile.

defaultMobList = {
    "Tile 9": 6,
	"Tile 31": 3,
    "Tile 32": 4,
    "Dungeon Tile 1": 4,
    "Dungeon Tile 2": 3,
    "Dungeon Tile 3": 2,
    "Dungeon Tile 4": 3,
    "Dungeon Tile 5": 3,
    "Dungeon Tile 6": 3,
    "Dungeon Tile 7": 2,
    "Dungeon Tile 8": 1
}  #Assigns a limit on the amount of monsters in a specific tile.


#Declare and initialize items based on IDs
IDDict = identifierDict
#Stores IDs for items, keyed to their names


def roman_to_int(string): #Converts roman numerals to Python integers
    roman = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000,
        'IV': 4,
        'IX': 9,
        'XL': 40,
        'XC': 90,
        'CD': 400,
        'CM': 900
    }
    i = 0
    num = 0
    while i < len(string):
        if i + 1 < len(string) and string[i:i + 2] in roman:
            num += roman[string[i:i + 2]]
            i += 2
        else:
            num += roman[string[i]]
            i += 1
    return num


def properTitle(inp): #Capitalizes objects with titles following proper Engish titling format
    inp = inp.split(" ")
    inp[0] = inp[0].capitalize()
    inp[-1] = inp[-1].capitalize()
    n = 1
    for i in inp[1:-1]:
        if i.lower() not in ("in", "for", "of", "a", "an", "and", "on", "the"):
            inp[n] = i.title()

        n += 1
    ret = ""
    for i in inp:
        ret += i + " "
    ret = ret.strip()
    return ret


def save(): #Saves the user into their DB.
    global username
    record = {}
    record["Turns"] = turns
    record["Name"] = name
    record["Race"] = race
    record["Gender"] = gender
    record["Tile"] = tile
    record["Stats"] = stats
    record["Sub Stats"] = sub_stats
    record["Quest Progress"] = questProgress
    record["Reputation"] = reputation
    record["Tile Items"] = tileItems
    record["Mob List"] = mobList
    record["Met NPCs"] = metNPCs
    record["Killed NPCs"] = killedNPCs
    record["Skill Levels"] = skillLevels
    record["Tile Respawn"] = tileRespawn
    enterDict = {}
    for key, value in equipped.items():
        if type(value) != str:
            enterDict.update({key: value.dumpSaveRepresentation()})
        else:
            enterDict.update({key: value})
    record["Equipped"] = enterDict
    enterDict = {}
    for key, value in inventory.items():
        enterDict.update({key: value.dumpSaveRepresentation()})
    record["Inventory"] = enterDict
    enterDict = {}
    for key, value in statusEffects.items():
        string = ""
        placeholder = key.split(" ")
        string += placeholder[0] + "|" + str(roman_to_int(placeholder[1]))
        enterDict.update({string: value})
    record["Status Effects"] = enterDict
    username = input(reset + "Enter your account username: " + gold)
    if username not in db.keys():
        print(red + "That username doesn't exist!")
        return
    pwd = input(reset + "Enter your account password: " + gold)
    if db[username]["PWD"] != pwd:
        print(red + "Password and username do not match.")
        return
    db[username]["Data"] = record
    print(green + "Data Saved!", reset)
    return
"""
def stackTraceCounter(size=2):
    \"""Get stack size for caller's frame.
    \"""
    frame = sys._getframe(size)
    try:
        for size in count(size, 8):
            frame = frame.f_back.f_back.f_back.f_back.\
                f_back.f_back.f_back.f_back
    except AttributeError:
        while frame:
            frame = frame.f_back
            size += 1
        return size - 1

def stackOverflowPreventer():
    #Prevents stack overflow by warning the user to save and restart when recursion depth grows too deep. Will premptively stop the program before it reaches maximum stack depth. 

"""    #Will implement if it becomes a problem.


def statAssign():
    #Self explanatory
    #Assigns random starting stats in addition to the +10 base value. REROLLS ALLOWED.
    selector()
    global stats
    global sub_stats
    stats["Strength"] += randint(1, 10)
    stats["Constitution"] += randint(1, 10)
    stats["Dexterity"] += randint(1, 10)
    stats["Agility"] += randint(1, 10)
    stats["Perception"] += randint(1, 10)
    stats["Charisma"] += randint(1, 10)
    stats["Intelligence"] += randint(1, 10)
    stats["Wisdom"] += randint(1, 10)
    sub_stats["Max HP"] = stats["Constitution"] * 10
    print(cyan + name + ", Level " + str(stats["Level"]) + " " + gender + " " +
          race + ":")
    print(fg.blue("Strength: ") + green + str(stats["Strength"]))
    print(
        fg.blue("  Damage range (") + gold + "S-[melee-item]" + fg.blue("):"),
        fg.red, (stats["Strength"]), "-",
        (stats["Strength"] + sub_stats["Item Damage"]))
    sub_stats["Damage-Lower"] = stats["Strength"]
    sub_stats["Damage-Upper"] = stats["Strength"] + sub_stats["Item Damage"]
    print(fg.blue("Constitution: ") + green, stats["Constitution"])
    print(
        fg.blue("  Base health pool (") + gold + "C" + fg.blue("): ") + green +
        str(sub_stats["Max HP"]) + " points")
    sub_stats["Max HP"] = stats["Constitution"] * 10
    sub_stats["Current HP"] = sub_stats["Max HP"]
    print(fg.blue + "Perception: " + green + str(stats["Perception"]))
    print(fg.blue + "Dexterity: " + green + str(stats["Dexterity"]))
    print(
        fg.blue("  Crit Chance (") + gold + "P-D" + fg.blue("): ") + green +
        str(
            round((0.1 * stats["Dexterity"] *
                   (stats["Perception"]) * 0.01) + 1, 2)) + "%")
    sub_stats["Crit Chance"] = round(
        (0.05 * stats["Dexterity"] * (stats["Perception"]) * 0.01) + 1, 2)
    print(fg.blue + "Charisma: " + green + str(stats["Charisma"]))
    print(fg.blue + "Intelligence: " + green + str(stats["Intelligence"]))
    print(
        fg.blue("  Learn Chance Bonus (") + gold + "I-W" + fg.blue("): ") +
        green + str(
            round((stats["Intelligence"] * 0.1) *
                  (stats["Wisdom"] * 0.01) + 1, 2)) + "%")
    sub_stats["Learn Chance"] = round(
        (stats["Intelligence"] * 0.1) * (stats["Wisdom"] * 0.01) + 1, 2)
    sub_stats["Max MP"] = stats["Wisdom"] * 5
    sub_stats["Current MP"] = sub_stats["Max MP"]
    print(fg.blue + "Wisdom: " + green, stats["Wisdom"], reset)
    print(blue + "  Base mana pool (" + gold + "W" + blue + "): " +
          light_purple + str(sub_stats["Current MP"]) + "/" +
          str(sub_stats["Max MP"]))
    save = checkIn(("y", "n"), "str",
                   (cyan + "Save character?" + blue + " (Y/N) "))
    #Needs a save data function probably
    if save == "y":
        return
    else:
        stats = {
            "Level": 1,
            "Strength": 10,
            "Constitution": 10,
            "Dexterity": 10,
            "Agility": 10,
            "Perception": 10,
            "Charisma": 10,
            "Intelligence": 10,
            "Wisdom": 10
        }
        sub_stats = {
            "Max HP": 100,
            "Current HP": 100,
            "Max MP": 50,
            "Current MP": 50,
            "Item Damage": 0,
            "Crit Chance": 0.0,
            "Learn Chance": 0.0,
            "Damage-Upper": 0,
            "Damage-Lower": 0,
            "Defense": 0,
            "Ghost Silver": 0,
            "XP": 0,
            "XP Needed": 10,
            "XP Next Scale Up": 10,
            "Element Damage": {
                "Fire": 0,
                "Water": 0,
                "Earth": 0,
                "Air": 0,
                "Light": 0,
                "Dark": 0,
                "Wood": 0,
                "Metal": 0,
                "Sun": 0,
                "Moon": 0,
                "Star": 0
            },
            "Element Defense": {
                "Fire": 0,
                "Water": 0,
                "Earth": 0,
                "Air": 0,
                "Light": 0,
                "Dark": 0,
                "Wood": 0,
                "Metal": 0,
                "Sun": 0,
                "Moon": 0,
                "Star": 0
            }
        }
        statAssign()


def selector():
    #Character selector for character attribute bonuses based on selection.
    global race
    global gender
    global name

    print(cyan + "Pick your character race:")
    print(" Human" + gold + " (Charisma/Dexterity)")
    print(cyan + " Elf" + gold + " (Intelligence/Light Element)")
    print(cyan + " Dwarf" + gold + " (Strength/Constitution)")
    print(cyan + " Demon" + gold + " (Strength/Dark Element)")

    placeholder = checkIn(
        ("h", "e", "dw", "de", "human", "elf", "dwarf", "demon"), "str")
    if placeholder == "h" or placeholder == "human":
        stats["Charisma"] += 6
        stats["Dexterity"] += 6
        race = "Human"
    elif placeholder == "e" or placeholder == "elf":
        stats["Intelligence"] += 8
        sub_stats["Element Damage"]["Light"] += 6
        sub_stats["Element Defense"]["Light"] += 6
        sub_stats["Element Defense"]["Dark"] -= 6
        race = "Elf"
    elif placeholder == "dw" or placeholder == "dwarf":
        stats["Strength"] += 6
        stats["Constitution"] += 6
        race = "Dwarf"
    elif placeholder == "de" or placeholder == "demon":
        stats["Strength"] += 8
        sub_stats["Element Damage"]["Dark"] += 6
        sub_stats["Element Defense"]["Dark"] += 6
        sub_stats["Element Defense"]["Light"] -= 6
        race = "Demon"

    print(cyan + "Pick your character gender:")
    print(" Male" + gold + " (S-Co)")
    print(cyan + " Female" + gold + " (Ch-D)")
    inputGender = checkIn(("m", "f", "nb", "male", "female", "nonbinary"),
                          "str")
    if inputGender == "m" or inputGender == "male":
        stats["Strength"] += 8
        stats["Constitution"] += 10
        gender = "Male"
    elif inputGender == "f" or inputGender == "female":
        stats["Charisma"] += 8
        stats["Dexterity"] += 10
        gender = "Female"
    elif inputGender == "nb" or inputGender == "nonbinary":
        gender = "Non-Binary"

    name = input(cyan + "Enter your name: " + gold)


def checkIn(
    listLegals,
    inputType,
    message=""
):  #Method for a customized "Is this input allowed?" and "If so do this."
    if inputType == "str":
        inputVal = input(message)
        inputVal = inputVal.lower()
    elif inputType == "int":
        while True:
            try:
                inputVal = int(input(message))
                break
            except:
                pass
    while inputVal not in listLegals:
        print(red + "Invalid input. Please try again.", reset)
        if inputType == "str":
            inputVal = input(message)
            inputVal = inputVal.lower()
        elif inputType == "int":
            try:
                inputVal = int(input(message))
            except:
                inputVal = int(input(message))
    return inputVal


def showTilePossibleInputs(tileID): #Displays the possible inputs in tiles.
    thisTile = tilesDict[tileID]
    print(green + "Valid inputs: ")
    possibleInputs = "help, look, inventory, stats, skills, quests, wander, "
    if thisTile.getNearbyTiles() != {}:
        for key in thisTile.getNearbyTiles():
            possibleInputs += key.lower() + ", "
    if thisTile.getUpTile() != 0:
        possibleInputs += "up" + ", "
    if thisTile.getDownTile() != 0:
        possibleInputs += "down" + ", "
    if thisTile.getInteractible() != False:
        possibleInputs += "interact" + ", "
    possibleInputs = possibleInputs[:-2]
    print(reset + possibleInputs)


def statsCheck():  #In-game stat checker!
    global name, race, gender, tile, stats
    print(cyan + name + ", Level " + str(stats["Level"]) + " " + gender + " " +
          race + ":")
    print(red + "HP (Co): " + str(sub_stats["Current HP"]) + "/" +
          str(sub_stats["Max HP"]))
    print(light_purple + "MP (W): " + str(sub_stats["Current MP"]) + "/" +
          str(sub_stats["Max MP"]))
    print(green + "XP: " + str(sub_stats["XP"]) + "/" +
          str(sub_stats["XP Needed"]))
    print(silver + str(sub_stats["Ghost Silver"]) + " GS")
    print(fg.blue("Strength (S): ") + green + str(stats["Strength"]))
    print(
        fg.blue("  Damage range (") + gold + "S-[melee-item]" + fg.blue("):"),
        fg.red, (sub_stats["Damage-Lower"]), "-", (sub_stats["Damage-Upper"]))
    print(fg.blue("Constitution (Co): ") + green, stats["Constitution"])
    print(fg.blue + "Perception (P): " + green + str(stats["Perception"]))
    print(fg.blue + "Dexterity (D): " + green + str(stats["Dexterity"]))
    print(
        fg.blue("  Crit Chance (") + gold + "P-D" + fg.blue("): ") + green +
        str(sub_stats["Crit Chance"]) + "%")
    print(fg.blue + "Charisma (Ch): " + green + str(stats["Charisma"]))
    print(fg.blue + "Intelligence (I): " + green + str(stats["Intelligence"]))
    print(
        fg.blue("  Learn Chance Bonus (") + gold + "I-W" + fg.blue("): ") +
        green + str(sub_stats["Learn Chance"]) + "%")
    print(fg.blue + "Wisdom (W):" + green, stats["Wisdom"], reset)
    for key, value in sub_stats["Element Damage"].items():
        print(blue + key + " Damage: " + gold + str(value) + purple + " | " +
              blue + key + " Defense: " + gold +
              str(sub_stats["Element Defense"][key]))


def skillsCheck(): #Shows the user's skill levels.
    print(green + "-----{" + name + "'s Skills}-----")
    for key, value in skillLevels.items():
        if value > 0:
            print(blue + key + " Level: " + str(value))
        else:
            pass


#Inventory System
def inventoryMenu():
    print(gold + name + "'s" + green + " inventory")
    print(blue + "Options:")
    invChoicer = checkIn(
        ("list", "equip", "unequip", "consumable", "exit"), "str",
        (blue + "List, Equip, Unequip, Consumable, Exit " + gold))
    if invChoicer == "list":  #List all the items in your inventory. Doesn't show entries of items you don't have.
        if len(inventory) == 0:
            print(red + "You have nothing in your inventory.")
        for value in inventory.values():
            print(value)
    elif invChoicer == "equip":
        equipItems()
        inventoryMenu()
    elif invChoicer == "unequip":
        unequipItems()
        inventoryMenu()
    elif invChoicer == "consumable":
        consumableMenu()
        inventoryMenu()
    elif invChoicer == "inspect":
        inspectItem()
        inventoryMenu()
    elif invChoicer == "exit":
        return
    else:
        inventoryMenu()


#Menu for selecting and using consumables.
def consumableMenu():
    print(green + "< Consumable Item Menu >", reset)
    print("Type list to show your usable Consumables")
    listConsumableItems = ["list", "exit"]
    legalList = []
    for _, value in inventory.items():
        if value.isSpecifiedType("Consumable"):
            legalList.append(value)
            listConsumableItems.append(value.getItemName().lower())
    consumableChecker = checkIn(listConsumableItems, "str",
                                (cyan + "Select a Consumable to use. " + gold))
    if consumableChecker == "list":
        if len(legalList) == 0:
            print(red + "You do not have any consumables in your inventory.")
            return
        for i in legalList:
            print(blue + "[ " + str(i) + blue + " ]", reset)
        consumableMenu()
    elif consumableChecker == "exit":
        return
    else:
        consumableChecker = consumableChecker.title()
        if IDDict[consumableChecker].getItemAmount() > 0:
            for key, value in IDDict[consumableChecker].getBonusDict().items():
                try:
                    if key == "Current HP":
                        print(green + "Healed " + str(value) + " HP.", reset)
                    sub_stats[key] += value
                except:
                    stats[key] += value
            for i in IDDict[consumableChecker].getEffects():
                placeholder = i.split("|")
                i = placeholder[0]
                effectDict[i].setLevel(int(placeholder[1]))
                applyEffect(effectDict[i], None, "player")
            inventory[consumableChecker] - 1
            if inventory[consumableChecker].getItemAmount() == 0:
                inventory.pop(consumableChecker)
        else:
            print(red + "You don't have this item!", reset)
        return


#Intermediary menu for selecting the type of item to equip to, and their specific slot
def equipItems():
    print(green + "< Equip Item Menu >", reset)
    print("Type list to show your equipped items")
    equipChecker = checkIn(("head", "chest", "legs", "feet", "weapon", "neck",
                            "ring", "magic", "list", "exit"), "str",
                           (cyan + "Select a slot to equip to: " + gold))
    if equipChecker == "list":
        for key, value in equipped.items():
            if type(value) == str:
                print(blue + key + ": [ " + value + " ]", reset)
            else:
                print(
                    blue + key + ": [ " + value.equippedRepresentation() +
                    blue + " ]", reset)
    elif equipChecker == "exit":
        return
    else:
        if equipped[equipChecker.capitalize()] == "Empty":
            equipItem(equipChecker.capitalize())
            equipItems()
        else:
            print(red + "Slot occupied!", reset)
            equipItems()


#Menu for selecting the item to be equipped to that specific slot
def equipItem(itemType):
    global inventory
    global sub_stats
    listLegalItems = []
    for _, value in inventory.items():
        if value.isSpecifiedType(itemType):
            listLegalItems.append(value)
    print(green + "< " + red + itemType + " Select " + green + ">", reset)
    print("The following are equippable. Pick from the list.")
    legalNames = []
    for i in listLegalItems:
        print(blue + "[ " + str(i) + blue + " ]", reset)
        legalNames.append(i.getItemName().lower())
    legalNames.append("exit")
    userInput = checkIn(legalNames, "str",
                        (blue + "Equip which " + orange + itemType.lower() +
                         blue + "? " + gold))
    if userInput == "exit":
        return
    userInput = userInput.title()
    for key, value in IDDict[userInput].getBonusDict().items():
        try:
            sub_stats[key] += value
        except:
            stats[key] += value
    if "Item Damage" in IDDict[userInput].getBonusDict().keys():
        sub_stats["Damage-Upper"] = sub_stats["Damage-Lower"]
        sub_stats["Damage-Upper"] += sub_stats["Item Damage"]
    inventory[userInput] - 1
    if inventory[userInput].getItemAmount() == 0:
        inventory.pop(userInput)
    equipped[itemType] = IDDict[userInput]
    return


#Take an item out of its equip slot
def unequipItems():
    print(green + "< Unequip Item Menu >", reset)
    print("Type list to show your equipped items")
    equipChecker = checkIn(("head", "chest", "legs", "feet", "weapon", "neck",
                            "ring", "magic", "list", "exit"), "str",
                           (cyan + "Select a slot to unequip from: " + gold))
    if equipChecker == "list":
        for key, value in equipped.items():
            if type(value) == str:
                print(blue + key + ": [ " + value + " ]", reset)
            else:
                print(
                    blue + key + ": [ " + value.equippedRepresentation() +
                    blue + " ]", reset)
    elif equipChecker == "exit":
        return
    else:
        typeItem = equipChecker.capitalize()
        item = equipped[typeItem]
        if item != "Empty":
            try:
                inventory[item.getItemName()] + 1
            except:
                IDDict[item.getItemName()] + 1
                inventory.update(
                    {item.getItemName(): IDDict[item.getItemName()]})
            for key, value in IDDict[
                    item.getItemName()].getBonusDict().items():
                sub_stats[key] -= value
            if "Item Damage" in IDDict[
                    item.getItemName()].getBonusDict().keys():
                sub_stats["Damage-Upper"] = sub_stats["Damage-Lower"]
                sub_stats["Damage-Upper"] += sub_stats["Item Damage"]
            equipped[typeItem] = "Empty"
        else:
            print(red + "Slot already empty.")
            unequipItems()


# def inspectItem():
#     print(purple + "< - Item Inspect - >")


#Just check the file cuz I don't wanna print it out here
def help():
    print(green + "-----> Welcome to Primallux <-----")
    print(reset + "Please read about the controls in the " + blue + "README",
          reset, "file")


#Add points to stats here
def levelUp():  #Manage level-ups
    skillPoints = 0
    while True:
        if sub_stats["XP"] >= sub_stats["XP Needed"]:
            sub_stats["XP"] -= sub_stats["XP Needed"]
            skillPoints = 6
            stats["Level"] += 1
            print(green + "----------{ LEVEL UP! }----------")
            sub_stats["XP Needed"] += sub_stats["XP Next Scale Up"]
            sub_stats["XP Next Scale Up"] += round(
                (sub_stats["XP Next Scale Up"] * ((1 + 5**0.5) / 2)))
            while skillPoints > 0:
                print(blue + "You have " + green + str(skillPoints) +
                      " points to assign to stats.")
                print(blue + "(List to show current information)")
                userInput = checkIn(
                    ("list", "strength", "constitution", "dexterity",
                     "perception", "charisma", "intelligence", "wisdom", "str",
                     "con", "dex", "per", "cha", "int", "wis"), "str",
                    (blue + "What would you like to assign points to? "))
                if userInput == "list":
                    statsCheck()
                else:
                    if userInput in ("str", "con", "dex", "per", "cha", "int",
                                     "wis"):
                        userInput = {
                            "str": "strength",
                            "con": "constitution",
                            "dex": "dexterity",
                            "per": "perception",
                            "cha": "charisma",
                            "int": "intelligence",
                            "wis": "wisdom"
                        }[userInput]
                    userInput = userInput.capitalize()
                    print(blue + "Available points: " + green +
                          str(skillPoints))

                    pointsAmount = checkIn(
                        [x for x in range(skillPoints + 1)], "int",
                        (blue + "Assign how many points to " + userInput +
                         "? " + gold))
                    stats[userInput] += pointsAmount
                    skillPoints -= pointsAmount
                    sub_stats["Crit Chance"] = round(
                        (0.05 * stats["Dexterity"] *
                         (stats["Perception"]) * 0.01) + 1, 2)
                    sub_stats["Max MP"] = stats["Wisdom"] * 5
                    sub_stats["Current MP"] = sub_stats["Max MP"]
                    sub_stats["Max HP"] = stats["Constitution"] * 10
                    sub_stats["Current HP"] = sub_stats["Max HP"]
                    sub_stats["Damage-Lower"] = stats["Strength"]
                    sub_stats["Damage-Upper"] = stats["Strength"] + sub_stats[
                        "Item Damage"]
                    sub_stats["Learn Chance"] = round(
                        (stats["Intelligence"] * 0.1) *
                        (stats["Wisdom"] * 0.01) + 1, 2)
        else:
            break
    return


def elementDamage(targetType: str, element: str, user="Player") -> None:
    elementColors = {
        "Fire": orange,
    }
    if targetType == "Player":  #Assumes the target is a mob. THIS MAY BE CHANGED in the case that I add a global PVP arena.
        damageTaken = max(
            user.getElementalDamage()[element] -
            sub_stats["Element Defense"][element], 0)
        sub_stats["Current HP"] -= damageTaken
        print(red + "Taken " + elementColors[element] + str(damageTaken) +
              red + " " + element + " damage.")


#Fight system. This is going to be filled with bugs I bet.
def applyEffect(
    effect,
    mob=None,
    target="player"
) -> None:  #Applies an effect to the player or the mob (untested). The status effect affects various stats and alters them accordingly.
    effect.setTarget(target)
    if effect.getTarget() == "mob" and mob is not None:
        print(blue + "[ Applied effect to " + mob.getMobName() + blue + " ]",
              reset)
        for key, value in effect.getEffect().items():
            if effect.getEffect() == "Strength":
                mob.addDamage(value)
            elif effect.getEffect() == "Constitution":
                mob.addDefense(value)
            elif effect.getEffect() == "HP":
                mob.addHP(value)
            elif effect.getEffect() == "Dexterity":
                mob.addSpeed(value)
            elif effect.getEffect() == "Intelligence":
                mob.removeSpell()
    elif effect.getTarget() == "player":
        print(gold + "[!]" + orange + " Received effect " + str(effect) + gold + "[!]", reset)
        for key, value in effect.getEffect().items():
            if key in stats:
                stats[key] += value
            elif key == "Damage":
                sub_stats["Damage-Upper"] += value
                sub_stats["Damage-Lower"] += value
            elif key in sub_stats:
                sub_stats[key] += value
        statusEffects.update({str(effect): effect.getDuration() + turns})
        return 


def magicCasting(
    caster,
    spell,
    mob,
    defenseSuccess=False
):  #Casting magic tested and working when the mob does it. No idea if it works for player casting since that's not implemented yet.
    placeholder = spell.split("|")
    spell = spellDict[placeholder[0]]
    spell.setLevel(int(placeholder[1]))
    if caster == "enemy" and spell.getType() == "Heal":
        spell.setTarget("enemy")
    elif caster == "enemy":
        spell.setTarget("player")
    elif caster == "player" and spell.getType() == "Heal":
        spell.setTarget("player")
    else:
        spell.setTarget("enemy")

    if len(mob.getSpells()) > 0:
        if spell.getTarget() == "player" and not defenseSuccess:
            print(mob.getMobName() + " casts " +
                  spell.getCastRepresentation() + "!")
            sub_stats["Current HP"] -= spell.getDamage()
            if spell.getDamage() > 0:
                print(red + "You take " + str(spell.getDamage()) +
                      " HP worth of damage.")
            print(red + "HP: " + str(sub_stats["Current HP"]) + "/" +
                  str(sub_stats["Max HP"]))
            for i in spell.getEffects():
                if str(effectDict[i]) not in statusEffects:
                    effectDict[i].setTarget("player")
                    applyEffect(effectDict[i], mob)
        elif spell.getTarget() == "player" and defenseSuccess:
            print(mob.getMobName() + " casts " +
                  spell.getCastRepresentation() + "!")
            sub_stats["Current HP"] -= round(spell.getDamage() * 0.5)
            if round(spell.getDamage() * 0.5) > 0:
                print(red + "You take " + str(round(spell.getDamage() * 0.5)) +
                      " HP worth of damage.")
            print(red + "HP: " + str(sub_stats["Current HP"]) + "/" +
                  str(sub_stats["Max HP"]))
            for i in spell.getEffects():
                if str(effectDict[i]) not in statusEffects:
                    effectDict[i].setTarget("player")
                    applyEffect(effectDict[i], mob)
    #Reset the spell level in order to ensure that when cast again, the next effects aren't added to the stuff from before.
    spell.resetLevel()
    return


def casterMenu(
    inBattle=False
):  #Planned casting menu, with a mode for in-battle (Use spells and display CD and Costs) and out of battle (Equip/unequip runes).
    if inBattle == False:
        print(purple + "< Rune Equip Menu >")
        print(reset + "Actions: List, Equip, Unequip, Exit")
        userInput = checkIn(("list", "equip", "unequip", "exit"), "str",
                            (blue + "What will you do? " + gold))
        if userInput == "exit":
            return
    else:
        print("a")
        return
    casterMenu(inBattle=inBattle)


def enemyMove(
    mob, defendBool
):  #Enemy move in fights. Moved it out of the other function because it made that look way too long.
    meleeOrCastWeights = {
        "Warrior": 100,
        "Skirmisher": 80,
        "Fighter": 50,
        "Warmage": 40,
        "Caster": 25,
        "Mage": 10
    }
    choicer = choices(("melee", "cast"),
                      weights=(meleeOrCastWeights[mob.getMobType()],
                               100 - meleeOrCastWeights[mob.getMobType()]))[0]
    if defendBool == True and choicer == "melee":
        if choices(("full", "half"),
                   weights=(round(
                       (sub_stats["Defense"] * sub_stats["Crit Chance"] +
                        stats["Constitution"] * 0.1)),
                            mob.dealDamage())) == ["full"]:
            print(
                gold + "[!] " + green + "You completely block the " +
                mob.getMobName() + "'s attack!", reset)
            print(red + "Your HP: " + str(sub_stats["Current HP"]) + "/" +
                  str(sub_stats["Max HP"]))
            defendBool = False
        else:
            print(
                gold + "[!]" + orange +
                "You block most of the attack, but some slips through.", reset)
            sub_stats["Current HP"] -= max(
                round((mob.dealDamage() * 0.5)) - sub_stats["Defense"], 0)
            print(red + "Your HP: " + str(sub_stats["Current HP"]) + "/" +
                  str(sub_stats["Max HP"]))
            defendBool = False
    elif defendBool == True and choicer == "cast":
        if choices(("full", "half"),
                   weights=(round(
                       (sub_stats["Defense"] * sub_stats["Crit Chance"] +
                        stats["Constitution"] * 0.1)),
                            round(mob.dealDamage() * 1.5))) == ["full"]:
            print(gold + "[!] " + green + "The spell of the " +
                  mob.getMobName() + " fails to affect you!")
            print(red + "Your HP: " + str(sub_stats["Current HP"]) + "/" +
                  str(sub_stats["Max HP"]))
        else:
            print(
                gold + "[!]" +
                "The spell lands, though fails to affect you as greatly as intended."
            )
            magicCasting("enemy",
                         choice(mob.getSpells()),
                         mob,
                         defenseSuccess=True)
    elif defendBool == False and choicer == "cast":
        magicCasting("enemy", choice(mob.getSpells()), mob)
        print(red + "The spell lands a direct hit on you.")
    else:
        print(red + "You take the hit.", reset)
        print(mob.getTaunt())
        sub_stats["Current HP"] -= max(mob.dealDamage() - sub_stats["Defense"],
                                       0)
        print(red + "Your HP: " + str(sub_stats["Current HP"]) + "/" +
              str(sub_stats["Max HP"]))


def manaRegen():
    if sub_stats["Current MP"] < sub_stats["Max MP"]:
        sub_stats["Current MP"] = min(
            sub_stats["Current MP"] + (stats["Wisdom"] // 2),
            sub_stats["Max MP"])
        print(purple +
              str(sub_stats["Current MP"] + "/" + sub_stats["Max MP"]))


def monsterFight(mob, tile):
    global turns
    global statusEffects
    turns += 1
    defendBool = False
    print(red + "----------< ! FIGHT ! >----------")
    print(reset + mob.getEnterText())
    while True:
        if len(statusEffects) != 0: #For removing status effects when they expire.
            tempDict = {key: value for key, value in statusEffects.items()}
            for key, value in statusEffects.items():
                if "HP" in key:
                    DOTdamage = key.split("HP ")[1].split(" ")[0]
                    sub_stats["Current HP"] += int(DOTdamage)
                    print("You take an additional " + str(DOTdamage) + " HP worth of damage.")
                if value - turns == 0:
                    print(gold + "[!] " + blue + key + "effect has expired." +
                          gold + " [!]")
                    val = key.split(":")[0].split(" ")[:-1] #Retrieve the correct effectDict reference name.
                    effLevel = roman_to_int(key.split(":")[0].split(" ")[-1])
                    effectKey = ""
                    for i in val:
                        effectKey += i + " "
                    effectKey = effectKey[:-1]
                    effectDict[effectKey].setLevel(effLevel)

                    for key2, value2 in effectDict[effectKey].getEffect().items():
                        
                        if key2 in stats:
                            stats[key2] -= value2
                        elif key2 in sub_stats and not key2 == "Damage":
                            sub_stats[key2] -= value2
                        elif key2 == "Damage":
                            sub_stats["Damage-Lower"] -= value2
                            sub_stats["Damage-Upper"] -= value2
                    tempDict.pop(key)
    
                    sub_stats["Crit Chance"] = round(
                        (0.05 * stats["Dexterity"] *
                         (stats["Perception"]) * 0.01) + 1, 2)
                    sub_stats["Learn Chance"] = round(
                        (stats["Intelligence"] * 0.1) *
                        (stats["Wisdom"] * 0.01) + 1, 2)
                    effectDict[effectKey].resetLevel()
                else:
                    print(blue + key + "lasts for " + str(value - turns) +
                          " more turn(s).")
            statusEffects = tempDict
        
        manaRegen()
        print(reset + mob.getDuringText())
        print(green + "Valid Inputs:" + "\n")
        print(reset + "attack, fight, run, consumable, talk, defend, pacify")
        userInput = checkIn(
            ("attack", "fight", "a", "f", "run", "flee", "consumable", "c",
             "r", "talk", "t", "defend", "d", "pacify", "p"), "str",
            (reset + "What will you do? " + gold))
        if userInput == "attack" or userInput == "fight" or userInput == "a" or userInput == "f":
            print(reset + "You attack the " + red + mob.getMobName() + ".")
            if choices(
                ("hit", "miss"),
                    weights=(stats["Dexterity"], mob.getSpeed())) == ["hit"]:
                if randint(1, 101) <= sub_stats["Crit Chance"]:
                    print(gold + "< CRITICAL HIT! >", reset)
                    if sub_stats["Damage-Upper"] > sub_stats["Damage-Lower"]:
                        num = 2 * randint(sub_stats["Damage-Lower"],
                                          sub_stats["Damage-Upper"] + 1)
                    else:
                        num = 2 * randint(sub_stats["Damage-Lower"],
                                          sub_stats["Damage-Upper"] + 1)
                    mob.takeDamage(num)
                    print(orange + "Dealt " + str(num) + " damage to " +
                          mob.getMobName() + ".")
                else:
                    if sub_stats["Damage-Upper"] > sub_stats["Damage-Lower"]:
                        num = randint(sub_stats["Damage-Lower"],
                                      sub_stats["Damage-Upper"] + 1)
                    else:
                        num = randint(sub_stats["Damage-Lower"],
                                      sub_stats["Damage-Upper"] + 1)
                    mob.takeDamage(num)
                    print(orange + "Dealt " +
                          str(max((num - mob.getDefense()), 0)) +
                          " damage to " + mob.getMobName() + ".")
            else:
                print(red + "You missed.")
        elif userInput == "run" or userInput == "flee" or userInput == "r":
            if choices(("escape", "caught"),
                       weights=(stats["Dexterity"],
                                mob.getSpeed())) == ["escape"]:
                print(reset + "You have successfully escaped from " +
                      mob.getMobName())
                break
            else:
                print("You fail to run away fast enough, and the " +
                      mob.getMobName() + " catches to you.")

        elif userInput == "defend" or userInput == "d":
            defenceVar = choices(
                ("crit", "success", "fail"),
                weights=(round(sub_stats["Crit Chance"] * 0.25),
                         round(
                             (sub_stats["Defense"] +
                              stats["Constitution"] * 0.1)), mob.dealDamage()))
            if defenceVar == ["crit"]:
                print(gold + "< COUNTER! >", reset)
                num = 2 * randint(sub_stats["Damage-Lower"],
                                  sub_stats["Damage-Upper"])
                mob.takeDamage(num)
                print(orange + "Dealt " + str(num) + " damage to " +
                      mob.getMobName() + ".")
                defendBool = True
            elif defenceVar == ["success"]:
                defendBool = True
            else:
                print(red + "You fail to defend yourself properly.", reset)
        elif userInput == "pacify" or userInput == "p":
            if mob.disarm(stats, reputation):
                print(mob.getPacifyText())
                print(
                    green + "You convince the " + mob.getMobName() +
                    " not to fight!", reset)
                if mob.getFaction() != "":
                    reputation[mob.getFaction()] += mob.getPacifyBonus()
                break
            else:
                print(
                    red + "You fail to charm " + mob.getMobName() +
                    " away from fighting.", reset)
        elif userInput == "consumable" or userInput == "c":
            consumableMenu()
        elif userInput == "talk" or userInput == "t":
            if mob.getDialogue() == "":
                print("The " + mob.getMobName() + " doesn't respond.")
        print(red + str(mob))

        if mob.isDefeated():
            print(reset + mob.getExitText())
            sub_stats["XP"] += mob.getXP()
            if mob.getFaction() != "":
                reputation[mob.getFaction()] -= mob.getRepDecrease()
            print(green + "----------< You win! >----------")
            for getLoot in mob.lootGenerate():
                print(blue + "You find " + silver + str(mob.getDropSilver()) +
                      blue + " pieces of " + silver + "Ghost Silver.")
                sub_stats["Ghost Silver"] += mob.getDropSilver()
                if getLoot == "Nothing":
                    print(
                        reset +
                        "You fail to find something interesting left in the corpse"
                    )
                else:
                    print(blue + "You find a " + green + getLoot + ".")
                    try:
                        inventory[getLoot] + 1
                    except:
                        IDDict[getLoot] + 1
                        inventory.update({getLoot: IDDict[getLoot]})
            mob.resetHP()
            levelUp()
            break
        
        enemyMove(mob, defendBool)
        defendBool = False
        if sub_stats["Current HP"] <= 0:
            print(red + "!========= Game Over =========!")
            quit()

        if mob.getMobHP() <= mob.getMobFleeHP():
            print(mob.getFleeText())
            mob.resetHP()
            break
        turns += 1

    mob.resetDamage()
    mob.resetDefense()
    mob.resetSpeed()
    mob.resetSpells()
    fitDict = {
        key: value
        for key, value in questProgress.items()
        if key in questsDict and value < len(questsDict[key].getQuestChainTuple())
    }
    killQuests = [
        questsDict[key] for key, value in fitDict.items()
        if questsDict[key].getQuestChainTuple()[value - 1].getType() == "Kill"
    ]
    for i in killQuests:
        questHandler(i, "Check", mob, tile)
    return


#Actually make the adventure?????????


def dialogueManager(interaction: Interactible):
	try:
		print(interaction.getDialogue().getGreeting(turns, questProgress))
	except:
		print("This person does not appear like they wish to speak at the moment.") 
		return
	dlog = interaction.getDialogue()
	dialogueRound = 1
	previousChoice = ""
	tempDictionary = interaction.getDialogue().getFurtherDialogueDict()

	while True:
		listLegals = []
		for key in tempDictionary.keys():
			tempKey = "".join(
				list(filter(lambda a: a not in ("@", "*", "#", "`", "\\"), key)))
			if "#" in key and not interaction.getDialogue().getMetBefore():
				continue
			if "`" in key and interaction.getDialogue().getMetBefore():
				continue
			if "=" in key:
				arg = tempKey.split("=")[1].split("/")
				tempKey = tempKey.split("=")[0]
				if questProgress[arg[0]] == int(arg[1]):
					if arg[2] == "Toggle":
						print(
							f"{gold} [!] {green} Objective {str(questsDict[arg[0]].getQuestChainTuple()[questProgress[questsDict[arg[0]].getQuestName()]-1])} reached!"
						)
						questProgress[questsDict[arg[0]].getQuestName()] += 1
					elif arg[2] == "Give":
						amount = 1
						if len(arg) == 5:
							amount = int(arg[4])
						if identifierDict[arg[3]].getItemAmount() < amount:
							print(red +
								"You do not have the required amount of " +
								arg[3] + ".")
							break
						print(questsDict[arg[0]].getQuestChainTuple()[
							questProgress[questsDict[arg[0]].getQuestName()] -
							1]).getNPCDialogue()		
						identifierDict[arg[3]].getItemAmount() - amount

			if "$" in key: 
				arg = tempKey.split("$")[1].split(" ")
				arg2 = tempKey.split("$")[1][tempKey.split("$")[1].index(" ") +
											 1:]
				tempKey = tempKey.split("$")[0]
				if arg[0] == "Quest" and questProgress[arg2] == 0:
					questHandler(arg2, "Receive")
				elif arg[0] == "Currency":
					sub_stats[arg2.split(" ")[0]] += int(arg2.split(" ")[1])
				elif arg[0] == "Item":
					arg2 = arg2.split(" ")
					identifierDict[arg2[0]] + int(arg2[1])
				elif arg[0] == "Reputation":
					arg2 = arg2.split(" ")
					reputation[arg2[0]] += int(arg2[1])
				elif arg[0] == "MetBefore":
					interaction.getDialogue().setMetBefore(True)
                    

			if tempKey[tempKey.index("|") + 1] != "&":
				val = tempKey.split("|")[1].split("&")[0]
				val = val.split(" ")
				if val[0] != "Quest": #In the case that a Quest is a conditional, it does not attempt to change the quest name to an integer.
					val[2] = int(val[2])
				if val[0] == "Turns":
					if val[1] == "<" and turns >= val[2]:
						continue
					elif val[1] == "<=" and turns > val[2]:
						continue
					elif val[1] == ">" and turns <= val[2]:
						continue
					elif val[1] == ">=" and turns < val[2]:
						continue
				elif val[0] == "Reputation":
					if val[1] == "<" and turns >= val[2]:
						continue
					elif val[1] == "<=" and turns > val[2]:
						continue
					elif val[1] == ">" and turns <= val[2]:
						continue
					elif val[1] == ">=" and turns < val[2]:
						continue
				elif val[0] == "Quest":
					if questProgress[" ".join(val[1:-1])] < int(val[-1]):
						continue
				elif val[0] == "nQuest": #Flipped version of Quest. Operates similarly
					if questProgress[" ".join(val[1:-1])] > int(val[-1]):
						continue
				elif val[0] == "nMet":
					if not dlog.getMetBefore():
						continue

			if len(tempKey.split("|")) > 1 and int(
					tempKey.split("&")[1].split("^")[0].split(" ")
				[1]) == dialogueRound:
				if len(tempKey.split("|")[1].split("&")[0].split(
					"^")) > 1 and int(
						tempKey.split("|")[1].split("&")[-1].split("^")
						[1]) != previousChoice:
					continue
				print("".join(
					list(
						filter(lambda a: a not in ("@", "*", "#", "`"),
							blue + key.split("|")[0]))))
				listLegals.append(key.split(")")[0])

		userInput = checkIn(listLegals, "str",
							(cyan + "What will you say? " + gold))

		for key in tempDictionary.keys():
			if (userInput + ")") in key and key.find(userInput + ")") == 0:
				print("".join(
					list(
						filter(lambda a: a not in ("@", "*", "#", "`"),
							blue + key.split(")")[1].split("|")[0]))))
				print(reset +
					interaction.getDialogue().getOneFurtherDialogue(key))

				if "@" in key:
					dialogueRound = 1
					previousChoice = ""
				elif "*" not in key:
					dialogueRound += 1
					previousChoice = userInput
				else:
					previousChoice = ""
				break
		if userInput == "g":
			break
	print(interaction.getDialogue().getGoodbye(turns))


def haggle(haggleType: str, merchantTargetCost: int) -> int:
    userInput = checkIn(
        ("yes", "no"), "str",
        (blue + "Would you like to haggle for a new value of the item? "))
    if userInput == "no":
        return merchantTargetCost
    if haggleType == "buy":
        while True:
            try:
                userInput = int(input((blue + "Enter a new cost. " + gold)))
            except:
                print(red + "Please type a valid integer.")
                continue
            if userInput < 0:
                print(red + "Please enter a value greater than or equal to 0.")
                continue
            if choices(("accept", "does not accept"),
                       weights=(round(stats["Charisma"] / 2),
                                2 * merchantTargetCost +
                                max(0, (2 * merchantTargetCost - userInput))
                                ))[0] == "accept":
                print(green + "The merchant agrees to this new cost.")
                return userInput
            else:
                print(orange + "The merchant doesn't agree to this cost.")
                if choices(("full price", "average price"),
                           weights=(merchantTargetCost + round(
                               (merchantTargetCost + userInput) / 2),
                                    stats["Charisma"]))[0] == "average price":
                    print(
                        green +
                        "However, the merchant agrees to sell the item for a new price of "
                        + silver +
                        str(round((merchantTargetCost + userInput) / 2)) +
                        " GS.")
                    return round((merchantTargetCost + userInput) / 2)
                else:
                    print(
                        green +
                        "The merchant refuses to budge on the price of the item."
                    )
                    return merchantTargetCost
    elif haggleType == "sell":
        while True:
            try:
                userInput = int(input((blue + "Enter a new cost. " + gold)))
            except:
                print(red + "Please type a valid integer.")
                continue
            if userInput < 0:
                print(red + "Please enter a value greater than or equal to 0.")
                continue
            if choices(("accept", "does not accept"),
                       weights=(2 * merchantTargetCost +
                                max(0, (2 * merchantTargetCost - userInput)),
                                round(stats["Charisma"] / 2)))[0] == "accept":
                print(green + "The merchant agrees to this new cost.")
                return userInput
            else:
                print(orange + "The merchant doesn't agree to this cost.")
                if choices(
                    ("full price", "average price"),
                        weights=(stats["Charisma"], merchantTargetCost +
                                 round(merchantTargetCost +
                                       userInput / 2)))[0] == "average price":
                    print(
                        green +
                        "However, the merchant agrees to sell the item for a new price of "
                        + str(round(merchantTargetCost + userInput / 2)) +
                        " gold.")
                    print(round((merchantTargetCost + userInput) / 2))
                    return round((merchantTargetCost + userInput) / 2)
                else:
                    print(
                        green +
                        "The merchant refuses to budge on the price of the item."
                    )
                    return merchantTargetCost


def sellManager(variable):
    global statusEffects
    print(variable.getSellItems())
    aList = []
    for i in variable.getSellItems():
        if i in inventory.keys():
            aList.append(IDDict[i].getItemName().lower())
    aList.append("exit")
    userInput = ""
    cost = 0
    if len(aList) == 1:
        print(
            red +
            "You don't have anything that the merchant wants in your inventory."
        )
        return
    print(green + variable.getShopName() + ", " + variable.getName() +
          " is buying: ")
    while variable.checkForItemInSell(userInput.title()) == False:
        itemList = [x.title() for x in aList if x != "exit"]
        for key2 in itemList:
            print(
                str(IDDict[key2]) + blue + " Price: " + gold +
                str(variable.getItemPrice(key2)))
        userInput = checkIn(aList, "str",
                            (blue + "Pick an item to sell. " + gold))
        if userInput == "exit":
            return
        print(
            str(IDDict[userInput.title()]) + blue + " can sell for " + gold +
            str(variable.getSellItems()[userInput.title()]) + " gold.")
        cost = haggle("sell", variable.getSellItems()[userInput.title()])
    print("hi")

    print(green + "You have sold " + str(IDDict[userInput.title()]) + " for " +
          str(cost) + " gold.")
    sub_stats["Ghost Silver"] += cost
    inventory[userInput.title()] - 1
    if inventory[userInput.title()].getItemAmount() == 0:
        inventory.pop(userInput.title())


def craftingHandler(kind: str, recipes: tuple) -> None:
    print({
        "Alchemy": (green + "-----{ Alchemist's Cauldron }-----"),
        "Runation": (purple + "-----{Enchanter's Inscription Circle}-----"),
        "Smithing": (orange + "-----{Blacksmith's Forge}-----"),
		"Tailoring": (light_purple + "-----{Tailor's Loom}-----")
    }[kind])  #Print decoration separator

    for i in recipes:
        print(blue + str(recipes.index(i) + 1) + ") " +
              str(i))  #Print possible crafts
        tempList = [i for i in range(0, len(recipes) + 1)]
    userInput = checkIn(
        tempList, "int",
        (blue + "Select an item to craft (input its index number): " +
         gold))  #Select a recipe to craft from in the list
    if userInput == 0:
        return
    craftingRecipe = recipes[userInput - 1]

    if craftingRecipe.getCraftingType() not in skillLevels.keys():
        skillLevels.update({craftingRecipe.getCraftingType(): 0})
    if craftingRecipe.isPossibleCraft(
            stats, skillLevels
    ):  #Checks if the recipe is possible with your current items and levels.

        print("You have crafted " +
              craftingRecipe.getOutputItemRepresentation() + ".")
        try:
            inventory[craftingRecipe.getOutputItem(
            )] + craftingRecipe.getOutputAmount()
        except:
            IDDict[craftingRecipe.getOutputItem(
            )] + craftingRecipe.getOutputAmount()
            inventory.update({
                craftingRecipe.getOutputItem():
                IDDict[craftingRecipe.getOutputItem()]
            })
        for key, value in craftingRecipe.getItemsRequired().items():
            inventory[key] - value
            if inventory[key].getItemAmount() == 0:
                inventory.pop(key)
        return
    else:
        return


def questHall():
    global tile

    QHNames = {21: "Moonreach Quest Hall"}
    print(orange + " -----{ " + QHNames[tile] + " }----- ")
    action = checkIn(("take", "complete", "exit"), "str", (
        f"{blue} {underline}Take{reset} {blue}a quest, {underline}Complete{reset} {blue}a quest, or exit."
    ))

    questHallDict = {21: moonreachQuests}
    if action == "take":
        randomQuestList = questHallDict[tile]  #sample(questHallDict[tile], 3)
        for i in range(len(randomQuestList)):
            print(
                f"{bold} {blue} {str(i + 1)} : {reset} {str(questsDict[randomQuestList[i]])}"
            )
        val = checkIn(
            ["1", "2", "3", "exit"], "str",
            (reset + "Select which quest of the above?  ('exit' to leave)" +
             gold))
        if val == "exit":
            return
        else:
            val = int(val)
            questHandler(questsDict[randomQuestList[val - 1]], "Receive")
    elif action == "complete":
        completableQuests = [
            i for i in questHallDict[tile]
            if questProgress[i] >= len(questsDict[i].getQuestChainTuple())
        ]
        if len(completableQuests) == 0:
            print(red + "You have no quests to hand into this " + orange +
                  "Guild Hall" + red + ".")
            return
        else:
            for i in completableQuests:
                print(bold + blue + i)
            val = checkIn(
                [i.lower() for i in completableQuests], "str",
                (blue + "Please select a quest to complete. " + gold))
            questHandler(questsDict[properTitle(val)], "Finish")
            return
    elif action == "exit":
        return


def interactionManager(kind, accessTileID):
    variable = interactionDict[accessTileID]
    print(variable.getInteractText(), reset)
    if kind == "Merchant":
        listLegals = []
        merchDict = {}
        for i in variable.getMerchants():
            print(str(i))
            listLegals.append(i.getName().lower())
            listLegals.append(i.getShopName().lower())
            merchDict.update({i.getName().lower(): i})
            merchDict.update({i.getShopName().lower(): i})
            listLegals.append((i.getShopName() + ", " + i.getName()).lower())
            merchDict.update({
                (i.getShopName() + ", " + i.getName()).lower(): i
            })
        print(blue + "Exit")
        listLegals.append("exit")
        userInput = checkIn(
            listLegals,
            "str",
            message=(blue + "Choose an establishment to go to. " + gold))

        if userInput == "exit":
            return
        else:
            variable = merchDict[userInput]
        print(variable.getFlavorText())
        print(str(variable))
        userInput = checkIn(("buy", "talk", "exit"), "str",
                            (blue + "Buy, talk, or exit the shop. " + gold))
        if userInput == "buy":
            print(green + variable.getShopName() + ", " + variable.getName() +
                  " is selling: ")
            variable.printBuyItems()
            listLegals = []
            for i in variable.getBuyDict().keys():
                listLegals.append(IDDict[i].getItemName().lower())
            listLegals.append("exit")
            userInput = ""
            cost = 0
            while variable.checkForItemInBuy(userInput.title()) == False:
                userInput = checkIn(listLegals, "str",
                                    (blue + "Pick an item to buy. " + gold))
                if userInput == "exit":
                    return
                print(reset + str(IDDict[userInput.title()]) + blue +
                      " costs " + silver +
                      str(variable.getShopItems()[userInput.title()]) + " GS.")
                cost = haggle("buy",
                              variable.getShopItems()[userInput.title()])
                if sub_stats["Ghost Silver"] < cost:
                    print(red + "You don't have the money to buy this item.",
                          reset)
                    userInput = ""
            #haggling?
            if checkIn(("yes", "no"), "str",
                       (blue + "You currently have " + silver +
                        str(sub_stats["Ghost Silver"]) + "GS.\n" +
                        "Do you accept this price? " + gold)) == "no":
                print(blue + "You refuse the offer.")
                return
            print(green + "You have bought " + str(IDDict[userInput.title()]) +
                  " for " + silver + str(cost) + " GS.")
            sub_stats["Ghost Silver"] -= cost
            try:
                inventory[userInput.title()] + 1
            except:
                IDDict[userInput.title()] + 1
                inventory.update(
                    {userInput.title(): IDDict[userInput.title()]})
            return
        elif userInput == "sell":
            sellManager(variable)
            tileManager(accessTileID, flag=True)
        elif userInput == "talk":
            dialogueManager(variable)

        elif userInput == "exit":
            return
    elif kind == "Crafting":
        craftingHandler(variable.getCraftingType(), [
            i for i in recipeDict.values()
            if i.getCraftingType() == variable.getCraftingType()
        ])
        tileManager(accessTileID, True)
    #elif kind == "Merchant|Crafting"
    elif kind == "Dungeon Entrance":  #In the case of it being a dungeon entrance, it directs you to the tile-manager for the tile on the other side of the entrance.
        tileManager(variable.getToTileID())
    elif kind == "Resource":  #Runs some lil function to test if you get the resource or not, and upon success, adds it to the inventory.
        resourceList = variable.getLoot(
            round(stats["Strength"] * 0.05 + stats["Perception"] * 0.05) +
            skillLevels[variable.getGatherMod()])
        for i in resourceList:
            if i == "Nothing":
                resourceList.remove(i)
        if len(resourceList) == 0:
            print(
                blue +
                "You fail to extract any resources from this area.")
        else:
            for i in resourceList:
                lis = i.split("|")
                print(blue + "You gather some " + IDDict[lis[0]].getColor() +
                      IDDict[lis[0]].getItemName() + ".")
                skillLevels[lis[1]] += int(lis[2])
                try:
                    inventory[lis[0]] + 1
                except:
                    IDDict[lis[0]] + 1
                    inventory.update({lis[0]: IDDict[lis[0]]})
        return
    elif kind == "Dialogue":  #Talk to NPCs
        dialogueManager(variable)
    elif kind == "Multi-Dialogue": #In order to fit multiple dialogue NPCs into the same tile, multiple Interactibles need to be initialized and then filled into the base Interactible object. Note: Store dialogues as {"NPC Name":Interactible}.
        print("People in this area: ")
        for key in variable.getDialogueLink().keys():
            print(f"{green}{key}")
        speakTo = checkIn(list(variable.getDialogueLink().keys()), "str", message=f"{blue}Who to talk to? {gold}")
        print(f"{blue} You speak to {green}{speakTo}.")
        dialogueManager(variable.getDialogueLink()[speakTo])
        return
    elif kind == "Quest Hall":
        questHall()


def tileManager(
        number,
        flag=False):  #Function for running to streamline tile creation.
    global turns, tile, statusEffects
    tile = number
    turns += 1

    signalFlag = False
    variable = tilesDict[number]
    variable.resetNothing(
    )  #Resets the "Nothing" statements for loot and stuff so it actually works rather than being infinitely subtracted by the modifiers.
    if variable.getReferenceName() in tileRespawn:
        if tileRespawn[variable.getReferenceName()] <= turns:
            try:
                mobList[variable.getReferenceName()] = defaultMobList[
                    variable.getReferenceName()]
            except KeyError:
                pass
            try:
                tileItems[variable.getReferenceName()] = defaultTileItems[
                    variable.getReferenceName()]
            except KeyError:
                pass

            tileRespawn.pop(variable.getReferenceName())
    if not flag:
        replit.clear()
    if variable.getStatModifiers(
    ) != {}:  #Modifies stats accordingly to the environmental conditions specified by the tile.
        mods = variable.getStatModifiers()
        for key, value in mods.items():
            stats[key] += value
    if len(statusEffects) != 0:
        tempDict = {key: value for key, value in statusEffects.items()}
        for key, value in statusEffects.items():
            if value - turns == 0:
                print(gold + "[!] " + blue + key + "effect has expired." +
                      gold + " [!]")
                val = key.split(":")[0].split(" ")[:-1] #Retrieve the correct effectDict reference name.
                effLevel = roman_to_int(key.split(":")[0].split(" ")[-1])
                effectKey = ""
                for i in val:
                    effectKey += i + " "
                effectKey = effectKey[:-1]
                effectDict[effectKey].setLevel(effLevel)

                for key2, value2 in effectDict[effectKey].getEffect().items():
                    
                    if key2 in stats:
                        stats[key2] -= value2
                    elif key2 in sub_stats and not key2 == "Damage":
                        sub_stats[key2] -= value2
                    elif key2 == "Damage":
                        sub_stats["Damage-Lower"] -= value2
                        sub_stats["Damage-Upper"] -= value2
                tempDict.pop(key)

                sub_stats["Crit Chance"] = round(
                    (0.05 * stats["Dexterity"] *
                     (stats["Perception"]) * 0.01) + 1, 2)
                sub_stats["Learn Chance"] = round(
                    (stats["Intelligence"] * 0.1) *
                    (stats["Wisdom"] * 0.01) + 1, 2)
                effectDict[effectKey].resetLevel()
            else:
                print(blue + key + "lasts for " + str(value - turns) +
                      " more turn(s).")
        statusEffects = tempDict

    if variable.getLootTable(
    ) != {}:  #Modifies the loot table's "Nothing" condition to make Perception have an impact on loot finding.
        variable.setLootTableModifier(stats["Perception"])
        if variable.getLootTable()["Nothing"] < 0:
            variable.getLootTable()["Nothing"] = 0

    if variable.getQuestFlavorText(
            questProgress
    ) == "":  #Replace usual flavor text with quest text, if at that stage.
        print(variable.getFlavorText())
    else:
        print(variable.getQuestFlavorText(questProgress))

    if variable.getQuestEntryEncounter() and variable.isQuestEncounter(
            questProgress
    ):  #Test if there is a quest encounter at this tile and quest stage. If there is, it will proceed by playing out the encounter.
        monster, val = variable.getQuestEncounter(questProgress)
        if type(monster) == list or type(monster) == tuple: #Randomly select a monster from the questEncounters list at that quest stage.
            monster = choice(monster)
        monsterFight(monster, number)
        variable.questEncounterWin(val)
    if type(variable.getEncounter()
            ) == tuple and mobList[variable.getReferenceName()] > 0:
        pickedMob = choice(variable.getEncounter())
        monsterFight(pickedMob, number)
    if type(variable.getEncounter()) != bool and variable.getEncounter(
    ).getFaction() != "":  #In the case that the mob has a faction.
        try:  #It'll try and test if there's a mob here that's specified to be able to enter a battle upon entry.
            if variable.encounterOnEnter(mobList[variable.getReferenceName(
            )]) and reputation[variable.getEncounter().getFaction(
            )] <= variable.getEncounter().getEncounterThreshold():
                monsterFight(variable.getEncounter(), number)
            elif reputation[variable.getEncounter().getFaction(
            )] > variable.getEncounter().getEncounterThreshold(
            ):  #If you're liked by the mob's faction, it won't fight you.
                print(reset + variable.getNoRepText())
        except KeyError:
            print("Nothing is here to challenge you.")
        except AttributeError:
            print("Nothing is here to challenge you.")

    else:
        try:
            if variable.encounterOnEnter(mobList[variable.getReferenceName()]):
                monsterFight(variable.getEncounter(), number)
        except KeyError:
            print("Nothing is here to challenge you.")
        except AttributeError:
            print("Nothing is here to challenge you.")

    manaRegen()

    fitDict = {
        key: value
        for key, value in questProgress.items()
        if key in questsDict and value < len(questsDict[key].getQuestChainTuple())
    }
    enterQuests = [
        questsDict[key] for key, value in fitDict.items()
        if questsDict[key].getQuestChainTuple()[value - 1].getType() == "Scout"
        or questsDict[key].getQuestChainTuple()[value - 1].getType() == "Go"
    ]

    for i in enterQuests:
        questHandler(i, "Check", tileNum=number)
    showTilePossibleInputs(number)
    userInput = checkIn(tilesetLegals, "str", "What will you do? " +
                        gold)  #User inputs for the tile itself.
    if userInput == "wander":  #Selects a random direction to go in, and sends you in that direction.
        userInput = sample(("n", "s", "e", "w"), 1)[0]
    if userInput in ("n", "s", "e", "w"):
        userInput = {
            "n": "north",
            "s": "south",
            "e": "east",
            "w": "west"
        }[userInput]

    if userInput == "search" or userInput == "look" or userInput == "l":  #When the player searches, they run a huge function to test if they find loot or not, and/or find a monster. Also leaves some nice text.
        if variable.isQuestEncounter(questProgress):
            replit.clear()
            if type(variable.getQuestEncounter(questProgress)) != bool:
                monster, val = variable.getQuestEncounter(questProgress)
                monsterFight(monster, number)
                variable.questEncounterWin(val)
        if type(variable.getEncounter()) != bool and variable.getEncounter(
        ).getFaction() != "":
            replit.clear()
            if variable.getReferenceName() in mobList.keys():
                if variable.encounterTest(
                        mobList[variable.getReferenceName()],
                        reputation[variable.getEncounter().getFaction()]):
                    monsterFight(variable.getEncounter(), number)
                    mobList[variable.getReferenceName()] -= 1
                elif mobList[variable.getReferenceName()] == 0:
                    print(variable.getNoMoreMobsText())
                else:
                    print(reset + variable.getNoFindText())
            else:
                print(
                    blue +
                    "You don't find anything that presents a suitable challenge.",
                    reset)  #When there's no mob in the tile.
        elif type(variable.getEncounter()) != bool:
            try:
                if variable.encounterTest(
                        mobList[variable.getReferenceName()]):
                    monsterFight(variable.getEncounter(), number)
                    mobList[variable.getReferenceName()] -= 1
                elif mobList[variable.getReferenceName()] == 0:
                    print(variable.getNoMoreMobsText())
                else:
                    print(reset + variable.getNoFindText())
            except KeyError:
                print(
                    blue +
                    "You don't find anything that presents a suitable challenge.",
                    reset)  #When there's no mob in the tile.

        if (variable.getReferenceName()
                in mobList.keys()) and (mobList[variable.getReferenceName()]
                                        == 0) and (variable.getReferenceName()
                                                   not in tileRespawn.keys()):
            tileRespawn.update({
                variable.getReferenceName():
                turns + defaultTileRespawns[variable.getReferenceName()]
            })
        if variable.getQuestSearchText(questProgress) == "":
            print(variable.getSearchText())
        else:
            print(variable.getQuestSearchText(questProgress))

        if variable.getReferenceName() in tileItems and tileItems[
                variable.getReferenceName()] == 0:
            print(red + "There's nothing left of interest here."
                  )  #When there aren't any more items left in the tile.
        elif variable.getReferenceName(
        ) in tileItems and tileItems[variable.getReferenceName(
        )] > 0 and variable.getLootTable() != {}:
            loot = variable.getLoot()
            lootList = list(
                filter(("Nothing").__ne__, loot)
            )  #Filters out "Nothing" variable to avoid that being appended to the inventory.

            if lootList != []:
                for i in lootList:
                    tileItems[variable.getReferenceName()] -= 1
                    if tileItems[variable.getReferenceName()] == 0 and (
                            variable.getReferenceName()
                            not in tileRespawn.keys()):
                        tileRespawn.update({
                            variable.getReferenceName():
                            turns +
                            defaultTileRespawns[variable.getReferenceName()]
                        })
                    print("You find a " + IDDict[i].getColor() +
                          IDDict[i].getItemName())
                    if IDDict[i].getItemName() in inventory:
                        inventory[i] + 1
                    else:
                        IDDict[i] + 1
                        inventory[i] = IDDict[
                            i]  #Adds the item to the inventory
                        #inventory.update({i:IDDict[i]})
            else:
                print(red + "You don't find anything."
                      )  #States that you can't find the item.
        if variable.getStatModifiers(
        ) != {}:  #Should be modifying stats based on what you find, albeit temporarily.
            mods = variable.getStatModifiers()
            for key, value in mods.items:
                if value < 0:
                    print(red + key + "-" + value, reset)
                else:
                    print(green + key + "+" + value, reset)
        tileManager(number, flag=True)
    elif userInput == "stats":  #Checks your stats in-game.
        statsCheck()
        tileManager(number, flag=True)
    elif userInput == "skills":
        skillsCheck()
        tileManager(number, flag=True)
    elif userInput == "quests":
        questMenu()
        tileManager(number, flag=True)
    elif userInput == "help" or userInput == "h":  #Displays the lackluster help page.
        help()
        tileManager(number, flag=True)
    elif userInput == "inv" or userInput == "inventory":  #Accesses the inventory menu.
        inventoryMenu()
        tileManager(number, flag=True)
    elif userInput == "int" or userInput == "interact":  #Provides access to tile-specific interactions.
        signalFlag = False
        if variable.getInteractible() == "Random":
            variable.randomSetInteractible(30)
            signalFlag = True
        if variable.getInteractible() and not (variable.getReferenceName()
                                               in killedNPCs):
            interactionManager(interactionDict[tile].getType(), tile)
        else:
            print("There's nothing to interact with here.")
        if (signalFlag):
            variable.resetInteractible()
        tileManager(number, flag=True)
    elif userInput == "save":  #Saves your data.
        save()
        tileManager(number, flag=True)
    elif userInput == "up" or userInput == "down":  #The user can go up or down in the tile, provided they succeed the Dexterity check.
        if variable.getClimbable():
            if userInput == "up" and variable.checkClimb(
                    stats["Dexterity"]) and variable.getUpTile() != 0:
                print(variable.getClimbText())
                if variable.getStatModifiers() != {}:
                    mods = variable.getStatModifiers()
                    for key, value in mods.items():
                        stats[key] -= value
                tileManager(variable.getUpTile())
            elif userInput == "down" and variable.checkClimb(
                    stats["Dexterity"]) and variable.getDownTile() != 0:
                print(variable.getClimbText())
                if variable.getStatModifiers() != {}:
                    mods = variable.getStatModifiers()
                    for key, value in mods.items():
                        stats[key] -= value
                tileManager(variable.getDownTile())
            else:  #Enacts a punishment on failing by cutting your HP
                print(variable.climbFailText())
                sub_stats["Current HP"] -= variable.climbFailDamage()
                print(blue + "You take " + str(variable.climbFailDamage()) +
                      " damage from falling down.\n" + red + "HP: " +
                      str(sub_stats["Current HP"]) + "/" +
                      str(sub_stats["Max HP"]))
                if sub_stats["Current HP"] <= 0:
                    print(red + "!========= Game Over =========!")
                    quit()
        else:
            print(
                blue + "You see nothing to climb here.", reset
            )  #Stops the player from climbing everywhere in places that make no sense.
        tileManager(number, flag=True)
    else:
        if userInput.capitalize() in variable.getNearbyTiles():
            if variable.getStatModifiers(
            ) != {}:  #Removes all the stat modifiers that were incurred previously.
                mods = variable.getStatModifiers()
                for key, value in mods.items():
                    stats[key] -= value
            tileManager(variable.getNearbyTiles()[userInput.capitalize()])
        else:
            print(variable.getTileNotFound())
            tileManager(number, flag=True)
    tileManager(tile)


def questMenu():
    ph = False
    for key, value in questProgress.items():
        if value == 0:
            continue
        print(str(questsDict[key]))
        print(blue + "----<[Objective]>----\n" +
              str(questsDict[key].getQuestChainTuple()[value - 1]) + "\n")
        ph = True
    if not ph:
        print(red + "You have not accepted any quests.")


def questHandler(quest: Quest, action: str, inp="", tileNum=0):
    if action == "Receive":
        if quest.getNeededReputation()[0] != None:
            if quest.getNeededReputation()[1] <= reputation[
                    quest.getNeededReputation()[0]]:
                questProgress[quest.getQuestName()] += 1
                print(green + "-----{Received Quest: " + quest.getQuestName() +
                      "}-----")
                print(quest.getIntroText())
            else:
                print(
                    red +
                    "Your standing is not high enough with this faction to accept this quest."
                )
        else:
            questProgress[quest.getQuestName()] += 1
            print(green + "-----{Received Quest: " + quest.getQuestName() +
                  "}-----")
            print(quest.getIntroText())

    elif action == "Check":
        if questProgress[quest.getQuestName()] - 1 == -1 or questProgress[
                quest.getQuestName()] - 1 >= len(quest.getQuestChainTuple()):
            return
        questObj = quest.getQuestChainTuple()[
            questProgress[quest.getQuestName()] - 1]
        if questObj.getType() == "Kill":
            if inp == questObj.getMob():
                questObj.incrementAmount()
                if questObj.getCurrentAmount() >= questObj.getAmount():
                    print(
                        f"{gold} [!] {green} Objective {str(questObj)} reached!"
                    )
                    questProgress[quest.getQuestName()] += 1
        elif questObj.getType() == "Gather":
            if inp == questObj.getItem():
                questObj.incrementAmount()
                if questObj.getCurrentAmount() >= questObj.getAmount():
                    print(
                        f"{gold} [!] {green} Objective {str(questObj)} reached!"
                    )
                    questProgress[quest.getQuestName()] += 1
        elif questObj.getType() == "Go" or questObj.getType() == "Scout":
            if tileNum in questObj.getLocation():
                print(f"{gold} [!] {green} Objective {str(questObj)} reached!")
                questProgress[quest.getQuestName()] += 1
        elif questObj.getType() == "Clear":
            if tilesDict[tileNum].getAmountEncounters() <= 0:
                print(f"{gold} [!] {green} Objective {str(questObj)} reached!")
                questProgress[quest.getQuestName()] += 1
    elif action == "Finish":
        print(gold + "[!] " + green + "Quest Finished " + gold + "[!]")
        rewards = quest.getReward()
        for key, value in rewards.items():
            if key == "Ghost Silver":
                print(silver + "Ghost Silver +" + str(value))
                sub_stats["Ghost Silver"] += value
            elif key == "XP":
                print(green + "XP +" + str(value))
                sub_stats["XP"] += value
                levelUp()
            else:
                print(IDDict[key].getColor() + IDDict[key].getItemName() +
                      " +" + str(value))
                try:
                    inventory[key] + value
                except KeyError:
                    IDDict[key] + value
                    inventory[key] = IDDict[key]


def newGame():
    global name, race, gender, tile, stats, sub_stats, equipped, inventory, questProgress, tileItems, mobList, reputation, turns, statusEffects, metNPCs, killedNPCs, tileRespawn, skillLevels
    tile = 1
    name = ""
    race = ""
    gender = ""
    turns = 0

    stats = {
        "Level": 1,
        "Strength": 10,
        "Constitution": 10,
        "Dexterity": 10,
        "Agility": 10,
        "Perception": 10,
        "Charisma": 10,
        "Intelligence": 10,
        "Wisdom": 10
    }  #Main stats that're actually displayed.

    sub_stats = {
        "Max HP": 100,
        "Current HP": 100,
        "Max MP": 50,
        "Current MP": 50,
        "Item Damage": 0,
        "Crit Chance": 0.0,
        "Learn Chance": 0.0,
        "Damage-Upper": 0,
        "Damage-Lower": 0,
        "Defense": 0,
        "Ghost Silver": 0,
        "XP": 0,
        "XP Needed": 10,
        "XP Next Scale Up": 10,
        "Element Damage": {
            "Fire": 0,
            "Water": 0,
            "Earth": 0,
            "Air": 0,
            "Light": 0,
            "Dark": 0,
            "Mind": 0,
            "Wood": 0,
            "Metal": 0,
            "Sun": 0,
            "Moon": 0,
            "Star": 0
        },
        "Element Defense": {
            "Fire": 0,
            "Water": 0,
            "Earth": 0,
            "Air": 0,
            "Light": 0,
            "Dark": 0,
            "Mind": 0,
            "Wood": 0,
            "Metal": 0,
            "Sun": 0,
            "Moon": 0,
            "Star": 0
        }
    }  #Stats that are dependent upon the stats read by the stats function, or are those not represented entirely as stats in the in-game stats checker.

    questProgress = defaultQuests #Dictionary for storing quest progression based on stages! Get quests from NPCs.

    reputation = defaultRep  #Reputation system for NPC convo buffs, quests, Sparing system, etc
    skillLevels = {
        "Fishing": 0,
        "Herbalism": 0,
        "Hunting": 0,
        "Mining": 0,
        "Salvaging": 0,
        "Alchemy": 0,
        "Cooking": 0,
        "Smithing": 0,
        "Jeweling": 0,
        "Runation": 0,
        "Tailoring": 0,
        "Tinkering": 0
    }  #Skills for resource gathering and crafting.

    tileItems = {key: value for key, value in defaultTileItems.items()}

    mobList = {key: value for key, value in defaultMobList.items()}

    inventory = {}  #Stores your held items, those that aren't equipped.

    statusEffects = {}

    tileRespawn = {}  #Locally stores the respawn timers for items and mobs.

    metNPCs = [] #Stores NPCs the player has gained a metBefore status with.

    killedNPCs = {} #Stores dead NPCs.

    equipped = {
        "Head": "Empty",
        "Chest": "Empty",
        "Legs": "Empty",
        "Feet": "Empty",
        "Weapon": "Empty",
        "Neck": "Empty",
        "Ring": "Empty",
        "Magic": "Empty"
    }  #Slots for items.
    statAssign()
    tileManager(1)


def registerAccount():
    registry = checkIn(("yes", "no"), "str",
                       "Register a new Primallux account? " + gold)
    try:
        if registry == "yes":
            usn = input(cyan + "Enter a username to register to. " + gold)
            if usn in db.keys():
                print(red + "This username is already in use.")
                registerAccount()
            else:
                password = input(cyan + "Enter a password. " + gold)
                confPassword = input(cyan + "Enter your password again. " +
                                     gold)
                if password != confPassword:
                    print(red + "Passwords do not match.")
                    registerAccount()
                else:
                    db[usn] = {"PWD": password, "Data": {}}
                    print(
                        blue + "Primallux Account created!\n" + gold + "[!] " +
                        green +
                        "Remember to write down your username and password somewhere, or you won't be getting them back!"
                    )
                    input(blue + "Press [ENTER] to continue.")
                    replit.clear()
                    newGame()
                    return False, usn
        elif registry == "no":
            try:
                usn = input(reset + "Username: " + gold)
                pwd = input(reset + "Password: " + gold)
                if db[usn]["PWD"] == pwd:
                    replit.clear()
                    return True, usn
                else:
                    replit.clear()
                    print(red + "Password and Username do not match.")
                    return registerAccount()
            except KeyError:
                replit.clear()
                print(red + "This account is not registered.")
                return registerAccount()
    except AttributeError as e:
        print(e)


def __main__(): #Start Here
    global name, race, gender, tile, stats, sub_stats, equipped, inventory, questProgress, tileItems, mobList, reputation, turns, statusEffects, metNPCs, killedNPCs, skillLevels, tileRespawn, username

    n, usn = registerAccount()
    if n:
        global record
        record = db[usn]["Data"]
        if len(record) > 0:
            print(blue + "You have a file on record.")
            userInput = checkIn(
                ("yes", "no"), "str",
                "Would you like to load it? " + gold + "(yes/no) ")
            if userInput == "yes": #Loads data
                turns = record["Turns"]
                name = record["Name"]
                race = record["Race"]
                gender = record["Gender"]
                tile = int(record["Tile"])
                stats = dict(record["Stats"])
                sub_stats = dict(record["Sub Stats"])
                sub_stats["Element Damage"] = dict(sub_stats["Element Damage"])
                sub_stats["Element Defense"] = dict(
                    sub_stats["Element Defense"])
                tileItems = dict(record["Tile Items"])
                questProgress = dict(record["Quest Progress"])
                for key, value in defaultQuests.items():
                    if key not in questProgress:
                        questProgress[key] = value
                reputation = dict(record["Reputation"])
                for key, value in defaultRep.items():
                    if key not in reputation:
                        reputation[key] = value
                mobList = dict(record["Mob List"])
                skillLevels = dict(record["Skill Levels"])
                enterDict = {}
                placeholder = record["Equipped"]
                metNPCs = list(record["Met NPCs"])
                for i in metNPCs:
                    dialogueDict[i].setMetBefore(True)
                killedNPCs = dict(record["Killed NPCs"])
				
                for key, value in placeholder.items():
                    if value != "Empty":
                        loadList = value.split("|")
                        IDDict[loadList[0]] + int(loadList[1])
                        enterDict.update({key: IDDict[loadList[0]]})
                    else:
                        enterDict.update({key: value})
                equipped = enterDict
                enterDict = {}
                placeholder = record["Inventory"]
                inventory = {}
                for key, value in placeholder.items():
                    loadList = value.split("|")
                    IDDict[loadList[0]] + int(loadList[1])
                    enterDict.update({key: IDDict[key]})
                inventory.update(enterDict)
                statusEffects = {}
                placeholder = record["Status Effects"]
                for key, value in placeholder.items():
                    loadList = key.split("|")
                    effectDict[loadList[0]].setLevel(loadList[1])
                    statusEffects.update({str(effectDict[loadList[0]]): value})
                tileRespawn = dict(record["Tile Respawn"])
                placeholder = {
                    key: value
                    for key, value in defaultTileItems.items()
                    if key not in tileItems
                }
                for key, value in placeholder.items():
                    tileItems.update({key: value}) #Adds fields to tileItems if there is a new update after player has created a saved character.
                placeholder = {
                    key: value
                    for key, value in defaultMobList.items()
                    if key not in mobList
                }
                for key, value in placeholder.items():
                    mobList.update({key: value}) #Adds fields to moblist if there is a new update after player has created a saved character.
                replit.clear()
                print(green + "Data Loaded!")

                tileManager(tile)
            else:
                db[usn]["Data"] = {}
                newGame()
        else:
            newGame()


#yes, this code is this long. you made it to the end, good for you.

if __name__ == "__main__":
    __main__()
