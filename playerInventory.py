from ansi.colour.rgb import rgb256
from ansi.color.fx import reset
from random import randint
from magic import effectDict
import copy

black = "\u001b[30m"
red = "\u001b[31m"
green = rgb256(0x00, 0xff, 0x09)
yellow = "\u001b[93m"
orange = rgb256(0xff, 0x73, 0x00)
gold = rgb256(0xe6, 0xcb, 0x02)
blue = "\u001b[34m"
lime = rgb256(0xa2, 0xff, 0x00)
magenta = "\u001b[95m"
cyan = rgb256(0x61, 0xff, 0xf4)
purple = rgb256(0xbe, 0x03, 0xfc)
white = "\u001b[37m"
bold = "\u001b[1m"
underline = "\u001b[4m"
italic = "\u001b[3m"
colorsForTypes = {
    "Consumable": green,
    "Ward": lime,
    "Magic": purple,
    "Weapon": red,
    "Head": cyan,
    "Chest": cyan,
    "Legs": cyan,
    "Feet": cyan,
    "Ring": magenta,
    "Amulet": magenta,
    "Misc": orange
}


class InvItem(object):
    def __init__(self, itemType:str, itemName:str, amount:int):
        self.typeColor = colorsForTypes[itemType]
        self.itemType = itemType
        self.itemName = itemName
        self.amount = amount

    def __repr__(self):
        return self.typeColor + self.itemName + cyan + ": " + str(self.amount)

    def __add__(self, addedAmount):
        self.amount += addedAmount

    def __sub__(self, subtractedAmount):
        self.amount -= subtractedAmount

    def __eq__(self, other):
        if type(other) != InvItem or type(other) != EquipmentItem or type(
                other) != ConsumableItem:
            return False
        else:
            return self.itemType == other.itemType and self.itemName == other.itemName

    def isSpecifiedType(self, nameOfType):
        if self.itemType == nameOfType:
            return True
        else:
            return False

    def getItemName(self):
        return self.itemName

    def getColoredName(self):
        return self.typeColor + self.itemName

    def getItemType(self):
        return self.itemType

    def getItemAmount(self):
        return self.amount

    def getColor(self):
        return self.typeColor

    def setItemAmount(self, amount):
        self.amount = amount

    def dumpSaveRepresentation(self):
        return self.itemName + "|" + str(self.amount)


class ConsumableItem(InvItem):
    def __init__(self, itemName:str, amount:int, bonuses:dict, effects=()):
        self.typeColor = green
        self.itemType = "Consumable"
        self.itemName = itemName
        self.amount = amount
        self.bonuses = bonuses
        self.effects = effects

    def __repr__(self):
        appendedString = " "
        counter = len(self.bonuses.items())
        for key, value in self.bonuses.items():
            counter -= 1
            color = green
            if value < 0:
                color = red
            if counter != 0:
                appendedString += appendedString + color + key + " " + str(
                    value) + ", "
            else:
                appendedString += appendedString + color + key + " " + str(
                    value)
        return self.typeColor + self.itemName + cyan + ": " + str(
            self.amount) + appendedString

    def __str__(self):
        appendedString = " "
        counter = len(self.bonuses.items())
        for key, value in self.bonuses.items():
            counter -= 1
            color = green
            if value < 0:
                color = red
            if counter != 0:
                appendedString += appendedString + color + key + " " + str(
                    value) + ", "
            else:
                appendedString += appendedString + color + key + " " + str(
                    value)
            if len(self.effects) != 0:
                for i in self.effects:
                    eff = copy.copy(effectDict[i.split("|")[0]])
                    eff.setLevel(int(i.split("|")[1]))
                    appendedString += ", " + str(eff)
        return self.typeColor + self.itemName + cyan + ": " + str(
            self.amount) + appendedString

    def getBonusDict(self):
        return self.bonuses

    def getEffects(self):
        return self.effects


