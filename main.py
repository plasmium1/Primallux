import playerInventory
import monsters
#from replit import db
from random import randint, choices
from ansi.colour import fg
from ansi.colour.rgb import rgb256
from ansi.colour.fx import reset


black = "\u001b[30m"
red = "\u001b[31m"
green = rgb256(0x00, 0xff, 0x09)
orange = rgb256(0xfc, 0x94, 0x03)
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

tilesetLegals = ("h", "help", "look", "l", "search", "north", "south", "east", "west", "n", "s", "e", "w", "wander", "inv", "inventory", "magic", "m", "int", "interact", "stats") #Public tuple for allowing checkIn to check the right values for each tile


#Declare and initialize items based on IDs
pineTwig = playerInventory.EquipmentItem("Weapon","Pine Twig", 0, {"Item Damage":5})
wolfFang = playerInventory.EquipmentItem("Weapon", "Wolf Fang", 0, {"Item Damage":randint(5,8)})
wolfPelt = playerInventory.InvItem("Misc", "Wolf Pelt", 0)
hungryWolf = monsters.mob("Hungry Wolf", 28, 3, 8, 1, 0, 4, "A ragged wolf appears out of the trees, drool slavering from its jaws.", "It growls in hunger. Perhaps prey has been hard to find these days.", "The wolf collapses, finally succumbing to its wounds and starvation.", "The wolf snarls, and moves back in to counterattack.", "The wolf growls, but leaves you alone to find someone else.", 3, lootTable={"Rolls":1, "Wolf Fang":15, "Nothing":70, "Wolf Pelt":15})
mushroom = playerInventory.ConsumableItem("Mushroom", 0, {"Current HP":15})

identifierDict = {"Pine Twig":pineTwig, "Wolf Fang":wolfFang, "Wolf Pelt":wolfPelt, "Mushroom":mushroom}
#Stores IDs for items, keyed to their names


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
  print(cyan + name + ", Level " + str(stats["Level"]) + " " + gender + " " + race + ":")
  print(fg.blue("Strength: ") + green + str(stats["Strength"]))
  print(fg.blue("  Damage range (") + gold + "S-[melee-item]" + fg.blue("):"), fg.red, (stats["Strength"]), "-",
        (stats["Strength"] + sub_stats["Item Damage"]))
  sub_stats["Damage-Lower"] = stats["Strength"]
  sub_stats["Damage-Upper"] = stats["Strength"] + sub_stats["Item Damage"]
  print(fg.blue("Constitution: ") + green,  stats["Constitution"])
  print(fg.blue("  Base health pool (") + gold +"C" + fg.blue("): ") + green + str(sub_stats["Max HP"]) + " points")
  sub_stats["Max HP"] = stats["Constitution"] * 10
  sub_stats["Current HP"] = sub_stats["Max HP"]
  print(fg.blue + "Perception: " + green + str(stats["Perception"]))
  print(fg.blue + "Dexterity: " + green + str(stats["Dexterity"]))
  print(fg.blue("  Crit Chance (") + gold +"P-D" + fg.blue("): ") + green +
        str(round((0.1* stats["Dexterity"] * (stats["Perception"]) * 0.01) + 1, 2)) + "%")
  sub_stats["Crit Chance"] = round((0.1 * stats["Dexterity"] * (stats["Perception"]) * 0.01) + 1, 2)
  print(fg.blue + "Charisma: " + green + str(stats["Charisma"]))
  print(fg.blue + "Intelligence: " + green + str(stats["Intelligence"]))
  print(fg.blue("  Learn Chance Bonus (") + gold + "I-W" + fg.blue("): ") + green + str(round((stats["Intelligence"]*0.1) * (stats["Wisdom"] * 0.01) + 1, 2)) + "%")
  sub_stats["Learn Chance"] = round((stats["Intelligence"]*0.1) * (stats["Wisdom"] * 0.01) + 1, 2)
  sub_stats["Max MP"] = stats["Wisdom"] * 5
  sub_stats["Current MP"] = sub_stats["Max MP"]
  print(fg.blue + "Wisdom: " + green, stats["Wisdom"], reset)
  print(blue + "  Base mana pool (" + gold + "W" + blue + "): " + light_purple + str(sub_stats["Current MP"]) + "/" + str(sub_stats["Max MP"]))
  save = checkIn(("y", "n"), "str", (cyan + "Save character?" + blue + " (Y/N) "))
  #Needs a save data function probably
  if save == "y":
    return
  else:
    stats = {"Level":1,"Strength":10, "Constitution":10, "Dexterity":10, "Agility":10, "Perception":10, "Charisma":10, "Intelligence":10, "Wisdom":10}
    sub_stats = {"Max HP":100, "Current HP":100, "Max MP":50, "Current MP":50, "Item Damage":0, "Crit Chance":0.0, "Learn Chance":0.0, "Damage-Upper":0, "Damage-Lower":0, "Defense":0, "Gold":0, "XP":0, "XP Needed":10, "XP Next Scale Up":10} 
    statAssign()
