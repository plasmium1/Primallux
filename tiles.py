from ansi.colour.rgb import rgb256
from ansi.colour.fx import reset
from random import choices, choice
import monsters
from playerInventory import identifierDict
from monsters import mobDict, Mob
#Use this later for handling the tile if statements?
black = "\u001b[30m"
red = "\u001b[31m"
green = rgb256(0x00, 0xff, 0x09)
yellow = "\u001b[93m"
orange = rgb256(0xff, 0x73, 0x00)
gold = rgb256(0xe6, 0xcb, 0x02)
silver = rgb256(0xbf, 0xbf, 0xbf)
blue = "\u001b[34m"
magenta = "\u001b[95m"
cyan = rgb256(0x61, 0xff, 0xf4)
purple = rgb256(0xbe, 0x03, 0xfc)
white = "\u001b[37m"
bold = "\u001b[1m"
underline = "\u001b[4m"
italic = "\u001b[3m"

class Merchant:
  def __init__(self, name, shopName, flavorText, faction, buyDict, sellDict={}, dialogue="", discounts=""):
    self.name = name
    self.shopName = shopName
    self.flavorText = flavorText
    self.faction = faction
    self.buyDict = buyDict
    self.sellDict = sellDict
    self.dialogue = dialogue
    self.discounts = discounts

  def __str__(self):
    return rgb256(0x4a, 0xff, 0xa1) + self.shopName + ", " + self.name
  def getName(self):
    return self.name
  def getShopName(self):
    return self.shopName
  def getFlavorText(self):
    return self.flavorText
  def getFaction(self):
    return self.faction
  def getBuyDict(self):
    return self.buyDict
  def getDiscounts(self):
    return self.discounts
  def getDialogue(self):
    return self.dialogue
  def getShopItems(self):
    return self.buyDict
  def getSellItems(self):
    return self.sellDict
  def getItemPrice(self, val):
    return self.sellDict[val]
  def printBuyItems(self):
    for key, value in self.buyDict.items():
      print(str(identifierDict[key]) + blue + " Cost: " + silver + str(value))
  def printSellItems(self):
    myString = ""
    for key, value in self.sellDict.items():
      myString += str(identifierDict[key]) + blue + " Price: " + gold + str(value) + "\n"
    return myString
  def checkForItemInBuy(self, itemName):
    for key in self.buyDict.keys():
      if itemName == key:
        return True
    return False
  def checkForItemInSell(self, itemName):
    for key in self.sellDict.keys():
      if itemName == key:
        return True
    return False

class Dialogue:
  def __init__(self, greeting={}, goodbye={}, metBefore=False, dialogueRounds={}):
    self.greeting = greeting
    self.goodbye = goodbye
    self.dialogueRounds = dialogueRounds
    self.metBefore = metBefore

  def getMetBefore(self):
    return self.metBefore
  def setMetBefore(self, value):
    self.metBefore = value
  def getGreeting(self, turn, questDict):
    for key, value in self.greeting.items():
      key = key.split(" ")
      if key[0] == "Starter":
        print(value)
      elif key[0] == "Turns":
        if key[1] == "<" and self.metBefore:
          if turn < int(key[2]):
            return value
        elif key[1] == "<=" and self.metBefore:
          if turn <= int(key[2]):
            return value
        elif key[1] == ">" and self.metBefore:
          if key > int(key[2]):
            return value
        elif key[1] == ">=" and self.metBefore:
          if key >= int(key[2]):
            return value
        else:
          return ""
      #Make another conditional that accepts Quests for dialogues.
  
  def getGoodbye(self, turn):
    for key, value in self.goodbye.items():
      key = key.split(" ")
      if key[0] == "Starter":
        self.setMetBefore(True)
        print(value)
      elif key[0] == "Turns":
        if key[1] == "<" and self.metBefore:
          if turn < int(key[2]):
            self.setMetBefore(True)
            return value
        elif key[1] == "<=" and self.metBefore:
          if turn <= int(key[2]):
            self.setMetBefore(True)
            return value
        elif key[1] == ">" and self.metBefore:
          if key > int(key[2]):
            self.setMetBefore(True)
            return value
        elif key[1] == ">=" and self.metBefore:
          if key >= int(key[2]):
            self.setMetBefore(True)
            return value
      return ""

  def getOneFurtherDialogue(self, key):
      return "".join(list(filter(lambda a: a not in ("@", "*", "#", "`"), self.dialogueRounds[key])))
  def getFurtherDialogueDict(self):
      return self.dialogueRounds