class EquipmentItem(InvItem):
    #Input bonuses parameter as a dictionary with keys as the bonus name, and values as buffs or debuffs.
    def __init__(self, itemType:str, itemName:str, amount:int, bonuses:dict):
        self.typeColor = colorsForTypes[itemType]
        self.itemType = itemType
        self.itemName = itemName
        self.amount = amount
        self.bonuses = bonuses

    def __repr__(self):
        appendedString = " "
        counter = len(self.bonuses.items())
        for key, value in self.bonuses.items():
            counter -= 1
            color = green
            if value < 0:
                color = red
            if counter != 0:
                appendedString += appendedString + color + key + " " + str(
                    value) + ", "
            else:
                appendedString += appendedString + color + key + " " + str(
                    value)
        return self.typeColor + self.itemName + cyan + ": " + str(
            self.amount) + appendedString

    def __str__(self):
        appendedString = " "
        counter = len(self.bonuses)
        for key, value in self.bonuses.items():
            counter -= 1
            color = green
            if value < 0:
                color = red
            if counter != 0:
                appendedString += appendedString + color + key + " " + str(
                    value) + ", "
            else:
                appendedString += appendedString + color + key + " " + str(
                    value)
        return self.typeColor + self.itemName + cyan + ": " + str(
            self.amount) + appendedString

    def getBonusDict(self):
        return self.bonuses

    def equippedRepresentation(self):
        appendedString = " "
        counter = len(self.bonuses)
        for key, value in self.bonuses.items():
            counter -= 1
            color = green
            if value < 0:
                color = red
            if counter != 0:
                appendedString += appendedString + color + key + " " + str(
                    value) + ", "
            else:
                appendedString += appendedString + color + key + " " + str(
                    value)

        return self.typeColor + self.itemName + appendedString


class Recipe:
    def __init__(self,
                 itemsRequired:dict,
                 outputItem:str,
                 skillLevelXP:int,
                 craftingType:str,
                 outputAmount=1,
                 levelRequirement=0,
                 skillLevelRequired=0):
        self.itemsRequired = itemsRequired
        self.outputItem = outputItem
        self.skillLevelXP = skillLevelXP
        self.craftingType = craftingType
        self.outputAmount = outputAmount
        self.levelRequirement = levelRequirement
        self.skillLevelRequired = skillLevelRequired

    def __str__(self):
        string = ""
        if self.outputAmount > 1:
            string += str(self.outputAmount) + "x "
        string += self.outputItem
        for key, value in self.itemsRequired.items():
            string += blue + " " + str(
                value) + "x " + identifierDict[key].getColor() + key
        string += green + " Gives Skill XP: " + str(self.skillLevelXP)
        if self.levelRequirement > 0:
            string += red + " Needs Level: " + str(self.levelRequirement)
        if self.skillLevelRequired > 0:
            string += red + " Needs Skill XP: " + str(self.skillLevelRequired)
        return string

    def isPossibleCraft(self, stats, skillLevels):
        notInInventoryItems = {}
        for key, value in self.itemsRequired.items():
            if identifierDict[key].getItemAmount() < value:
                value2 = value - identifierDict[key].getItemAmount()
                notInInventoryItems.update({key: value2})
        if len(notInInventoryItems) != 0:
            print(red + "You currently lack: ")
            for key, value in notInInventoryItems.items():
                print(gold + str(value),
                      reset + "x " + str(identifierDict[key]))
            return False
        if stats["Level"] < self.levelRequirement:
            print(red + "This items needs Level " +
                  str(self.levelRequirement) +
                  " minimum to craft.\nYou are Level " + str(stats["Level"]) +
                  ".")
            return False
        if skillLevels[self.craftingType] < self.skillLevelRequired:
            print("This item needs Skill Level " +
                  str(self.skillLevelRequired) +
                  " minimum to craft.\nYou are Skill Level " +
                  str(skillLevels[self.craftingType]) + " in " +
                  self.craftingType + ".")
            return False
        return True

    def getItemsRequired(self):
        return self.itemsRequired

    def getOutputItem(self):
        return self.outputItem

    def getOutputItemRepresentation(self):
        string = ""
        if self.outputAmount > 1:
            string += str(self.outputAmount) + "x " + self.outputItem
        else:
            string += self.outputItem
        return string

    def getSkillLevelXP(self):
        return self.skillLevelXP

    def getCraftingType(self):
        return self.craftingType

    def getOutputAmount(self):
        return self.outputAmount

    def getLevelRequirement(self):
        return self.levelRequirement

    def getSkillLevelRequired(self):
        return self.skillLevelRequired


#Define items and assign ID tags
pineTwig = EquipmentItem("Weapon", "Pine Twig", 0, {"Item Damage": 2})
wolfFang = EquipmentItem("Weapon", "Wolf Fang", 0, {"Item Damage": 4})
ironDagger = EquipmentItem("Weapon", "Iron Dagger", 0, {
    "Item Damage": 5,
    "Dexterity": 2
})
ironShortSword = EquipmentItem("Weapon", "Iron Short Sword", 0, {
    "Item Damage": 7,
    "Dexterity": 1
})
ironLongsword = EquipmentItem("Weapon", "Iron Longsword", 0,
                              {"Item Damage": 9})