"""
def save():
  print(gold + "Saved!")
  global name
  db["Name"] = name
  global race
  db["Race"] = race
  global gender
  db["Gender"] = gender
  db["Stats"] = stats
  db["Sub Stats"] = sub_stats
  db["Quest Progress"] = questProgress
  db["Reputation"] = reputation
  db["Tile Items"] = tileItems
  db["Inventory"] = inventory
  db["Equipped"] = equipped
  db["Saved"] = True
  global tile
  db["Tile"] = tile
"""

def selector(): #Character selector for specific character attribute bonus thing.
  global race
  global gender
  global name
  print(cyan + "Pick your character race:")
  print(" Human" + gold +" (Ch-D)")
  print(cyan + " Elf" + gold +" (I-W)")
  print(cyan + " Dwarf" + gold +" (S-Co)")
  placeholder = checkIn(("h", "e", "d", "human", "elf", "dwarf"), "str")
  if placeholder == "h" or placeholder == "human":
    stats["Perception"] += 3
    stats["Dexterity"] += 3
    race = "Human"
  elif placeholder == "e" or placeholder == "elf":
    stats["Intelligence"] += 3
    stats["Wisdom"] += 3
    race = "Elf"
  elif placeholder == "d" or placeholder == "dwarf":
    stats["Strength"] += 3
    stats["Constitution"] += 3
    race = "Dwarf"

  print(cyan + "Pick your character gender:")
  print(" Male" + gold + " (S-Co)")
  print(cyan + " Female" + gold + " (Ch-D)")
  inputGender = checkIn(("m", "f", "male", "female"), "str")
  if inputGender == "m" or inputGender == "male":
    stats["Strength"] += 4
    stats["Constitution"] += 4
    gender = "Male"
  elif inputGender == "f" or inputGender == "female":
    stats["Charisma"] += 4
    stats["Dexterity"] += 4
    gender = "Female"

  name = input(cyan + "Enter your name: " + gold)

  
    
def checkIn(listLegals, inputType, message=""): #Method for a customized "Is this input allowed?" and "If so do this."
  if inputType == "str":
    inputVal = input(message)
    inputVal = inputVal.lower()
  elif inputType == "int":
    inputVal = input(message)
  while inputVal not in listLegals:
    print(red + "Invalid input. Please try again.", reset)
    if inputType == "str":
      inputVal = input(message)
      inputVal = inputVal.lower()
    elif inputType == "int":
      inputVal = input(message)
  return inputVal

def statsCheck(): #In-game stat checker!
  global stats
  print(cyan + name + ", Level " + str(stats["Level"]) + " " + gender + " " + race + ":")
  print(red + "HP: " + str(sub_stats["Current HP"]) + "/" + str(sub_stats["Max HP"]))
  print(light_purple + "MP: " + str(sub_stats["Current MP"]) + "/" + str(sub_stats["Max MP"]))
  print(green+ "XP: " + str(sub_stats["XP"]) + "/" + str(sub_stats["XP Needed"]))
  print(gold + str(sub_stats["Gold"]) + " Gold")
  print(fg.blue("Strength: ") + green + str(stats["Strength"]))
  print(fg.blue("  Damage range (") + gold + "S-[melee-item]" + fg.blue("):"), fg.red, (stats["Strength"]), "-",
        (stats["Strength"] + sub_stats["Item Damage"]))
  print(fg.blue("Constitution: ") + green,  stats["Constitution"])
  print(fg.blue + "Perception: " + green + str(stats["Perception"]))
  print(fg.blue + "Dexterity: " + green + str(stats["Dexterity"]))
  print(fg.blue("  Crit Chance (") + gold +"P-D" + fg.blue("): ") + green +
        str(sub_stats["Crit Chance"]) + "%")
  print(fg.blue + "Charisma: " + green + str(stats["Charisma"]))
  print(fg.blue + "Intelligence: " + green + str(stats["Intelligence"]))
  print(fg.blue("  Learn Chance Bonus (") + gold + "I-W" + fg.blue("): ") + green + str(sub_stats["Learn Chance"]) + "%")
  print(fg.blue + "Wisdom:" + green, stats["Wisdom"], reset)


