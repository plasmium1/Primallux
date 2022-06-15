from ansi.colour.rgb import rgb256
from ansi.colour.fx import reset
from random import choices, choice
import monsters
from playerInventory import identifierDict
from monsters import hungryWolf, koboldScout, caveShrieker, caveCrawler
#Use this later for handling the tile if statements?
black = "\u001b[30m"
red = "\u001b[31m"
green = rgb256(0x00, 0xff, 0x09)
yellow = "\u001b[93m"
orange = rgb256(0xff, 0x73, 0x00)
gold = rgb256(0xe6, 0xcb, 0x02)
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
      print(str(identifierDict[key]) + blue + " Cost: " + gold + str(value))
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
      return self.dialogueRounds[key]
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
  def getSelling(self):
    return self.selling
  def getBuying(self):
    return self.buying
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

dialogue1 = Dialogue(greeting={"Starter":"\"Hail the Moons!\"", "Turns < 200":"\"You new here?\"", "Turns > 200":"\"I'm glad to see you again!\"", "Turns > 700":"\"Ah, it's you again. How long has it been, this time?\""}, goodbye={"Starter":"\"I wish you luck on your journey!\""}, metBefore=False, dialogueRounds={"f)Ask about the fortress.|Turns < 200&Round 1":"\"The Moonreach Fortress is pretty much the center of the Hertolfan forest, the hub of trade in this region.\nThe guild pays no little amount of gold to its adventurers who go out and protect citizens like me.\nAnd, I get to be paid when they buy my goods!\"", "b)Ask the traveler why he didn't join the Guild.|&Round 2^f@":"\"Well, uh, I'm not that brave of a guy, haha.\"", "g)Goodbye.|&Round 1":""})

dialogue2 = Dialogue(greeting={"Starter":"\"Anything you'd like to eat?\"", "Turns > 50":"\"Good, yeah?\""}, goodbye={"Starter":"\"Thank you for your business!\""})

merchant1 = Merchant("Peddler Jonas", "The Roasting Spit", "As you approach the stand, you smell an intensely enticing aroma, as the smell of cooked meat lathered in sauce caresses your nostrils.", "Moonreach Guild", {"Roast Rabbit":4}, discounts=1, dialogue=dialogue2)

merchant2 = Merchant("Armorsmith Barro", "The Hammer and Plate", "A sign with a black-headed hammer over a silver-colored chestplate hangs over a medium-sized shop, where banging sounds from within.", "Moonreach Guild", {"Plated Leather Jerkin":16})

interact1 = Interactible("Dungeon Entrance", "You enter the cave, walking into the yawning, dirty, stone.", toTileID=-1)
interact2 = Interactible("Dungeon Entrance", "You exit the cave, as your eyes slowly adjust to the light of the outside.", toTileID=9)
interact3 = Interactible("Dialogue", "You approach one of the other travelers entering the gates.", dialogue=dialogue1)
interact4 = Interactible("Merchant", "You approach the stalls.", merchants=(merchant1, merchant2))
crafting1 = Interactible("Crafting", "You enter the house radiating of strange fumes, as you smell odd smells that fill the air of this house of hissing and puffing magical machinery.", craftingType="Alchemy")
resource1 = Interactible("Resource", "You attempt to capture one of the fish swimming in these waters.", tileID=7, lootTable={"Rolls":1, "Fresh Perch":4, "Nothing":96}, gatherMod="Fishing")
interactionDict = {9:interact1, -1:interact2, 7:resource1, 10:interact3, 12:interact4, 16:crafting1}