ironSpear = EquipmentItem("Weapon", "Iron Spear", 0, {
    "Item Damage": 8,
    "Crit Chance": 0.05
})
woodcuttersJaggedAxe = EquipmentItem("Weapon", "Woodcutter's Jagged Axe", 0, {
    "Item Damage": 10,
    "Dexterity": -1
})
banditCleaver = EquipmentItem("Weapon", "Bandit Cleaver", 0, {
    "Item Damage": 11,
    "Crit Chance": 0.03,
    "Dexterity": 1
})

koboldLeatherTunic = EquipmentItem("Chest", "Kobold Leather Tunic", 0,
                                   {"Defense": 2})
leatherTunic = EquipmentItem("Chest", "Leather Tunic", 0, {"Defense": 3})
studdedLeatherTunic = EquipmentItem("Chest", "Studded Leather Tunic", 0,
                                    {"Defense": 5})
reinforcedLeatherTunic = EquipmentItem("Chest", "Reinforced Leather Tunic", 0, {"Defense": 7})
leatherPants = EquipmentItem("Legs", "Leather Pants", 0, {
    "Defense": 2,
    "Dexterity": 1
})
studdedLeatherPants = EquipmentItem("Legs", "Studded Leather Pants", 0, {"Defense":4, "Dexterity":1})
woolenShoes = EquipmentItem("Feet", "Woolen Shoes", 0, {
    "Defense": 1,
    "Dexterity": 2
})
skullCap = EquipmentItem("Head", "Skull Cap", 0, {"Defense": 2})
woolenHat = EquipmentItem("Head", "Woolen Hat", 0, {
    "Defense": 1,
    "Perception": 1
})

foxPelt = InvItem("Misc", "Fox Pelt", 0)
foxTail = InvItem("Misc", "Fox Tail", 0)
wolfPelt = InvItem("Misc", "Wolf Pelt", 0)
koboldEye = InvItem("Misc", "Kobold Eye", 0)
quartzStone = InvItem("Misc", "Quartz Stone", 0)
fungusIchor = InvItem("Misc", "Fungus Ichor", 0)
northFernSporeSac = InvItem("Misc", "Northern Fern Spore-Sac", 0)
heavyChitinPlate = InvItem("Misc", "Heavy Chitin Plate", 0)
redBannerToken = InvItem("Misc", "Red Banner Token", 0)

mushroom = ConsumableItem("Mushroom", 0, {"Current HP": 15})
freshPerch = ConsumableItem("Fresh Perch", 0, {"Current HP": 20})
roastMushroomSkewer = ConsumableItem("Roast Mushroom Skewer",
                                 0, {"Current HP": 22},
                                 effects=("Hearty Meal|1", ))
roastMeatSkewer = ConsumableItem("Roast Meat Skewer",
                                     0, {"Current HP": 48},
                                     effects=("Hearty Meal|1", ))

insectFlesh = ConsumableItem("Insect Flesh",
                             0, {"Current HP": 10},
                             effects=("Food Poisoning|1", ))
potionOfSight = ConsumableItem("Potion of Sight",
                               0, {},
                               effects=("Improved Sight|1", ))

identifierDict = {
    "Bandit Cleaver": banditCleaver,
    "Fresh Perch": freshPerch,
	"Fox Pelt": foxPelt,
	"Fox Tail": foxTail,
    "Fungus Ichor": fungusIchor,
    "Heavy Chitin Plate": heavyChitinPlate,
    "Insect Flesh": insectFlesh,
    "Iron Dagger": ironDagger,
    "Iron Longsword": ironLongsword,
    "Iron Short Sword": ironShortSword,
    "Iron Spear": ironSpear,
    "Kobold Eye": koboldEye,
    "Kobold Leather Tunic": koboldLeatherTunic,
    "Northern Fern Spore-Sac": northFernSporeSac,
    "Mushroom": mushroom,
    "Leather Tunic": leatherTunic,
    "Leather Pants": leatherPants,
    "Pine Twig": pineTwig,
    "Potion of Sight": potionOfSight,
    "Quartz Stone": quartzStone,
    "Red Banner Token": redBannerToken,
    "Reinforced Leather Tunic":reinforcedLeatherTunic,
    "Roast Meat Skewer": roastMeatSkewer,
    "Roast Mushroom Skewer": roastMushroomSkewer,
    "Skull Cap": skullCap,
    "Studded Leather Tunic": studdedLeatherTunic,
    "Studded Leather Pants": studdedLeatherPants,
    "Wolf Fang": wolfFang,
    "Wolf Pelt": wolfPelt,
    "Woolen Hat": woolenHat,
    "Woolen Shoes": woolenShoes
}

sightPotRecipe = Recipe({
    "Kobold Eye": 2,
    "Fungus Ichor": 1
}, "Potion of Sight", 8, "Alchemy")

recipeDict = {"Potion of Sight": sightPotRecipe}