#Inventory System (Yes it's GODDAMN HUGE)
def inventoryMenu():
  print(gold + name + "'s"+ green + " inventory")
  print(blue + "Options:")
  invChoicer = checkIn(("list", "equip", "unequip", "consumable", "exit"), "str", (blue + "List, Equip, Unequip, Consumable, Exit " + gold))
  if invChoicer == "list":
    counter = 0
    for _, value in inventory.items():
      print(value)
      counter += 1
    if counter == 0:
      print(red + "You have nothing in your inventory.")
  elif invChoicer == "equip":
    equipItems()
    inventoryMenu()
  elif invChoicer == "unequip":
    unequipItems()
    inventoryMenu()
  elif invChoicer == "consumable":
    consumableMenu()
    inventoryMenu()
  elif invChoicer == "exit":
    return
  else:
    inventoryMenu()

def consumableMenu():
  print(green + "< Consumable Item Menu >", reset)
  print("Type list to show your usable Consumables")
  listConsumableItems = ["list", "exit"]
  legalList = []
  for _, value in inventory.items():
    if value.isSpecifiedType("Consumable"):
      legalList.append(value)
      listConsumableItems.append(value.getItemName().lower())
  consumableChecker = checkIn(listConsumableItems, "str", (cyan + "Select a Consumable to use. " + gold))
  if consumableChecker == "list":
    if len(legalList) == 0:
      print(red + "You do not have any consumables in your inventory.")
      return
    for i in legalList:
      print(blue +"[ " + str(i) + blue + " ]", reset)
  elif consumableChecker == "exit":
    return
  else:
    consumableChecker = consumableChecker.title()
    for key, value in identifierDict[consumableChecker].getBonusDict().items():
      try:
        sub_stats[key] += value
      except:
        stats[key] += value
    inventory[consumableChecker] - 1
    if inventory[consumableChecker].getItemAmount() == 0:
      inventory.pop(consumableChecker)
    identifierDict[consumableChecker] - 1
    return
    
  

def equipItems():
  print(green + "< Equip Item Menu >", reset)
  print("Type list to show your equipped items")
  equipChecker = checkIn(("head", "chest", "legs", "feet", "weapon", "neck", "ring", "magic", "list", "exit"), "str", (cyan + "Select a slot to equip to: " + gold))
  if equipChecker == "list":
    for key, value in equipped.items():
      if type(value) == str: 
        print(blue + key + ": [ " + value + " ]", reset)
      else:
        print(blue + key + ": [ " + value.equippedRepresentation() + blue + " ]", reset)
  elif equipChecker == "exit":
    return
  elif equipChecker == "weapon":
    if equipped["Weapon"] == "Empty":
      equipWeapons()
      equipItems()
    else:
      print(red + "Slot occupied!", reset)
      equipItems()
  else:
    print(gold + "Not implemented.")
  

def equipWeapons():
  global inventory
  global sub_stats
  listWeaponItems = []
  for _, value in inventory.items():
    if value.isSpecifiedType("Weapon"):
      listWeaponItems.append(value)
  print(green + "< " + red + "Weapon Select " + green + ">", reset)
  print("The following are equippable. Pick from the list.")
  legalNames = []
  for i in listWeaponItems:
    print(blue +"[ " + str(i) + blue + " ]", reset)
    legalNames.append(i.getItemName().lower())
  legalNames.append("exit")
  userInput = checkIn(legalNames, "str", (blue + "Equip which " + red + "weapon" + blue + "? " + gold))
  if userInput == "exit":
    return
  userInput = userInput.title()
  for key, value in identifierDict[userInput].getBonusDict().items():
    sub_stats[key] += value
  sub_stats["Damage-Upper"] += sub_stats["Item Damage"]
  inventory[userInput] - 1
  if inventory[userInput].getItemAmount() == 0:
    inventory.pop(userInput)
  equipped["Weapon"] = identifierDict[userInput]
  return
  
def unequipItems():
  print(green + "< Unequip Item Menu >", reset)
  print("Type list to show your equipped items")
  equipChecker = checkIn(("head", "chest", "legs", "feet", "weapon", "neck", "ring", "magic", "list", "exit"), "str", (cyan + "Select a slot to unequip from: " + gold))
  if equipChecker == "list":
    for key, value in equipped.items():
      if type(value) == str: 
        print(blue + key + ": [ " + value + " ]", reset)
      else:
        print(blue + key + ": [ " + value.equippedRepresentation() + blue + " ]", reset)
  elif equipChecker == "exit":
    return
  else:
    typeItem = equipChecker.capitalize()
    item = equipped[typeItem]
    if item != "Empty":
      try:
        inventory[item.getItemName()] + 1
      except:
        identifierDict[item.getItemName()] + 1
        inventory.update({item.getItemName():identifierDict[item.getItemName()]})
      if "Item Damage" in identifierDict[item.getItemName()].getBonusDict():
        sub_stats["Damage-Upper"] -= sub_stats["Item Damage"]
      for key, value in identifierDict[item.getItemName()].getBonusDict().items():
        sub_stats[key] -= value
      equipped[typeItem] = "Empty"
    else:
      print(red + "Slot already empty.")
      unequipItems()

