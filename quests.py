from ansi.colour.rgb import rgb256
from monsters import mobDict

black = "\u001b[30m"
red = "\u001b[31m"
green = rgb256(0x00, 0xff, 0x09)
yellow = "\u001b[93m"
orange = rgb256(0xfc, 0x94, 0x03)
gold = rgb256(0xe6, 0xcb, 0x02)
blue = "\u001b[34m"
magenta = "\u001b[95m"
cyan = rgb256(0x61, 0xff, 0xf4)
purple = rgb256(0xbe, 0x03, 0xfc)
white = "\u001b[37m"
bold = "\u001b[1m"
underline = "\u001b[4m"
italic = "\u001b[3m"


#Class for storing data for quests! Quest progress is synced in the main file dictionary but this saves the individual parts of npc text, various other flavor text, the workflow for it, needed rep, and more. This should be tied into a Quest-type interaction in order to launch it. Maybe various other quest type interactions to handle intermediary quest parts?
class Quest:
    def __init__(self, questName:str, questDescription:str, difficulty:int, introText:str, 
                 questChainTuple:tuple,
                 neededReputation=(None, 0), reward={}):
        self.questName = questName
        self.questDescription = questDescription
        self.difficulty = difficulty
        self.introText = introText
        self.questChainTuple = questChainTuple
        self.neededReputation = neededReputation

    def __str__(self):
        return blue + "-----<" + self.questName + ">-----\n" + green + self.questDescription + red + "\nDifficulty: " + str(self.difficulty)
        

    def getQuestName(self):
        return self.questName

    def getDifficulty(self):
        return self.difficulty

    def getIntroText(self):
        return self.introText

    def getQuestChainTuple(self):
        return self.questChainTuple

    def getNeededReputation(self):
        return self.neededReputation
        
    def getReward(self):
        return self.reward


class Objective:
    def __init__(self, type:str, stage:int, locationName="", location=(), mob="", item="", currentAmount=0, amount=1, npcName="", npcDialogue=""):
        self.type = type
        self.stage = stage
        self.locationName = locationName
        self.location = location
        self.mob = mob
        self.item = item
        self.currentAmount = currentAmount
        self.amount = amount
        self.npcName = npcName
        self.npcDialogue = npcDialogue

    def __str__(self):
        string = ""
        if self.type == "Kill":
            string = red + self.type
            string += " " + self.amount
            string += " " + str(self.mob)
            if self.amount > 1:
                string += "s"
            if self.locationName != "":
                string += " at " + self.locationName
        elif self.type == "Fetch":
            string = orange + self.type
            string += " " + self.amount
            string += " " + str(self.item)
            if self.amount > 1:
                string += "s"
            if self.locationName != "":
                string += " at " + self.locationName
        elif self.type == "Give":
            string = yellow + self.type
            string += " " + self.amount
            string += " " + self.item.getColoredName() 
            if self.amount > 1:
                string += "s"
            string += " to " + self.npcName
            string += " at " + self.locationName
        elif self.type == "Scout":
            string = cyan + self.type
            string += " out the " + self.locationName
        elif self.type == "Go":
            string = cyan + self.type
            string += " to " + self.locationName
        elif self.type == "Clear":
            string = purple + self.type
            string += " out " + self.locationName
        elif self.type == "Talk":
            string = green + self.type
            string += " to " + self.npcName
            string += " at " + self.locationName
        return string


    def getType(self):
        return self.type
    def getStage(self):
        return self.stage
    def getLocationName(self):
        return self.locationName
    def getLocation(self):
        return self.location
    def getMob(self):
        return self.mob
    def getItem(self):
        return self.item
    def getCurrentAmount(self):
        return self.currentAmount
    def getAmount(self):
        return self.amount
    def getNPCName(self):
        return self.npcName
    def getNPCDialogue(self):
        return self.npcDialogue
    def incrementAmount(self):
        self.currentAmount += 1

objective1 = Objective("Scout", 1, "Fortress Southern Road", location=(28,))
objective2 = Objective("Scout", 2, "Bandit Camp", location=(34,))
objective3 = Objective("Clear", 3, "Bandit Camp", location=(35,))
objective4 = Objective("Kill", 4, "Bandit Camp", location=(35,), mob=mobDict["Bandit Leader Toderick"])



quest1 = Quest("Bandits", "A group of bandits have been ambushing trade caravans coming to the Moonreach Fortress for a while now. And the Guild wants you to find them and clear them out.", 4, "To begin, the Guild wishes for you to investigate the disappearance of a traveling merchant who was coming to the fortress.", (objective1, objective2, objective3, objective4), reward={"Ghost Silver":50, "XP":30})

# quest2 = Quest("")

questsDict = {"Bandits":quest1}
moonreachQuests = ("Bandits",)