class Tile:
  #Input nearbyTiles as a dictionary! Put in indices as "North," "South," "East," or "West." Use a string to use as text for a tile that isn't there.
  def __init__(self, flavorText, searchText, thisTileID, nearbyTiles, tileNotFoundText=(gold + "Area not made yet, sorry."), interactible=False, climbable=False, upTileID=0, downTileID=0, climbText="", climbFailText="", climbFailDamage=0, climbRequirement=0, encounter=False, encounterChance=0, findNoEncounterText="", repNoEncounterText="", noMoreMobsText="", entryEncounter=False, lootTable={}, statModifiers={}, questFlavorText={}, questSearchText={}):
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

  def randomSetInteractible(self, weight):
    self.interactible = choices((True, False), (weight, 100-weight), k=1)[0]

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
    
  def checkClimb(self, modifierStat):
    if choices(("success", "fail"), (modifierStat, self.climbRequirement)) == ["success"]:
      print(blue + self.climbText, reset)
      return True
    else:
      print(red + self.climbFailText, reset)
      return False

tile1 = Tile((reset + "You awaken in a forest of pines"), (reset + "The trees stretch tall and thick, as piles of pine needles and small herbs cling to the ground."), 1, {"North":2, "South":5, "East":3, "West":4}, lootTable={"Rolls":1, "Pine Twig":1, "Nothing":30})

tile2 = Tile((reset + "A burbling brook sounds off ahead."), (reset + "You spot the outline of a building off to the northwest."), 2, {"South":1, "West":6, "East":7})

tile3 = Tile((reset + "A very large tree stands before you, its crown scraping the sky."), (reset + "The tree rises, as clouds float through its needles."), 3, {"North":7, "West":1}, lootTable={"Rolls":1,"Mushroom":1, "Nothing":35}) #Make this climbable eventually

tile4 = Tile((reset + "The trees give way to a dirt road cutting through the wilderness."), ("A serene road stretches through the forest, as off to the north, lies a fortress sitting atop a hill."), 4, {"North":6, "South":8, "East":1})

tile5 = Tile((reset + "The leaves wave in the wind. A damp draft curls around your feet."), (reset + "You spot a cave, further down south, its entrance covered slightly by vegetation."), 5, {"North":1, "South":9})

tile6 = Tile((reset + "A hill rises, a mound that rises slowly above the ground.\nAtop which lies a fortress of stone."), (reset + "While climbing the hill, the clamor of those within the fortress grows louder and louder."), 6, {"North":10, "South":4, "East":2})

tile7 = Tile((reset + "A river rushes before you, running through the forest."), ("You spot fish swimming in these shallows"), 7, {"South":3, "West":2}, interactible=True)

tile8 = Tile((reset + "The trees come very close to the well-travelled road.\nRoots frame the sides of the road, branches towering over a road that flashes of points of light dancing as the shadows of pine needles move."), (reset + "You spot a curve in the road as it goes south, where it turns to the west."), 8, {"North":4, "East":9})

tile9 = Tile((reset + "A yawning cave opening is before you, as small sticks are strewn about.its entrance."), (reset + "The ground is damp, the dirt cool and watered."), 9, {"North":5, "West":8}, interactible=True, repNoEncounterText=("The animals reluctantly welcome your presence in their homes."),findNoEncounterText=("You feel like you are being watched by a few creatures nearby."),noMoreMobsText=(reset +"All that's left here, are the stones that line the entrance, and the trees around it.\nIt's quite quiet here."), encounter=hungryWolf, encounterChance=20)

tile10 = Tile((reset + "You arrive at the gates of the fortress, guarded by armored humans hefting long, crescent-tipped pikes.\nAll the while, a rare person walks down the path to enter the fortress."), (reset + "The guards look at you strangely as you search around the hill before the fortress gates.\nThis fortress was certainly a structure built for war, as you spot intricate, durable, masonry,\n with the little telltale holes of arrow slits by the sides of the gateway, a heavy iron gate raised above this vaunted corridor."), 10, {"North":11,"South":6}, tileNotFoundText=(gold + "There's no point in trying to walk through walls."), interactible="Random", entryEncounter=True, encounterChance=100)