#Skimping on it lol
#Just check the file cuz I don't wanna print it out here
def help():
  print(green + "-----> Welcome to Primallux <-----")
  print(reset + "Please read about the controls in the " + blue + "README", reset, "file")

def levelUp(): #IN PROGRESS
  skillPoints = 0
  while True:
    if sub_stats["XP"] >= sub_stats["XP Needed"]:
      sub_stats["XP"] -= sub_stats["XP Needed"]
      skillPoints = 6
      stats["Level"] += 1
      print(green + "----------{ LEVEL UP! }----------")
      sub_stats["XP Needed"] += sub_stats["XP Next Scale Up"]
      sub_stats["XP Next Scale Up"] += round((sub_stats["XP Next Scale Up"] * ((1 + 5 ** 0.5) / 2)))
      while skillPoints > 0:
        print(blue + "You have " + green + str(skillPoints) + " points to assign to stats.")
        userInput = checkIn(("list", "strength", "constitution", "dexterity", "perception", "charisma", "intelligence", "wisdom", "str", "con", "dex", "per", "cha", "int", "wis"), "str", (blue + "What would you like to assign points to? (List to show your current information.) "))
        if userInput == "list":
          statsCheck()
        else:
          if userInput in ("str", "con", "dex", "per", "cha", "int", "wis"):
            userInput = {"str":"strength", "con":"constitution", "dex":"dexterity", "per":"perception", "cha":"charisma", "int":"intelligence", "wis":"wisdom"}[userInput]
          userInput = userInput.capitalize()
          print(blue + "Available points: " + green + str(skillPoints))
          pointsAmount = checkIn([x for x in range(skillPoints+1)], "int", (blue + "Assign how many points to " + userInput + "? " + gold))
          stats[userInput] += pointsAmount
          sub_stats["Crit Chance"] = round((0.1 * stats["Dexterity"] * (stats["Perception"]) * 0.01) + 1, 2)
          sub_stats["Max MP"] = stats["Wisdom"] * 5
          sub_stats["Current MP"] = sub_stats["Max MP"]
          sub_stats["Max HP"] = stats["Constitution"] * 10
          sub_stats["Current HP"] = sub_stats["Max HP"]
          sub_stats["Damage-Lower"] = stats["Strength"]
          sub_stats["Damage-Upper"] = stats["Strength"] + sub_stats["Item Damage"]
          sub_stats["Learn Chance"] = round((stats["Intelligence"]*0.1) * (stats["Wisdom"] * 0.01) + 1, 2)
    else:
      break
  return

