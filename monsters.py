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


class Mob:
  def __init__(self, name, hp, damage_lower, damage_upper, speed, defense, giveXP, enterBattleText, duringBattleText, exitBattleText, taunt, pacifyText, ifPacifyBonus, dropSilver, convinceThreshold=50, lootTable={"Rolls":1}, spells=[], elementalDamage={}, elementalDefense={}, faction="", factionRepDecrease=0, dialogue=(), killRepBonus={}, mobFleeHP=-1, fleeText="", encounterThreshold=150, runawayRepCut=0, runawayText="", mobType="Warrior"):
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
    self.elementalDamage = elementalDamage
    self.elementalDefense = elementalDefense
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
  def getElementalDamage(self):
      return self.elementalDamage
  def getElementalDefense(self):
      return self.elementalDefense
    
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

          
#Normal mobs
hungryWolf = Mob("Hungry Wolf", 48, 3, 8, 1, 0, 4, "A ragged wolf appears, drool slavering from its jaws.", "It growls in hunger. Perhaps prey has been hard to find these days.", "The wolf collapses, finally succumbing to its wounds and starvation.", "The wolf snarls, and moves back in to counterattack.", "The wolf growls, but leaves you alone to find someone else.", 3, 
 1, convinceThreshold=80, lootTable={"Rolls":1, "Wolf Fang":15, "Nothing":70, "Wolf Pelt":15}, faction="Nature", factionRepDecrease=5)

forestWolf = Mob("Forest Wolf", 64, 5, 11, 3, 0, 6, "A furred wolf appears from the trees, its coat of varying shades of brown, that blends into the rest of the landscape.", "A rumbling growl emanates from the wolf's throat, the threat clear in the air.", "The wolf makes a whining noise, as it falls to the ground, blood leaking away from its body, as it expires.", "The wolf exposes its canines, showing you its teeth.", "The wolf sniffs your hand in curiosity, before leaving you alone, disappearing into the trees.", 4, 5, convinceThreshold=60, lootTable={"Rolls":1, "Wolf Fang":20, "Fine Wolf Pelt":5, "Wolf Pelt":10, "Nothing":65}, faction="Nature", factionRepDecrease=5, mobFleeHP=12, fleeText="The wolf feels its wounds, and the pain that suffuses its body. It runs, loping away and out of sight, escaping into the forest to lick its wounds.")

#direWolf = Mob("Dire Wolf", 75)

# silvermane = Mob()

forestFox = Mob("Forest Fox", 36, 6, 9, 36, 0, 7, "A small fox, furred in light browns that liken it to the color of dried pine needles, approaches you.", "The fox circles about, its beady eyes flicking up at your much larger form, as its tongue darts in and out to lick at its mouth.", "The fox falls, succumbing to its wounds, as it frantically paws at the ground in an attempt to escape, before falling still.", "The fox yips harshly, as it quickly dashes back a distance from you.", "The fox settles, its eyes no longer flicking everywhere about you and your surroundings, calming, before it leaves into the forest.", 4, 5, convinceThreshold=55, lootTable={"Rolls":1, "Fox Pelt":10, "Fox Tail":5, "Nothing":85}, faction="Nature", factionRepDecrease=5, mobFleeHP=15, fleeText="The fox's jumpiness reaches a new high, as it whimpers, and dashes away from the scene.")

koboldScout = Mob("Kobold Scout", 70, 10, 18, 18, 4, 10, "A diminutive lizardine biped meets you, holding a pair of daggers in its hands. It hisses at you in Kobold. Too bad you don't know what it's saying.", "The Kobold looks nervously at you, and at the passage behind it.", "The Kobold screeches in pain. It expires slowly, leaving the cowardly lizard as a corpse on the ground.", "The Kobold waves its daggers, which shine dully in the light. It's got a certain shake in its legs.", "The kobold hisses, and seeing that you don't present much danger to it, it runs off.", 8, 4, convinceThreshold=100, lootTable={"Rolls":1, "Iron Dagger":28, "Kobold Leather Tunic":30, "Kobold Eye":15, "Nothing":27}, faction="Draconic Accord", factionRepDecrease=10, killRepBonus={"Goblin Consortium":-10, "Mountain Jarldom":5}, mobFleeHP=15, fleeText="The kobold sees that you're too powerful, and itself, being too hurt to keep fighting. It runs away in fear.")

caveShrieker = Mob("Cave Shrieker", 22, 16, 28, 40, 0, 16, "You spot a large mushroom, far too large to be natural, glowing with greenish lights underneath its cap, and in small points upon its stem.", "The mushroom unleashes a terrible shrieking noise, one that causes you to feel instinctive discomfort.", "The living fungus shudders, as you spot white liquid, tinted green by the fading lights of the moving fungus's body, ooze out of its shriveling body.", "The mushroom screeches, even louder than it already has.", "", "", 6, convinceThreshold=False, lootTable={"Rolls":1, "Fungus Ichor":25, "Nothing":75}, spells=("Discordant Shriek|2",), killRepBonus={"Draconic Accord":4, "Tourial":8}, mobType="Skirmisher")