tile11 = Tile((reset + "A large courtyard, bustling with people moving every which way around the fortress-city on the hill."), "On the road further north, you spot a sloping street leading upward to a grand keep, of beautifully stained windows and stonework, flying purple and white banners of the guild, depicting a crescent moon.", 11, {"North":13, "South":10, "East":14, "West":12})

tile12 = Tile((reset + "You find a long, stretching, road, its cobblestones obscured by the encroaching stands of merchants, and the clamor of the citizens."), ("Warrens of alleyways and buildings make up the land around these shops, and in this hill fortress."), 12, {"North":17, "South":15, "East":11, "West":16}, interactible=True)

tile13 = Tile((reset + "The northern road leads to the main guildhall, where stone gargoyles stare downward over two massive wooden doors."), ("You spot that various colorful depictions of the adventurers of old are painted into the stained glass."), 13, {"North":18, "South":11, "West":17}, tileNotFoundText=(gold + "The walls of the arena do not present an entrance for you to go through."))

tile14 = Tile((reset + "The eastern road leads to a massive circular stone building, the walls of this edifice engraved with depictions of battle."), ("You see that this place is called the Arena, where glorious battle could be done between you and other powerful opponents, without any risk of death."), 14, {"North":19, "West":11})

tile15 = Tile((reset + "There is a large tower here, that stands tall and flies the banners of the Moonreach Guild."), "The tower's doors are locked.", 15, {"North":12}, tileNotFoundText="It doesn't seem like the other buildings here are for you to intrude upon.")

tile16 = Tile((reset + "Further down the market road, there lies a collection of buildings that house open facilities for crafters."), ("Two such buildings stand here, a forge radiating of heat and an apothecary smelling of magical fumes."), 16, {"East":12}, tileNotFoundText="It doesn't seem like the other buildings here are for you to intrude upon.", interactible=crafting1)

tile17 = Tile((reset + "North of the market road, lies a group of shops more lavish than those south of them, having their own buildings to themselves."), (reset + "Each of these buildings caters to the richer sort of adventurer."), 17, {"South":12, "East":13}, tileNotFoundText="It doesn't seem like the other buildings here are for you to intrude upon.")

tile18 = Tile((reset + "The main keep of the fortress is right before you, a pair of stone gargoyles grinning over the heads of a pair of heavily-armored guardsmen."), (reset + "The heavy wooden doors open wide into a long, vaunted, hall, a carpet of scarlet red stretching and branching off into the cathedral-like interior of the castle keep."), 18, {"North":20, "South":13})

tile19 = Tile((reset + "Even the arena's entrance gate is a grand sight, as effigies of past champions stand vigil in poses of victory, as plaques detail their exploits."), (reset + "You read the plaques: \nHaerclus Asmitheus, the Lord of Hunger, who ate his opponents alive when they failed.\nRevei Kroni, the Red Baron, who crushed his enemies with his unwavering will.\nGarth Karnis, the Champion of Steel, who had never been injured in a single match.\nEir Goromir, the Bone-Crusher, who turned his enemies to dust under his hammer larger than boulders.\nBead Tyrhall, the Ash Harpy, who burnt her enemies to piles of ash.\nGiorkkos, the Cloudy Day, who slew a full arena of fighters with a single spell."), 19, {"North":20, "South":14}, tileNotFoundText=(gold + "You don't find it a good idea to walk over open air, not knowing how to fly.")) #Add the Arena interactible here. May have an arena shop merchant who has random stuff in their sell dictionary.

tile20 = Tile((reset + "The grand chamber of the main guild-hall branches off into many rooms through halls on its eastern and western walls."), (reset + "Painted murals of past victories, of adventurer-heroes of the old who slew grotesque monsters are depicted hanging on the walls."), 20, {"South":18})