class Interactible:
  def __init__(self, type, interactText, dialogue="", tileID=0, toTileID=0, recipes={}, lootTable={}, gatherMod="", merchants="", craftingType=""):
    self.type = type
    self.interactText = interactText
    self.dialogue = dialogue
    self.tileID = tileID
    self.toTileID = toTileID
    self.recipes = recipes
    self.lootTable = lootTable
    self.gatherMod = gatherMod
    self.merchants = merchants
    self.craftingType = craftingType
    try:
      self.originalNothing = lootTable["Nothing"]
    except KeyError:
      self.originalNothing = 0

  def resetNothing(self):
    self.lootTable["Nothing"] = self.originalNothing
  def resetNothings(self):
    if self.lootTable["Nothing"] < 0:
      self.lootTable["Nothing"] = 0
  def getType(self):
    return self.type
  def getInteractText(self):
    return self.interactText
  def getDialogue(self):
    return self.dialogue
  def getTileID(self):
    return self.tileID
  def getToTileID(self):
    return self.toTileID
  def getGatherMod(self):
    return self.gatherMod
  def getRecipes(self):
    return self.recipes
  def getCraftingType(self):
    return self.craftingType
  def getLoot(self, stat):
    returnList = []
    listKeys = []
    listValues = []
    modifiedLootTable = self.lootTable
    nothingVal = modifiedLootTable["Nothing"]
    modifiedLootTable["Nothing"] -= stat
    if modifiedLootTable["Nothing"] < 0:
      modifiedLootTable = 0
    for key, value in self.lootTable.items():
      listKeys.append(key)
      listValues.append(value)
    del listKeys[0]
    del listValues[0]
    
    returnList = choices(listKeys, listValues, k=self.lootTable["Rolls"])
    modifiedLootTable["Nothing"] = nothingVal #Reset nothing value so that it doesn't just allow you to get infinite resources by spamming the interation.
    return returnList
  def setLootTableModifier(self, setModStat):
    #Subtrat mod from "nothing"
    self.lootTable["Nothing"] -= setModStat
    #Modifier set and finished.
  def getMerchants(self):
    return self.merchants

dialogue1 = Dialogue(greeting={"Starter":"\"Hail the Moons!\"", "Turns < 200":"\"You new here?\"", "Turns > 200":"\"I'm glad to see you again!\"", "Turns > 700":"\"Ah, it's you again. How long has it been, this time?\""}, goodbye={"Starter":"\"I wish you luck on your journey!\""}, metBefore=False, dialogueRounds={"f)Ask about the fortress.|Turns < 200&Round 1":"\"The Moonreach Fortress is pretty much the center of the Hertolfan forest, the hub of trade in this region.\nThe guild pays no little amount of gold to its adventurers who go out and protect citizens like me.\nAnd, I get to be paid when they buy my goods!\"", "b)Ask the traveler why he didn't join the Guild.|&Round 2^f@":"\"Well, uh, I'm not that brave of a guy, haha.\"", "g)Goodbye.|&Round 1":"", "g)Goodbye.|&Round 2":""})

dialogue2 = Dialogue(greeting={"Starter":"\"Anything you like?\"", "Turns > 50":"\"How you doing?\""}, goodbye={"Starter":"\"Thank you for your business!\"", "Turns > 50":"\"See you 'round!'\""}, metBefore=False, dialogueRounds={"i)Say that the food smells great.@|&Round 1":"\"Glad ya like it! Why don't you have a taste?\"", "c)Ask for his recipe.#@|Turns > 100&Round 1":"\"Haha, I'd be throwin' away my business if I told you!\"", "g)Goodbye.|&Round 1":""})

# dialogue3 = Dialogue(greeting={"Starter":""}, metBefore=False)

merchant1 = Merchant("Peddler Jonas", "The Roasting Spit", "As you approach the stand, you smell an intensely enticing aroma, as the smell of cooked meat lathered in sauce caresses your nostrils.", "Moonreach Guild", {"Roast Meat Skewer":8, "Roast Mushroom Skewer":5}, discounts=1, dialogue=dialogue2)

merchant2 = Merchant("Smith Barro", "The Hammer and Plate", "A sign with a black-headed hammer over a silver-colored chestplate hangs over a medium-sized shop, where banging sounds from within.", "Moonreach Guild", {"Leather Tunic":24, "Leather Pants":22, "Skull Cap":20, "Studded Leather Tunic":40, "Studded Leather Pants":36})

