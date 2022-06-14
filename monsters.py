from itertools import islice
from random import randint, choices, sample
from ansi.colour.rgb import rgb256
import magic
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


class mob:
  def __init__(self, name, hp, damage_lower, damage_upper, speed, defense, giveXP, enterBattleText, duringBattleText, exitBattleText, taunt, pacifyText, ifPacifyBonus, dropSilver, convinceThreshold=50, lootTable={"Rolls":1}, spells=[], faction="", factionRepDecrease=0, dialogue=(), killRepBonus={}, mobFleeHP=-1, fleeText="", encounterThreshold=150, runawayRepCut=0, runawayText="", mobType="Warrior"):
    self.name = name
    self.faction = faction
    self.mobHP = hp
    self.mobMaxHP = hp
    self.dropSilver = dropSilver
    self.damageLower = damage_lower
    self.defaultDamageLower = damage_lower
    self.damageUpper = damage_upper
    self.defaultDamageUpper = damage_upper
    self.speed = speed
    self.defaultSpeed = speed
    self.lootTable = lootTable
    self.convinceThreshold = convinceThreshold
    self.defense = defense
    self.defaultDefense = defense
    self.giveXP = giveXP
    self.spells = spells
    self.defaultSpells = spells
    self.factionRepDecrease = factionRepDecrease
    self.enterBattleText = enterBattleText
    self.duringBattleText = duringBattleText
    self.exitBattleText = exitBattleText
    self.fleeText = fleeText
    self.taunt = taunt
    self.pacifyText = pacifyText
    self.ifPacifyBonus = ifPacifyBonus
    self.dialogue = dialogue
    self.killRepBonus = killRepBonus
    self.mobFleeHP = mobFleeHP
    self.encounterThreshold = encounterThreshold
    self.runawayRepCut = runawayRepCut
    self.runawayText = runawayText
    self.mobType = mobType
  def __str__(self):
    return self.name + " " + red + "HP: " + str(self.mobHP) + "/" + str(self.mobMaxHP)
  
  def takeDamage(self, amount):
    if (amount - self.defense) < 0:
      return
    self.mobHP -= (amount - self.defense)

  def dealDamage(self):
    return randint(self.damageLower, self.damageUpper)

  def resetHP(self):
    self.mobHP = self.mobMaxHP
  def addHP(self, value):
    self.mobHP += value
  
  def lootGenerate(self):
    keys = []
    values = []
    for key, value in islice(self.lootTable.items(), 1, None):
      keys.append(key)
      values.append(value)
    returnedList = choices(keys, weights=values, k=self.lootTable["Rolls"])
    for value in returnedList:
      placeholder = []
      if value == "Nothing":
        returnedList.remove("Nothing")
        placeholder.append("Nothing")
    returnedList.extend(placeholder)
    return returnedList
  def getDamageUpper(self):
    return self.damageUpper
  def addDamage(self, value):
    self.damageUpper += value
    self.damageLower += value
    if self.damageLower < 0:
      self.damageLower = 0
    if self.damageUpper < 0:
      self.damageUpper = 0
  def resetDamage(self):
    self.damageUpper = self.defaultDamageUpper
    self.damageLower = self.defaultDamageLower
  def resetSpeed(self):
    self.speed = self.defaultSpeed
  def addSpeed(self, value):
    self.speed += value
    if self.speed < 0:
      self.speed = 0
  def getDropSilver(self):
    return self.dropSilver
  def getMobHP(self):
    return self.mobHP
  def getMobName(self):
    return self.name
  def getSpeed(self):
    return self.speed
  def getDefense(self):
    return self.defense
  def resetDefense(self):
    self.defense = self.defaultDefense
  def addDefense(self, value):
    self.defense += value
    if self.defense < 0:
      self.defense = 0
  def getXP(self):
    return self.giveXP
  def getRepDecrease(self):
    return self.factionRepDecrease
  def getEnterText(self):
    return self.enterBattleText
  def getDuringText(self):
    return self.duringBattleText
  def getExitText(self):
    return self.exitBattleText
  def getPacifyText(self):
    return self.pacifyText
  def getFleeText(self):
    return self.fleeText
  def getTaunt(self):
    return self.taunt
  def pacifyText(self):
    return self.pacifyText
  def getPacifyBonus(self):
    return self.ifPacifyBonus
  def getFaction(self):
    return self.faction
  def getMobFleeHP(self):
    return self.mobFleeHP
  def getEncounterThreshold(self):
    return self.encounterThreshold
  def getDialogue(self):
    if len(self.dialogue) >= 1:
      return self.dialogue[randint(0, len(self.dialogue))]
    else:
      return ""
  def isDefeated(self):
    if self.mobHP <= 0:
      return True
    else:
      return False
  def getSpells(self):
    return self.spells
  def getRunawayRepCut(self):
    return self.runawayRepCut
  def getRunawayText(self):
    return self.runawayText
  def resetSpells(self):
    self.spells = self.defaultSpells
  def removeSpell(self):
    if len(self.spells) > 0:
      removedItem = sample(self.spells)[0]
      self.spells.remove(removedItem)
    
  def disarm(self, playerStats, playerRep):
    if type(self.convinceThreshold) == int:
      if self.faction == "":
        if choices(("succeed", "fail"), weights=(playerStats["Charisma"], self.convinceThreshold)) == ["succeed"]:
          return True
        else:
          return False
      else:
        if playerRep[self.faction]<-100:
          return False
        elif playerRep[self.faction]>100:
          return True
        else:
          if choices(("succeed", "fail"), weights=(playerStats["Charisma"], round(self.convinceThreshold+(playerRep[self.faction]/10)))) == ["succeed"]:
            return True
          else:
            return False
    else:
      return False
  def getMobType(self):
    return self.mobType

          