#Fight system. This is going to be filled with bugs I bet.
def monsterFight(mob):
  
  defendBool = False
  print(red + "----------< ! FIGHT ! >----------")
  print(reset + mob.getEnterText())
  while True:
    userInput = checkIn(("attack", "fight", "a", "f", "run", "flee", "consumable", "c", "r", "talk", "t", "defend", "d", "pacify", "p"), "str", (reset + "What will you do? " + gold))
    if userInput == "attack" or userInput == "fight" or userInput == "a" or userInput == "f":
      print(reset + "You attack the " + red + mob.getMobName() + ".")
      if choices(("hit", "miss"), weights=(stats["Dexterity"], mob.getSpeed())) == ["hit"]:
        if randint(1, 101) <= sub_stats["Crit Chance"]:
          print(gold + "< CRITICAL HIT! >", reset)
          num = 2 * randint(sub_stats["Damage-Lower"], sub_stats["Damage-Upper"])
          mob.takeDamage(num)
          print(orange + "Dealt " + str(num) + " damage to " + mob.getMobName() + ".")
        else:
          num = randint(sub_stats["Damage-Lower"], sub_stats["Damage-Upper"])
          mob.takeDamage(num)
          print(orange + "Dealt " + str(num) + " damage to " + mob.getMobName() + ".")
      else:
        print(red + "You missed.")
    elif userInput == "run" or userInput == "flee" or userInput == "r":
      if choices(("escape", "caught"), weights=(stats["Dexterity"], mob.getSpeed())) == ["escape"]:
        print(reset + "You have successfully escaped from " + mob.getMobName())
        break
      else:
        print("You fail to run away fast enough, and the " + mob.getMobName() + " catches to you.")
    
    elif userInput == "defend" or userInput == "d":
      defenceVar = choices(("crit", "success", "fail"), weights=(round(sub_stats["Crit Chance"]), round((sub_stats["Defense"]+stats["Constitution"]*0.1)), mob.dealDamage()))
      if defenceVar == ["crit"]:
        print(gold + "< CRITICAL HIT! >", reset)
        num = 2 * randint(sub_stats["Damage-Lower"], sub_stats["Damage-Upper"])
        mob.takeDamage(num)
        print(orange + "Dealt " + str(num) + " damage to " + mob.getMobName() + ".")
        defendBool = True
      elif defenceVar == ["success"]:
        defendBool = True
      else:
        print(red + "You fail to defend yourself properly.", reset)
    elif userInput == "pacify" or userInput == "p":
      if mob.disarm(stats, reputation):
        print(green + "You convince the " + mob.getMobName() + " not to fight!", reset)
        reputation[mob.getFaction()] += mob.getPacifyBonus()
        break
        return
      else:
        print(red + "You fail to charm " + mob.getMobName() + " away from fighting.", reset)
    elif userInput == "consumable" or userInput == "c":
      consumableMenu()
    elif userInput == "talk" or userInput == "t":
      if mob.getDialogue() == "":
        print("The " + mob.getMobName() + " doesn't respond.")
    print(red + str(mob))
    
    if mob.isDefeated():
      sub_stats["XP"] += mob.getXP()
      if mob.getFaction() != "":
        reputation[mob.getFaction()] -= mob.getRepDecrease()
      print(green + "----------< You win! >----------")
      mob.resetHP()
      levelUp()
      break
    
    if defendBool == True:
      if choices(("full", "half"), weights=(round((sub_stats["Defense"]*sub_stats["Crit Chance"]+stats["Constitution"]*0.1)), mob.dealDamage())) == ["full"]:
        print(green + "You completely block the " + mob.getMobName() + "'s attack!", reset)
        print(red + "Your HP: " + str(sub_stats["Current HP"]) + "/" + str(sub_stats["Max HP"]))
        defendBool = False
      else:
        print(orange + "You block most of the attack, but some slips through.", reset)
        sub_stats["Current HP"] -= round((mob.dealDamage()*0.5))
        print(red + "Your HP: " + str(sub_stats["Current HP"]) + "/" + str(sub_stats["Max HP"]))
        defendBool = False
    else:
      print(red + "You take the hit.", reset)
      print(mob.getTaunt())
      sub_stats["Current HP"] -= mob.dealDamage()
      print(red + "Your HP: " + str(sub_stats["Current HP"]) + "/" + str(sub_stats["Max HP"]))

    if sub_stats["Current HP"] <= 0:
      print("You have died.")
      quit()
  return
  

  

#Actually make the adventure?????????

def tile1():
  global tile
  tile = 1
  print(reset + "You awaken in a forest of pines.")
  userInput = checkIn(tilesetLegals, "str", "What will you do? " + gold)
  if userInput == "search" or userInput == "look":
    try:
      num = randint(0, 30-stats["Perception"])
    except:
      num = 0
    if num == 0 and stats["Level"] < 3 and tileItems["Tile 1"] > 0:
      print(reset + "You find a " + pineTwig.getColor() + "Pine Twig.")
      tileItems["Tile 1"] -= 1
      try:
        inventory["Pine Twig"] + 1
      except:
        pineTwig + 1
        inventory.update({"Pine Twig":pineTwig})
    elif tileItems["Tile 1"] == 0 or stats["Level"] >= 3:
      print("There's nothing left of any interest.")
    else:
      print(reset + "You find " + red + "nothing.")
    tile1()
  elif userInput == "stats":
    statsCheck()
    tile1()
  elif userInput == "help" or userInput == "h":
    help()
    tile1()
  elif userInput == "int" or userInput == "interact":
    print("There's nothing to interact with!")
    tile1()
  elif userInput == "inv" or userInput == "inventory":
    inventoryMenu()
    tile1()
  elif userInput == "n" or userInput == "north":
    tile2()
  elif userInput == "s" or userInput == "south":
    tile5()
  elif userInput == "e" or userInput == "east":
    tile3()
  elif userInput == "w" or userInput == "west":
    tile4()
  elif userInput == "wander":
    num = randint(1,4)
    if num == 1:
      tile2()
    elif num == 2:
      tile5()
    elif num == 3:
      tile3()
    elif num == 4:
      tile4()
  #elif userInput == "save":
    #save()
    #tile1()