interact1 = Interactible("Dungeon Entrance", "You enter the cave, walking into the yawning, dirty, stone.", toTileID=-1)
interact2 = Interactible("Dungeon Entrance", "You exit the cave, as your eyes slowly adjust to the light of the outside.", toTileID=9)
interact3 = Interactible("Dialogue", "You approach another traveler entering the gates.", dialogue=dialogue1)
interact4 = Interactible("Merchant", "You approach the stalls.", merchants=(merchant1, merchant2))
interact5 = Interactible("Dialogue", "The demon raises his horned head, a chiseled face with a pair of darkened eyes looking at you in question, wordlessly asking for you to quickly go on and tell him what it was that troubled you so to enter the room." ) #dialogue=dialogue3
crafting1 = Interactible("Crafting", "You enter the house radiating of strange fumes, as you smell odd smells that fill the air of this house of hissing and puffing magical machinery.", craftingType="Alchemy")
resource1 = Interactible("Resource", "You attempt to capture one of the fish swimming in these waters.", tileID=7, lootTable={"Rolls":1, "Fresh Perch|Fishing|3":4, "Nothing":96}, gatherMod="Fishing")

moonreachQuestHall = Interactible("Quest Hall", "The Moonreach Quest Hall displays a wall of parchment papers that write a multitude of tasks open for you.")


class Tile:
  #Input nearbyTiles as a dictionary! Put in indices as "North," "South," "East," or "West." Use a string to use as text for a tile that isn't there.
  def __init__(self, flavorText, searchText, thisTileID, nearbyTiles, tileNotFoundText=(gold + "Area not made yet, sorry."), interactible=False, climbable=False, upTileID=0, downTileID=0, climbText="", climbFailText="", climbFailDamage=0, climbRequirement=0, encounter=False, encounterChance=0, findNoEncounterText="", repNoEncounterText="", noMoreMobsText="", entryEncounter=False, lootTable={}, statModifiers={}, questFlavorText={}, questSearchText={}, questEncounters={}, questEntryEncounter=False):
    self.thisTileID = thisTileID
    self.flavorText = flavorText
    self.nearbyTiles = nearbyTiles
    self.searchText = searchText
    self.tileNotFoundText = tileNotFoundText
    self.climbText = climbText
    self.climbFailText = climbFailText
    self.climbRequirement = climbRequirement
    self.climbFailDamage = climbFailDamage
    self.interactible = interactible
    self.lootTable = lootTable
    self.climbable = climbable
    self.upTileID = upTileID
    self.downTileID = downTileID
    self.encounter = encounter
    self.entryEncounter = entryEncounter
    self.encounterChance = encounterChance
    self.findNoEncounterText = findNoEncounterText
    self.repNoEncounterText = repNoEncounterText
    self.noMoreMobsText = noMoreMobsText
    self.statModifiers = statModifiers
    try:
      self.originalNothing = lootTable["Nothing"]
    except KeyError:
      self.originalNothing = 0
    self.questFlavorText = questFlavorText
    self.questSearchText = questSearchText
    self.questEncounters = questEncounters
    self.questEntryEncounter = questEntryEncounter


  def resetNothing(self):
    self.lootTable["Nothing"] = self.originalNothing
  def getReferenceName(self):
    if self.thisTileID > 0:
      return "Tile " + str(self.thisTileID)
    else:
      return "Dungeon Tile " + str(self.thisTileID - (2 * self.thisTileID))
  def getTileID(self):
    return self.thisTileID
  def getNearbyTiles(self):
    return self.nearbyTiles
  def getLoot(self):
    returnList = []
    listKeys = []
    listValues = []
    for key, value in self.lootTable.items():
      listKeys.append(key)
      listValues.append(value)
    del listKeys[0]
    del listValues [0]
    returnList = choices(listKeys, listValues, k=self.lootTable["Rolls"])
    return returnList
  def resetNothings(self):
    if self.lootTable["Nothing"] < 0:
      self.lootTable["Nothing"] = 0
  def getInteractible(self):
    return self.interactible
  def getTileNotFound(self):
    return self.tileNotFoundText
  def getFlavorText(self):
    return self.flavorText
  def getSearchText(self):
    return self.searchText
  def getLootTable(self):
    return self.lootTable
  def getClimbable(self):
    return self.climbable
  def getUpTile(self):
    return self.upTileID
  def getClimbFailDamage(self):
    return self.climbFailDamage
  def getDownTile(self):
    return self.downTileID
  def getEncounter(self):
    if type(self.encounter) == list:
      return choice(self.encounter)
    return self.encounter
  def setInteractible(self, value):
    self.interactible = value
  def getNoFindText(self):
    return self.findNoEncounterText
  def getNoRepText(self):
    return self.repNoEncounterText
  def getNoMoreMobsText(self):
    return self.noMoreMobsText
  def getStatModifiers(self):
    return self.statModifiers
  def getClimbText(self):
    return self.climbText
  def getClimbFailText(self):
    return self.climbFailText
  def getQuestEntryEncounter(self):
    return self.questEntryEncounter
  def getQuestFlavorText(self, questProgress):
    st = ""
    for key, value in self.questFlavorText.items():
      ph = key.split("|")
      if questProgress[ph[0]] == int(ph[1]):
        st += self.questFlavorText[key]
      st += "\n"
    st = st.strip()
    return st
  def getQuestSearchText(self, questProgress):
    st = ""
    for key, value in self.questSearchText.items():
      ph = key.split("|")
      if questProgress[ph[0]] == int(ph[1]):
        st += self.questSearchText[key]
      st += "\n"
    st = st.strip()
    return st

  def randomSetInteractible(self, weight):
    self.interactible = choices((True, False), (weight, 100-weight), k=1)[0]
    print(self.interactible)

  def resetInteractible(self):
    self.interactible = "Random"
    
  def encounterTest(self, tileMobs, reputation="None"):
    if reputation != "None":
      if self.encounter != False:
        if choices(("meet", "no meet"), (self.encounterChance, 100 - self.encounterChance)) == ["meet"] and tileMobs > 0 and reputation < self.encounter.getEncounterThreshold():
          return True
        else:
          return False
      else:
        return False
    else:
      
      if self.encounter != False:
        if choices(("meet", "no meet"), (self.encounterChance, 100 - self.encounterChance)) == ["meet"] and tileMobs > 0:
          return True
        else:
          return False
      else:
        return False
  
  def encounterOnEnter(self, mobAmount):
    if choices(("meet", "no meet"), (mobAmount, 100-mobAmount)) == ["meet"]:
      return True
    else:
      return False
  def setLootTableModifier(self, setModStat):
    #Subtrat mod from "nothing"
    self.lootTable["Nothing"] -= setModStat
    self.resetNothings()
    #Modifier set and finished.
    
  def checkClimb(self, modifierStat:int) -> bool:
    if choices(("success", "fail"), (modifierStat, self.climbRequirement)) == ["success"]:
      print(blue + self.climbText, reset)
      return True
    else:
      print(red + self.climbFailText, reset)
      return False
        
  def checkQuestEncounters(self, key:str, value:int) -> bool:
      for k, v in self.questEncounters.items():
          k = k.split("|")
          if k[0] == key and int(k[1]) == value and v[1] > 0:
              return True
      return False
    
  def isQuestEncounter(self, questProgress:dict) -> bool:
      success = [key for key, value in questProgress.items() if self.checkQuestEncounters(key, int(value))]
      if len(success) > 0:
          return True
      else:
          return False

  def getQuestEncounter(self, questProgress:dict):
      success = {key:value for key, value in questProgress.items() if self.checkQuestEncounters(key, int(value))}
      if len(success) == 0:
          return False
      k = list(success)[0] #First valid quest name
      return self.questEncounters[k + "|" + str(success[k])][0], k + "|" + str(success[k])
      # mob, and key
  def questEncounterWin(self, value:str) -> None:
      self.questEncounters[value][1] -= 1

  def getAmountEncounters(self, value:str) -> int:
      return self.questEncounters[value][1]
      
  