hungryWolf = mob("Hungry Wolf", 38, 3, 8, 1, 0, 4, "A ragged wolf appears, drool slavering from its jaws.", "It growls in hunger. Perhaps prey has been hard to find these days.", "The wolf collapses, finally succumbing to its wounds and starvation.", "The wolf snarls, and moves back in to counterattack.", "The wolf growls, but leaves you alone to find someone else.", 3, 
 1, convinceThreshold=60, lootTable={"Rolls":1, "Wolf Fang":15, "Nothing":70, "Wolf Pelt":15}, faction="Nature", factionRepDecrease=5)

#direWolf = mob("Dire Wolf", 45)

koboldScout = mob("Kobold Scout", 60, 10, 18, 18, 4, 10, "A diminutive lizardine biped meets you, holding a pair of daggers in its hands. It hisses at you in Kobold. Too bad you don't know what it's saying.", "The Kobold looks nervously at you, and at the passage behind it.", "The Kobold screeches in pain. It expires slowly, leaving the cowardly lizard as a corpse on the ground.", "The Kobold waves its daggers, which shine dully in the light. It's got a certain shake in its legs.", "The kobold hisses, and seeing that you don't present much danger to it, it runs off.", 8, 4, convinceThreshold=100, lootTable={"Rolls":1, "Iron Dagger":28, "Kobold Leather Tunic":30, "Kobold Eye":15, "Nothing":27}, faction="Draconic Accord", factionRepDecrease=10, killRepBonus={"Goblin Consortium":-10, "Mountain Jarldom":5}, mobFleeHP=15, fleeText="The kobold sees that you're too powerful, and itself, being too hurt to keep fighting. It runs away in fear.")

caveShrieker = mob("Cave Shrieker", 12, 16, 28, 40, 0, 16, "You spot a large mushroom, far too large to be natural, glowing with greenish lights underneath its cap, and in small points upon its stem.", "The mushroom unleashes a terrible shrieking noise, one that causes you to feel instinctive discomfort.", "The living fungus shudders, as you spot white liquid, tinted green by the fading lights of the moving fungus's body, ooze out of its shriveling body.", "The mushroom screeches, even louder than it already has.", "", "", 6, convinceThreshold=False, lootTable={"Rolls":1, "Fungus Ichor":25, "Nothing":75}, spells=("Discordant Shriek|2",), killRepBonus={"Draconic Accord":4, "Tourial":8}, mobType="Skirmisher")

caveCrawler = mob("Cave Crawler", 200, 4, 9, 2, 16, 18, "You spot what looks like a massive burly creature crawling upon segmented legs.\nIt doesn't seem that welcoming to the invader in its home.", "The creature moves at a plodding pace, flicking its legs, as it prepares to charge.", "The oversized insect finally collapses, its fleshy insides weak in comparison to its thick armor.", "The creature shifts its body, as you hear the a faint clacking noise as it flexes the plates on its armor.", "", "", 18, convinceThreshold=False, lootTable={"Rolls":1, "Heavy Chitin Plate":15, "Insect Flesh":30, "Nothing":55})

caveScythian = mob("Cave Scythian", 125, 15, 20, 35, 4, 24, "A strange insectoid creature, with a half-crescent head, drops out of the shadows to attack you.\nIt holds a pair of its limbs like arms, as four segmented legs clack on the stone of the cave floor.\nThe arms shine in the low light of the cave", "The insect's head opens slightly, showing a little glowing orb within, like a pearl in a clam's shell.", "The scythian clatters onto the ground, as its fury leaves it, its crescent head opening and closing slowly, as light leaves the little orb.", "The creature hefts its blade-like appendages, in a threatening, predatory, stance.", "", "", 28, convinceThreshold=False, lootTable={"Rolls":1, "Inert Cave Pearl":46, "Serrated Chitin Blade":34}, mobFleeHP=10, fleeText="Even predators know when to run, as the insectoid creature dashes away from the battle, vanishing into the shadows.", spells=("Bleeding Strike|2", "Blinding Flash|1"), mobType="Skirmisher")