def tile2():
  global tile
  tile = 2
  print(reset + "A burbling brook sounds off ahead.")
  userInput = checkIn(tilesetLegals, "str", ("What will you do? " + gold))
  if userInput == "search" or userInput == "look":
    print(reset + "You spot the outline of a building off to the northwest.")
    tile2()
  elif userInput == "stats":
    statsCheck()
    tile2()
  elif userInput == "help" or userInput == "h":
    help()
    tile2()
  elif userInput == "int" or userInput == "interact":
    print("There's nothing to interact with!")
    tile2()
  elif userInput == "inv" or userInput == "inventory":
    inventoryMenu()
    tile2()
  elif userInput == "n" or userInput == "north":
    print("Area not made yet, planned.")
    tile2()
  elif userInput == "s" or userInput == "south":
    tile1()
  elif userInput == "e" or userInput == "east":
    tile7()
  elif userInput == "w" or userInput == "west":
    tile6()
  elif userInput == "wander":
    num = randint(1,4)
    if num == 2:
      tile1()
    elif num == 4:
      tile6()
    else:
      print("Area not made yet, planned.")
      tile2()
  #elif userInput == "save":
    #save()
    #tile2()

def tile3():
  global tile
  tile = 3
  print(reset + "A very large tree stands before you, its crown scraping the sky.")
  userInput = checkIn(tilesetLegals, "str", ("What will you do? " + gold))
  if userInput == "search" or userInput == "look":
    try:
      num = randint(0, 35-stats["Perception"])
    except:
      num = 0
    if num <= 1 and stats["Level"] < 3 and tileItems["Tile 3"] > 0:
      print(reset + "You find a " + mushroom.getColor() + "Mushroom.")
      tileItems["Tile 3"] -= 1
      try:
        inventory["Mushroom"] + 1
      except:
        mushroom + 1
        inventory.update({"Mushroom":mushroom})
    elif tileItems == 0 or stats["Level"] >= 3:
      print("There's nothing left of any interest.")
    else:
      print(reset + "You find " + red + "nothing.")
    tile3()
  elif userInput == "stats":
    statsCheck()
    tile3()
  elif userInput == "help" or userInput == "h":
    help()
    tile3()
  elif userInput == "int" or userInput == "interact":
    print("There's nothing to interact with!")
    tile3()
  elif userInput == "inv" or userInput == "inventory":
    inventoryMenu()
    tile3()
  elif userInput == "n" or userInput == "north":
    tile7()
  elif userInput == "s" or userInput == "south":
    print("Area not made yet, planned.")
    tile3()
  elif userInput == "e" or userInput == "east":
    print("Area not made yet, planned.")
    tile3()
  elif userInput == "w" or userInput == "west":
    tile1()
  elif userInput == "wander":
    num = randint(1,4)
    if num == 4:
      tile1()
    else:
      print("Area not made yet, planned.")
      tile3()
  #elif userInput == "save":
    #save()
    #tile3()

def tile4():
  global tile
  tile = 4
  print(reset + "The trees give way to a dirt road cutting through the wilderness.")
  userInput = checkIn(tilesetLegals, "str", ("What will you do? " + gold))
  if userInput == "search" or userInput == "look":
    if questProgress["Bandits"] == 1:
      print("You smell the coppery tang of blood down southward the path.")
    else:
      print("A serene road stretches through the forest, as off to the north, lies a fortress sitting atop a hill.")
    tile4()
  elif userInput == "stats":
    statsCheck()
    tile4()
  elif userInput == "help" or userInput == "h":
    help()
    tile4()
  elif userInput == "int" or userInput == "interact":
    print("There's nothing to interact with!")
    tile4()
  elif userInput == "inv" or userInput == "inventory":
    inventoryMenu()
    tile4()
  elif userInput == "n" or userInput == "north":
    tile6()
  elif userInput == "s" or userInput == "south":
    print("Area not made yet, planned.")
    tile4()
  elif userInput == "e" or userInput == "east":
    tile1()
  elif userInput == "w" or userInput == "west":
    print("Area not made yet, planned.")
    tile4()
  elif userInput == "wander":
    num = randint(1,4)
    if num == 3:
      tile1()
    else:
      print("Area not made yet, planned.")
      tile4()
  #elif userInput == "save":
    #save()
    #tile4()