dungeonTile1 = Tile((reset + "The interior is cool, as your feet tap against the stone of the floor."), (reset + "Light still comes from the entrance, as greenery shows beyond the cool, dark, cave.\nYou notice that the tunnels branch into two directions."), -1, {"East":-2}, tileNotFoundText=(gold + "You bump into a stone wall in the darkness."), interactible=True, repNoEncounterText=("The hungry wolves decide not to attack you for food, though have none to spare for you."), findNoEncounterText=("Faint shapes flicker through the shadows, as light snarls caress the very edges of your hearing."), noMoreMobsText=("The cave has fallen silent, leaving only dimly-lit rocks glistening of moisture."), encounter=hungryWolf, encounterChance=20)

dungeonTile2 = Tile((reset + "The cave is filled with stones, and your feet splash in small puddles of water."), (reset + "The cave bends, turning away out of your vision."), -2, {"West":-1, "East":-3}, tileNotFoundText=(gold + "You bump into a stone wall in the darkness."), repNoEncounterText=(reset + "The wolves recognize your scent, and your place as a friend of nature."), findNoEncounterText=(reset + "Eyes are upon you, their gazes not friendly at all, filled with hunger."), noMoreMobsText=(reset + "The dim tunnel seems empty now."), encounter=hungryWolf, encounterChance=25, lootTable={"Rolls":1,"Quartz Stone":1, "Nothing":49})

dungeonTile3 = Tile((reset + "A cramped tunnel framed by collapsed stones leads ever deeper here."), (reset + "The darkness makes everything difficult to make out.\nThere is barely any light to speak of, aside from the shining of magical fungi clinging to the cave walls."), -3, {"West":-2, "East":-4}, tileNotFoundText=(gold + "You bump into a stone wall in the darkness."), 
findNoEncounterText="You sense what seems to be a presence in this darkness,\nof creatures that inhabit the underground that don't seem so welcoming to their visitor.", repNoEncounterText="The unfriendly gazes don't hold so much malice any more.", noMoreMobsText="This place has been deserted, as even the faint noises on the corner of your hearing disappeared.", encounter=koboldScout, encounterChance=15)

dungeonTile4 = Tile((reset + "You are in a large cavern, with a steep drop away from the cave opening a little bit higher than your current position. It's lit by small growths of shining crystal and mushrooms."), (reset + "You spot that there are several stones that look climbable, near the place from whence you came."), -4, {"South":-5}, climbable=True, upTileID=-3, climbText="You manage to clamber you way up the stones, escaping into the darkened passage above.", climbFailText="Your hands have difficulty grasping on these stones in the darkness, and you slip back down.", climbFailDamage=2, encounter=caveShrieker, encounterChance=10, findNoEncounterText="The mushrooms glow serenely on the walls. Underground vegetation is certainly far different from that of the surface.", noMoreMobsText="The place could even be described as peaceful.", entryEncounter=True, lootTable={"Rolls":1,"Quartz Stone":1, "Nothing":49})

dungeonTile5 = Tile((reset + "Most of the cave's inhabitants appear to be quite shy of your intrusion, making themselves scarce whenever you come near."), (reset + "A patch of glowing mushrooms grows by the side of a pool of water, filled by the steady drip of water dropping from the ceiling."), -5, {"North":-4}, encounter=caveCrawler, encounterChance=8, findNoEncounterText="You hear the lumbering of large creatures in the darkness. Who knew that things in a cave like this could grow to such sizes?", noMoreMobsText="It's a serene environment indeed, as the rhythmic plip, plop, of water droplets sounds in your ears, a rhythmic, slow, noise.")

tilesDict = {1:tile1, 2:tile2, 3:tile3, 4:tile4, 5:tile5, 6:tile6, 7:tile7, 8:tile8, 9:tile9, 10:tile10, 11:tile11, 12:tile12, 13:tile13, 14:tile14, 15:tile15, 16:tile16, 17:tile17, 18:tile18, 19:tile19, 20:tile20, -1:dungeonTile1, -2:dungeonTile2, -3:dungeonTile3, -4:dungeonTile4, -5:dungeonTile5}