caveCrawler = Mob("Cave Crawler", 200, 4, 9, 2, 16, 18, "You spot what looks like a massive burly creature crawling upon segmented legs.\nIt doesn't seem that welcoming to the invader in its home.", "The creature moves at a plodding pace, flicking its legs, as it prepares to charge.", "The oversized insect finally collapses, its fleshy insides weak in comparison to its thick armor.", "The creature shifts its body, as you hear the a faint clacking noise as it flexes the plates on its armor.", "", "", 18, convinceThreshold=False, lootTable={"Rolls":1, "Heavy Chitin Plate":15, "Insect Flesh":30, "Nothing":55})

#Quest mobs
forestBandit1 = Mob("Forest Bandit", 120, 9, 26, 50, 12, 20, "A man dressed in weathered leather armor walks out from the trees, as he cracks his neck while he walks toward you, as he draws a short sword and hefts it before you.", "The bandit jumps back in for the kill, swinging his blade outward to seek for your flesh. The man wants your belongings, everything you have, in the same greed and drive to steal, that led to his stealing from the merchant caravan.", "The man succumbs to his wounds, falling, and collapsing to the ground, as he spasms in his death throes, while an expanding pool of blood leaks out and stains the forest floor.", "The man sneers an ugly grin as he draws your blood.", "", "", 10, convinceThreshold=False, lootTable={"Rolls":1, "Iron Short Sword":5, "Skull Cap":10, "Leather Tunic":8, "Nothing":77})

forestBandit2 = Mob("Forest Bandit", 110, 12, 30, 54, 10, 22, "A man dressed in a simple peasant's rucksack and a shoddy breastplate greets you with a grooved woodcutter's axe raised in a threatening stance.", "The man swings his weapon about, as he loosen ups his limbs and smiles grimly, his scraggly beard rolling over his uneven teeth.", "The bandit clutches at his wounds, a final gurgling cough of blood gushes out of his mouth and splatters onto the ground. \nHe collapses, dead.", "The bandit laughs as he lands the strike. \"Just give up already! You're wasting my time fighting you!\"", "", "", 10, convinceThreshold=False, lootTable={"Rolls":1, "Woodcutters Jagged Axe":5, "Leather Tunic":8, "Leather Pants":10, "Nothing":77})

#Bosses and mini-bosses to follow.
caveScythian = Mob("Cave Scythian", 155, 15, 20, 65, 4, 44, "A strange insectoid creature, with a half-crescent head, drops out of the shadows to attack you.\nIt holds a pair of its limbs like arms, as four segmented legs clack on the stone of the cave floor.\nThe arms shine in the low light of the cave", "The insect's head opens slightly, showing a little glowing orb within, like a pearl in a clam's shell.", "The scythian clatters onto the ground, a furious gleam slowly dimming, while its crescent head opens and closes slowly.", "The creature hefts its blade-like appendages, in a threatening, predatory, stance.", "", "", 30, convinceThreshold=False, lootTable={"Rolls":1, "Inert Cave Pearl":46, "Serrated Chitin Blade":34}, mobFleeHP=10, fleeText="Even predators know when to run, as the insectoid creature dashes away from the battle, vanishing into the shadows.", spells=("Bleeding Strike|2", "Blinding Flash|1"), mobType="Skirmisher")

banditLeaderToderick = Mob("Bandit Leader Toderick", 380, 18, 32, 30, 18, 35, "A large man emerges from one of the tents, \na powerful man dressed in a set of damaged armor looted with the livery of a trading guild, who wields a wicked cleaver with a jagged edge.\n\"Come to destroy my crew, eh?\"\n\"Well, you'll be pavin' the road to my next big windfall!\"", "\"Boy, you're gettin' me fired up! Come on, let's make this easier, eh?\"", "The man falls, his eyes open wide in surprise and indignity, as he tries to roar, and stand back up, to use his blade as a cane.\nBut yet he loses his grip, his hand slick with his own blood, as he falls to the ground a second time, never to move again.", "The bandit smirks grimly, \"That's what ya get for takin' out mah boys!\"", "", "", 30, convinceThreshold=False, lootTable={"Rolls":2, "Bandit Cleaver":8, "Studded Leather Tunic":8, "Leather Pants":8, "Woolen Shoes":8, "Woolen Hat":8, "Red Banner Token":18}, killRepBonus={"House Valion":5, "Kingdom of Wroburg":10}, faction="Red Banner Company", factionRepDecrease=25, spells=("Bleeding Strike|3", "Heavy Strike|1"), mobType="Skirmisher")

mobDict = {"Hungry Wolf":hungryWolf,
           "Forest Wolf":forestWolf,
		   "Forest Fox":forestFox,
           "Kobold Scout":koboldScout,
           "Cave Shrieker":caveShrieker,
           "Cave Crawler":caveCrawler,
           "Forest Bandit 1":forestBandit1,
           "Forest Bandit 2":forestBandit2,
           "Bandit Leader Toderick":banditLeaderToderick,
           "Cave Scythian":caveScythian}