def tile5():
  global tile
  tile = 5
  print(reset + "The leaves wave in the wind. A damp draft curls around your feet.")
  userInput = checkIn(tilesetLegals, "str", ("What will you do? " + gold))
  if userInput == "search" or userInput == "look":
    print(reset + "You spot a cave, further south.")
    tile5()
  elif userInput == "stats":
    statsCheck()
    tile5()
  elif userInput == "help" or userInput == "h":
    help()
    tile5()
  elif userInput == "int" or userInput == "interact":
    print("There's nothing to interact with!")
    tile5()
  elif userInput == "inv" or userInput == "inventory":
    inventoryMenu()
    tile5()
  elif userInput == "n" or userInput == "north":
    tile1()
  elif userInput == "s" or userInput == "south":
    tile9()
  elif userInput == "e" or userInput == "east":
    print("Area not made yet, planned.")
    tile5()
  elif userInput == "w" or userInput == "west":
    print("Area not made yet, planned.")
    tile5()
  elif userInput == "wander":
    num = randint(1,4)
    if num == 1:
      tile1()
    elif num == 3:
      tile9()
    else:
      print("Area not made yet, planned.")
      tile5()
  #elif userInput == "save":
    #save()
    #tile5()
  

def tile6():
  global tile
  tile = 6
  print(reset + "A hill rises, a mound that rises slowly above the ground.\nAtop which lies a fortress of stone.")
  userInput = checkIn(tilesetLegals, "str", ("What will you do? " + gold))
  if userInput == "search" or userInput == "look":
    if questProgress["Bandits"] == 1:
      print("You smell the coppery tang of blood down southward the path.")
    print("While climbing the hill, the clamor of those within the fortress grows louder and louder.")
    tile6()
  elif userInput == "stats":
    statsCheck()
    tile6()
  elif userInput == "help" or userInput == "h":
    help()
    tile6()
  elif userInput == "int" or userInput == "interact":
    print("There's nothing to interact with!")
    tile6()
  elif userInput == "inv" or userInput == "inventory":
    inventoryMenu()
    tile6()
  elif userInput == "n" or userInput == "north":
    print("Area not made yet, planned.")
    tile6()
  elif userInput == "s" or userInput == "south":
    tile4()
  elif userInput == "e" or userInput == "east":
    tile2()
  elif userInput == "w" or userInput == "west":
    print("Area not made yet, planned.")
    tile6()
  elif userInput == "wander":
    num = randint(1,4)
    if num == 2:
      tile4()
    elif num == 3:
      tile2()
    else:
      print("Area not made yet, planned.")
      tile6()
  #elif userInput == "save":
    #save()
    #tile6()

def tile7():
  global tile
  tile = 7
  print(reset + "A river rushes before you, running through the forest.")
  userInput = checkIn(tilesetLegals, "str", ("What will you do? " + gold))
  if userInput == "search" or userInput == "look":
    print("You spot fish swimming in these shallows")
    tile7()
  elif userInput == "stats":
    statsCheck()
    tile7()
  elif userInput == "help" or userInput == "h":
    help()
    tile7()
  elif userInput == "int" or userInput == "interact":
    print("There's nothing to interact with!")
    tile7()
  elif userInput == "inv" or userInput == "inventory":
    inventoryMenu()
    tile7()
  elif userInput == "n" or userInput == "north":
    print("Area not made yet, planned.")
    tile7()
  elif userInput == "s" or userInput == "south":
    tile3()
  elif userInput == "e" or userInput == "east":
    print("Area not made yet, planned.")
    tile7()
  elif userInput == "w" or userInput == "west":
    tile2()
  elif userInput == "wander":
    num = randint(1,4)
    if num == 2:
      tile3()
    elif num == 4:
      tile2()
    else:
      print("Area not made yet, planned.")
      tile7()
  #elif userInput == "save":
    #save()
    #tile7()

def tile8():
  global tile
  tile = 8
  print(reset + "A river rushes before you, running through the forest.")
  userInput = checkIn(tilesetLegals, "str", ("What will you do? " + gold))
  if userInput == "search" or userInput == "look":
    print("You spot fish swimming in these shallows")
    tile8()
  elif userInput == "stats":
    statsCheck()
    tile8()
  elif userInput == "help" or userInput == "h":
    help()
    tile8()
  elif userInput == "int" or userInput == "interact":
    print("There's nothing to interact with!")
    tile8()
  elif userInput == "inv" or userInput == "inventory":
    inventoryMenu()
    tile8()
  elif userInput == "n" or userInput == "north":
    print("Area not made yet, planned.")
    tile8()
  elif userInput == "s" or userInput == "south":
    tile2()
  elif userInput == "e" or userInput == "east":
    print("Area not made yet, planned.")
    tile8() 
  elif userInput == "w" or userInput == "west":
    tile2()
  elif userInput == "wander":
    num = randint(1,4)
    if num == 2:
      tile3()
    elif num == 4:
      tile2()
    else:
      print("Area not made yet, planned.")
      tile8()
  #elif userInput == "save":
    #save()
    #tile7()