tile1 = Tile((reset + "You awaken in a forest of pines"), ("The trees stretch tall and thick, as piles of pine needles and small herbs cling to the ground."), 1, {"North":2, "South":5, "East":3, "West":4}, lootTable={"Rolls":1, "Pine Twig":1, "Nothing":30})

tile2 = Tile((reset + "A burbling brook sounds off ahead."), ("You spot the outline of a building off to the northwest."), 2, {"North":29, "South":1, "West":6, "East":7})

tile3 = Tile((reset + "A very large tree stands before you, its crown scraping the sky."), ("The tree rises, as clouds float through its needles."), 3, {"North":7, "South":30, "West":1}, lootTable={"Rolls":1,"Mushroom":1, "Nothing":35}) #Make this climbable eventually

tile4 = Tile((reset + "The trees give way to a dirt road cutting through the wilderness."), ("A serene road stretches through the forest, and off to the north, lies a fortress sitting atop a hill."), 4, {"North":6, "South":8, "East":1})

tile5 = Tile((reset + "The leaves wave in the wind. A damp draft curls around your feet."), ("You spot a cave, further down south, its entrance covered slightly by vegetation."), 5, {"North":1, "South":9, "East":30})

tile6 = Tile((reset + "A hill rises, a mound that rises slowly above the ground.\nAtop which lies a fortress of stone."), ("While climbing the hill, the clamor of those within the fortress grows louder and louder."), 6, {"North":10, "South":4, "East":2})

