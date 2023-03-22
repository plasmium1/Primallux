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


defaultQuests = {
        "Bandits": 0,
		"Bandits II": 0,
		"Bandits III": 0,
		"Goblins": 0,
		"Goblins II": 0,
		"Goblins III": 0,
		"Goblins IV": 0,
		"Bounty: Troll": 0,
		"Wolves": 0,
		"Wolves II": 0,
		"Rampage of the Silverfang": 0,
		"Recovering Lost Goods": 0,
		"Caravan Guard: Moonreach -> Wroburg": 0,
		"Caravan Guard: Wroburg -> Eldenholm": 0,
		"Caravan Guard: Moonreach -> Firway": 0,
		"Investigating the Ruins": 0,
		"Caves": 0,
		"Caves II": 0,
		"Caves III": 0,
		"Cavernous Ruin": 0,
		"Ruins of A'Thoraic": 0,
		"The Rise of Viraphan": 0,
		"Rats I": 0,
		"Rats II": 0,
		"Rats III": 0,
		"Crown of the Vermin": 0,
		"Depths of Moonreach": 0,
		"Bounty: Elosse the Hunter": 0,
		"Bounty: Polkond the Burglar": 0,
		"Bounty: Ildonos Bradanavo the Reaver": 0,
		"Bounty: Hrolg the Crusher": 0,
		"Bounty: Dervild Merranb the Mad": 0,
		"Bounty: Limmer Tinner the Quick": 0,
		"The Journey to the West": 0,
		"Tales of a Faraway Land": 0,
		"Sun's Blessed Children": 0,
		"The Immortal War I": 0, #Jade Empire vs Silvaris
		"The Immortal War II": 0,
		"The Immortal War III": 0,
		"Siege of Yingzhou": 0,
		"The Goblin Warlord": 0,
		"Capture Flameweave Fox": 0,
		"Red Banner Conspiracy": 0,
		"Siege of Wroburg": 0,
		"Legacy of the Sky": 0,
		"Lake's Wrath": 0,
		"Stars Falling": 0,
		"Baligor's Truest Wish": 0,
		"Barin Za'al's Ambition": 0,
		"Purifying the Blightlands": 0,
		"Bastard Sons of Tellmaran": 0,
		"The Crying Fallen Seraph": 0,
		"Legacy of the Western Land": 0,
		"Revival of Raz'Shi": 0,
		"Thorrasson, the Conqueror": 0,
		"Oddity in the Depths": 0,
		"Underworld Descent": 0,
		"The Supreme One's Last Reckoning": 0,
		"The Return of the Old Gods": 0,
		"The Fall of Wroburg": 0,
		"The Red Moon": 0,
		"Discord in the Association": 0,
		"Plight of the Illiani": 0,
		"Wroburg's Succession": 0,
		"Disturbance in the Hendron Pact": 0,
		"Requiem for the Ancient General": 0,
		"Legacy of Demonkind": 0,
		"Elven Civil War": 0,
		"The House of Twilight's Truest Wish": 0,
		"Beginning of the Calamity": 0,
		"The Cloud-Giants' Grand Parade": 0,
		"The Descent of the Nine": 0
}

defaultRep = {
        "Empire of Silvaris": 0,
        "Eldenholm Resistance": 0,
        "Grekkian City States": 0,
        "Raz'Shi Oligarchy": 0,
        "Tourial": 0,
        "Moonreach Guild": 0,
        "Kingdom of Wroburg": 0,
        "House Bogyar": 0,
        "House Valion": 0,
        "House Ertannis": 0,
        "House Illiani": 0,
        "Crown Restorationists": 0,
        "Hendron Pact": 0,
        "High City of Alfarihil": 0,
		"Holy City Dian": 0,
		"Jade Imperium": 0,
		"Divine Dragon Sect": 0,
		"Thundercloud Pavilion": 0,
		"Red Path Sect": 0,
		"Black Gate Sect": 0,
		"Adventurer's Association": 0,
        "Firway": 0,
        "House Hariel": 0,
		"House Minviert": 0,
        "Great Dune Caravans": 0,
        "House Rundal": 0,
        "Red Banner Company": 0,
        "Cerrunis": 0,
        "Northern Hordes": -50,
        "Mountain Jarldom": 0,
        "Draconic Accord": 0,
        "Green Consortium": 0,
		"Holy City Dian": 0,
        "Light Pantheon": 0,
        "Death Pantheon": 0,
        "Life Pantheon": 0,
        "Nature": 0,
        "Enclave of Moon-Peak": 0,
        "Stellar Covenant": 0,
        "Irithyn Concord": 0,
        "Yorkal Hive": 0,
        "Sirph": 0,
		"Chevyr-Lonn Union"
        "Mind of the Void": -1000
    }