def tile9():
  global tile
  tile = 9
  print(reset + "A yawning cave opening is ahead of you.")
  userInput = checkIn(tilesetLegals, "str", ("What will you do? " + gold))
  if userInput == "search" or userInput == "look":
    if mobList["Tile 9"] > 0 and randint(1, 5) == 1:
      monsterFight(hungryWolf)
      mobList["Tile 9"] -= 1
      tile9()
    elif mobList == 0:
      print("All that's left here, are the stones that line the entrance, and the trees around it.")
    elif reputation["Nature"] <= 150:
      print("You feel like you are being watched by a few creatures nearby.")
    else:
      print("The animals welcome your presence in their homes.")
    tile9()
  elif userInput == "stats":
    statsCheck()
    tile9()
  elif userInput == "help" or userInput == "h":
    help()
    tile9()
  elif userInput == "int" or userInput == "interact":
    print("There's nothing to interact with!")
    tile9()
  elif userInput == "inv" or userInput == "inventory":
    inventoryMenu()
    tile9()
  elif userInput == "n" or userInput == "north":
    tile5()
  elif userInput == "s" or userInput == "south":
    print("Area not made yet, planned.")
    tile9()
  elif userInput == "e" or userInput == "east":
    print("Area not made yet, planned.")
    tile9() 
  elif userInput == "w" or userInput == "west":
    print("Area not made yet, planned.")
    tile9()
  elif userInput == "wander":
    num = randint(1,4)
    if num == 1:
      tile2()
    else:
      print("Area not made yet, planned.")
      tile9()
  
  #elif userInput == "save":
    #save()
    #tile7()

  
def redirect(tile): #For use when saving data? It's supposed to start you off at the right tile.
  if tile == 1: 
    tile1()
  elif tile == 2:
    tile2()
  elif tile == 3:
    tile3()
  elif tile == 4:
    tile4()
  elif tile == 5:
    tile5()
  elif tile == 6:
    tile6()
global name, race, gender, tile
name = ""
race = ""
gender = ""
"""
if "Saved" in db.keys():
  print("You have a save file loaded! Would you like to load from your past save?")
  loadSave = input(gold + "Yes/No? ")
  if loadSave.lower() == "no":
    name = ""
    race = ""
    gender = ""
    db.clear()
  else:
    name = db["Name"]
    race = db["Race"]
    gender = db["Gender"]
    print("I'll assume that's a yes.")
    stats = db["Stats"]
    sub_stats = db["Sub Stats"]
    questProgress = db["Quest Progress"]
    reputation = db["Reputation"]
    tileItems = db["Tile Items"]
    inventory = db["Inventory"]
    equipped = db["Equipped"]
    redirect(db["Tile"])
"""

stats = {"Level":1,"Strength":10, "Constitution":10, "Dexterity":10, "Agility":10, "Perception":10, "Charisma":10, "Intelligence":10, "Wisdom":10} #Main stats that're actually displayed.

sub_stats = {"Max HP":100, "Current HP":100, "Max MP":50, "Current MP":50, "Item Damage":0, "Crit Chance":0.0, "Learn Chance":0.0, "Damage-Upper":0, "Damage-Lower":0, "Defense":0, "Gold":0, "XP":0, "XP Needed":10, "XP Next Scale Up":10} #Stats that are dependent upon the stats read by the stats function, 

questProgress = {"Bandits":0} #Dictionary for storing quest progression based on stages! Get quests from NPCs.

reputation = {"Silvaris":0, "Tourial":0, "Moonreach Guild":0, "Human Kingdom":0, "Elven Kingdom":0, "Firway":0, "Red Banner Company":0, "Cerrunis":0, "Northern Hordes":-50, "Light Pantheon":0, "Death Pantheon":0, "Life Pantheon":0, "Nature":0, "Mind Pantheon":0, "Stellar Covenant":0, "Mind of the Void":-1000} #Reputation system for NPC convo buffs, quests, Sparing system, etc

tileItems = {"Tile 1":7, "Tile 3":6} #Keeps track of how many items there are for each tile.

mobList = {"Tile 9":4} #Assigns a limit on the amount of monsters on a specific tile.

inventory = {}
equipped = {"Head":"Empty", "Chest":"Empty", "Legs":"Empty", "Feet":"Empty", "Weapon":"Empty", "Neck":"Empty", "Ring":"Empty", "Magic":"Empty"}

statAssign()
tile1()