tile7 = Tile((reset + "A river rushes before you, running through the forest, over gathered stones and rarely interrupted by a small form darting through its waters."), ("You spot fish swimming in these shallows."), 7, {"South":3, "West":2}, interactible=resource1)

tile8 = Tile((reset + "The trees come very close to the well-travelled road.\nRoots frame the sides of the road, branches towering over a road that flashes of points of light dancing as the shadows of pine needles move."), ("You spot a curve in the road as it goes south, where it turns to the east."), 8, {"North":4, "West":9, "South":28})

tile9 = Tile((reset + "A yawning cave opening is before you, as small sticks are strewn about.its entrance."), ("The ground is damp, the dirt cool and watered."), 9, {"North":5, "South":37, "East":33, "West":28}, interactible=interact1, repNoEncounterText=("The animals reluctantly welcome your presence in their homes."),findNoEncounterText=("You feel like you are being watched by a few creatures nearby."),noMoreMobsText=(reset +"All that's left here, are the stones that line the entrance, and the trees around it.\nIt's quite quiet here."), encounter=mobDict["Hungry Wolf"], encounterChance=20)

tile10 = Tile((reset + "You arrive at the gates of the fortress, guarded by armored humans hefting long, crescent-tipped pikes.\nAll the while, a rare person walks down the path to enter the fortress."), ("The guards look at you strangely as you search around the hill before the fortress gates.\nThis fortress was certainly a structure built for war, as you spot intricate, durable, masonry,\n with the little telltale holes of arrow slits by the sides of the gateway, a heavy iron gate raised above this vaunted corridor."), 10, {"North":11,"South":6}, tileNotFoundText=(gold + "There's no point in trying to walk through walls."), interactible="Random", entryEncounter=True, encounterChance=100)

tile11 = Tile((reset + "A large courtyard, bustling with people moving every which way around the fortress-city on the hill."), "On the road further north, you spot a sloping street leading upward to a grand keep, of beautifully stained windows and stonework, flying purple and white banners of the guild, depicting a crescent moon.", 11, {"North":13, "South":10, "East":14, "West":12})

tile12 = Tile((reset + "You find a long, stretching, road, its cobblestones obscured by the encroaching stands of merchants, and the clamor of the citizens."), ("Warrens of alleyways and buildings make up the land around these shops, and in this hill fortress."), 12, {"North":17, "South":15, "East":11, "West":16}, interactible=interact4)

tile13 = Tile((reset + "The northern road leads to the main guildhall, where stone gargoyles stare downward over two massive wooden doors."), ("You spot that various colorful depictions of the adventurers of old are painted into the stained glass."), 13, {"North":18, "South":11, "West":17}, tileNotFoundText=(gold + "The walls of the arena do not present an entrance for you to go through."))

tile14 = Tile((reset + "The eastern road leads to a massive circular stone building, the walls of this edifice engraved with depictions of battle."), ("You see that this place is called the Arena, where glorious battle could be done between you and other powerful opponents, without any risk of death."), 14, {"North":19, "West":11}, tileNotFoundText=(gold + "You find that you cannot walk through the walls of houses."))

tile15 = Tile((reset + "There is a large tower here, that stands tall and flies the banners of the Moonreach Guild."), "The tower's doors are locked.", 15, {"North":12}, tileNotFoundText="It doesn't seem like the other buildings here are for you to intrude upon.")

tile16 = Tile((reset + "Further down the market road, there lies a collection of buildings that house open facilities for crafters."), ("Two such buildings stand here, a forge radiating of heat and an apothecary smelling of magical fumes."), 16, {"East":12}, tileNotFoundText="It doesn't seem like the other buildings here are for you to intrude upon.", interactible=crafting1)

tile17 = Tile((reset + "North of the market road, lies a group of shops more lavish than those south of them, having their own buildings to themselves."), ("Each of these buildings caters to the richer sort of adventurer."), 17, {"South":12, "East":13}, tileNotFoundText="It doesn't seem like the other buildings here are for you to intrude upon.")

tile18 = Tile((reset + "The main keep of the fortress is right before you, a pair of stone gargoyles grinning over the heads of a pair of heavily-armored guardsmen."), ("The heavy wooden doors open wide into a long, vaunted, hall, a carpet of scarlet red stretching and branching off into the cathedral-like interior of the castle keep."), 18, {"North":20, "South":13})

tile19 = Tile((reset + "Even the arena's entrance gate is a grand sight, as effigies of past champions stand vigil in poses of victory, as plaques detail their exploits."), ("You read the plaques: \nHaerclus Asmitheus, the Lord of Hunger, who ate his opponents alive when they failed.\nRevei Kroni, the Red Baron, who crushed his enemies with his unwavering will.\nGarth Karnis, the Champion of Steel, who had never been injured in a single match.\nEir Goromir, the Bone-Crusher, who turned his enemies to dust under his hammer larger than boulders.\nBead Tyrhall, the Ash Harpy, who burnt her enemies to piles of ash.\nGiorkkos, the Cloudy Day, who slew a full arena of fighters with a single spell."), 19, {"South":14}, tileNotFoundText=(gold + "You don't find it a good idea to walk over open air, not knowing how to fly.")) #Add the Arena interactible here. May have an arena shop merchant who has random stuff in their sell dictionary.

tile20 = Tile((reset + "The grand chamber of the main guild-hall branches off into many rooms through halls on its eastern and western walls."), ("Painted murals of past victories, of adventurer-heroes of old who slew grotesque monsters are depicted hanging on the walls."), 20, {"North":24, "South":18, "East":21, "West":23})

tile21 = Tile((reset + "Past a statue of a winged man, lies a large hall,\nwith a floor of stone tiling leading up to a room lit to display a wall with papers tacked all over its surface."), ("You spot that the tiles on the floor are inscribed with the names of all those who had fallen, and died during their quests."), 21, {"West":20, "East":22}, tileNotFoundText=(gold + "The walls are in your way."), interactible=moonreachQuestHall) #Quest Hall interactible

tile22 = Tile((reset + "A desk with a brightly-smiling woman that greets all who enter the hall lies before you."), ("A stack of parchment and an feather pen and inkwell are placed upon the table."), 22, {"West":21}, tileNotFoundText=(gold + "The walls are in your way."))

tile23 = Tile((reset + "Past a statue of a thin, reedy, man in a businesslike suit, lies an open common plaza, with doorways opening off to numerous personal residences."), ("You spot a perfect model of a mirror-like lake at the bottom of a group of rocky crags."), 23, {"East":20}, tileNotFoundText=(gold + "These other residences are not for you to intrude upon."))

tile24 = Tile((reset + "The hall stretches for quite the long way, the vaunted ceiling draped with the purple and silver colors of the Moonreach Guild, a grand and ornate site to display awe upon the visitor."), ("You spot an ornate door leading off to a kingly chamber past the end of this great hall."), 24, {"North":27, "South":20, "East":25, "West":26})

tile25 = Tile((reset + "Past a statue of a lady with three eyes, lies a pair of closed doors, where beyond lies a room of absolute quiet."), ("Stacks of books that stretch and span the room, an interior lit by spiraling magic circles that fly in the sky, as a serene room of study spans outward around you."), 25, {"West":24}, tileNotFoundText=(gold + "The walls of books and shelves lead you round and round, till you return right where you began.")) #Library interactible.

tile26 = Tile((reset + "An empty-ceiling room lies here, a single man dressed in loose robes standing in its center. He seems to be engrossed in a series of artful strikes against an invisible opponent."), ("The room opens into the clear sky above, sunny light shining down on fluffy clouds that float through the towers of the guild hall roof."), 26, {"West":24}) #Yin Nagata NPC, may challenge player.

tile27 = Tile((reset + "Past a statue of a spear-wielding lady with a prideful smile, lies a spacious office, with a horned Demon and his assistant working together, poring over stacks upon stacks of parchment laid across their beautifully carved wooden table."), ("There lie a multitude of tapestries and varied trophies hanging on the walls and meticulously shelved, ever-more displaying this guild as that of hunters, hunters who hunted the big game of the wild."), 27, {"South":24}, tileNotFoundText=(gold + "You cannot find yourself walking through the walls of this office."), interactible=False) #Guildmaster Chrys NPC

tile28 = Tile((reset + "The road, stretching far from the north to the south, carved by the passage of foot and wagon, over many years of traveling."), ("Being further from civilization, this segment of the road is significantly more overgrown with weeds than that of the north."), 28, {"North":8, "South":36, "East":9, "West":34}, questFlavorText={"Bandits|1":(reset + "You come upon a wrecked wagon, with its drawing oxen slain with arrows in their eyes, and a wagon wheel crushed against the dirt."), "Bandits|2":(reset + "You come upon a wrecked wagon, with its drawing oxen slain with arrows in their eyes, and a wagon wheel crushed against the dirt.")}, questSearchText={"Bandits|2":(reset + "It's clear what happened here. The caravan was ambushed, with human tracks of at least three men that lead off into the west.")})

tile29 = Tile((reset + "Water runs over smoothened river stones, clear water reflecting the light of day in your eyes, as moss covered stones wall its sides in verdant green."), ("You spot a wooden bridge going over the stream, crossing the water and crafted of logs tied by water-soaked rope."), 29, {"South":2}) #Tilenotfound should be being blocked by fortress walls.

tile30 = Tile((reset + "A fallen log lies here, the bough of an elder tree long dead, overgrown with smaller plants and mushrooms hidden beneath."), ("You spot a rabbit hole nearly hidden beneath the rotting log."), 30, {"North":3, "South":33, "East":31, "West":5})

tile31 = Tile((reset + "Moss creeps over the bark of these trees, forming a layer of green over thick trunks as wide as two men."), ("Creeping vines flowering with small yellow blooms drape over the mosses."), 31, {"West":30, "South":32}, findNoEncounterText=("You feel like you are being stalked amongst these trees, only seeing faint shifts in the dry needles over the ground."), repNoEncounterText=("The gaze from within these trees is neutral, perhaps even friendly, as Nature welcomes you in its wild lands."), noMoreMobsText=("Light breezes flow through the trees, carrying faint birdsong from further lands."), encounter=mobDict["Forest Wolf"], encounterChance=16)

tile32 = Tile((reset + "The forest's floor is covered with encroaching smaller plants that cover the soil between the trees, while a forest trail stretches from the west to the east."), ("You see that these plants are constructed of little fronds, who hold small leaves growing upon them, where occasionally, you spot tiny sacs beneath a leaflet."), 32, {"North":31, "West":33}, lootTable={"Rolls":1, "Northern Fern Spore-Sac":25, "Nothing":75})

tile33 = Tile((reset + "The dirt rises into a hill to the west, as more uneven ground breaks into the forest, the dirt now filled with myriad small chips of rock."), ("Among these shards of stone that lie on the forest floor, you spot a shattered half of a weathered boulder, half of its form cleaved away, revealing a grievous wound in a once large rock."), 33, {"North":30, "West":9, "East":32})

tile34 = Tile((reset + "Deeper into the forest, you spot the branches close together, as pine fronds intersect each other, each seeking for, and turning the sun's rays into thin points of light on the dirt."), ("Life seems to be flourishing, in the places shaded by tree leaves, as small plants with purple sickle-shaped leaves growing amongs knotted roots."), 34, {"South":35, "East":28}, questFlavorText={"Bandits|2":(reset + "Bloodied tracks lead down to the south. You feel that your quarry is close, perhaps even watching you, already."), "Bandits|3":(reset + "Bloodied tracks lead down to the south. You feel that your quarry is close, perhaps even watching you, already.")}, questSearchText={"Bandits|3":(reset + "An acrid smell fills the air, the smell of overcooked, charred, meat.")})

tile35 = Tile((reset + "A small clearing lies here, where there once was a great tree that stretched into the skies, now reduced to a behemoth moss-grown table of circle-marked wood."), ("Small yellow flowers dot the green carpeting over the ground, as the clear blue skies show above in the sky, opening a window of sunlight into the clearing guarded by brown-clad sentries."), 35, {"North":34, "East":36}, questFlavorText={"Bandits|3":(reset + "You enter a small clearing in the forest, where a bandit camp lies, tents placed in the forest, the remnants of a burnt-out campfire, and the laughing of cruel men.")}, questEncounters={"Bandits|3":[[mobDict["Forest Bandit 1"], mobDict["Forest Bandit 2"]], 8], "Bandits|4":mobDict["Bandit Leader Toderick"]}, questEntryEncounter=True)

tile36 = Tile((reset + "The road cuts a line through the forest, as if defying the wild sanctity of nature with its presence."), ("You see twisted boughs, elder bark, and a sense of permanence, and beings born of a long-past era, around you. These knotted trees seem to be thick enough for you to climb."), 36, {"North":28, "East":37, "West":35}, lootTable={"Rolls":1, "Mushroom":15, "Nothing":75})

tile37 = Tile((reset + "The ground is carpeted with yellowed pine needles, as light shines down through the bare branches of a dying tree."), ("Between the fallen needles, you spot the tracks of many animals. It seems this clearing has been the home of many."), 37, {"North":9, "West":36}, encounter=mobDict["Forest Fox"], encounterChance=15, findNoEncounterText="While the animals of the forest once were in these lands, they don't seem to show themselves to their visitor.", repNoEncounterText="A small family of foxes stare at you from next to a tree trunk. While they still are wary of you, they do not flee.")

dungeonTile1 = Tile((reset + "The interior is cool, as your feet tap against the stone of the floor."), ("Light still comes from the entrance, as greenery shows beyond the cool, dark, cave.\nYou notice that the tunnels branch into two directions."), -1, {"East":-2}, tileNotFoundText=(gold + "You bump into a stone wall in the darkness."), interactible=interact2, repNoEncounterText=("The hungry wolves decide not to attack you for food, though have none to spare for you."), findNoEncounterText=("Faint shapes flicker through the shadows, as light snarls caress the very edges of your hearing."), noMoreMobsText=("The cave has fallen silent, leaving only dimly-lit rocks glistening of moisture."), encounter=mobDict["Hungry Wolf"], encounterChance=20)

dungeonTile2 = Tile((reset + "The cave is filled with stones, and your feet splash in small puddles of water."), ("The cave bends, turning away out of your vision."), -2, {"West":-1, "East":-3}, tileNotFoundText=(gold + "You bump into a stone wall in the darkness."), repNoEncounterText=(reset + "The wolves recognize your scent, and your place as a friend of nature."), findNoEncounterText=(reset + "Eyes are upon you, their gazes not friendly at all, filled with hunger."), noMoreMobsText=(reset + "The dim tunnel seems empty now."), encounter=mobDict["Hungry Wolf"], encounterChance=25, lootTable={"Rolls":1,"Quartz Stone":1, "Nothing":49})

dungeonTile3 = Tile((reset + "A cramped tunnel framed by collapsed stones leads ever deeper here."), ("The darkness makes everything difficult to make out.\nThere is barely any light to speak of, aside from the shining of magical fungi clinging to the cave walls."), -3, {"West":-2, "East":-4}, tileNotFoundText=(gold + "You bump into a stone wall in the darkness."), 
findNoEncounterText="You sense what seems to be a presence in this darkness,\nof creatures that inhabit the underground that don't seem so welcoming to their visitor.", repNoEncounterText="The unfriendly gazes don't hold so much malice any more.", noMoreMobsText="This place has been deserted, as even the faint noises on the corner of your hearing disappeared.", encounter=mobDict["Kobold Scout"], encounterChance=15)

dungeonTile4 = Tile((reset + "You are in a large cavern, with a steep drop away from the cave opening a little bit higher than your current position. It's lit by small growths of shining crystal and mushrooms."), ("You spot that there are several stones that look climbable, near the place from whence you came."), -4, {"South":-5}, climbable=True, upTileID=-3, climbText="You manage to clamber you way up the stones, escaping into the darkened passage above.", climbFailText="Your hands have difficulty grasping on these stones in the darkness, and you slip back down.", climbFailDamage=2, encounter=mobDict["Cave Shrieker"], encounterChance=10, findNoEncounterText="The mushrooms glow serenely on the walls. Underground vegetation is certainly far different from that of the surface.", noMoreMobsText="The place could even be described as peaceful.", entryEncounter=True, lootTable={"Rolls":1,"Quartz Stone":1, "Nothing":49})

dungeonTile5 = Tile((reset + "Most of the cave's inhabitants appear to be quite shy of your intrusion, making themselves scarce whenever you come near."), ("A patch of glowing mushrooms grows by the side of a pool of water, filled by the steady drip of water dropping from the ceiling."), -5, {"North":-4}, encounter=mobDict["Cave Crawler"], encounterChance=8, findNoEncounterText="You hear the lumbering of large creatures in the darkness. Who knew that things in a cave like this could grow to such sizes?", noMoreMobsText="It's a serene environment indeed, as the rhythmic plip, plop, of water droplets sounds in your ears, a rhythmic, slow, noise.")

tilesDict = {1:tile1, 2:tile2, 3:tile3, 4:tile4, 5:tile5, 6:tile6, 7:tile7, 8:tile8, 9:tile9, 10:tile10, 11:tile11, 12:tile12, 13:tile13, 14:tile14, 15:tile15, 16:tile16, 17:tile17, 18:tile18, 19:tile19, 20:tile20, 21:tile21, 22:tile22, 23:tile23, 24:tile24, 25:tile25, 26:tile26, 27:tile27, 28:tile28, 29:tile29, 30:tile30, 31:tile31, 32:tile32, 33:tile33, 34:tile34, 35:tile35, 36:tile36, 37:tile37, -1:dungeonTile1, -2:dungeonTile2, -3:dungeonTile3, -4:dungeonTile4, -5:dungeonTile5}

interactionDict = {9:interact1, -1:interact2, 7:resource1, 10:interact3, 12:interact4, 16:crafting1, 21:moonreachQuestHall, 27:interact5}
