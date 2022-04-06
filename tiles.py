from ansi.colour.rgb import rgb256
from ansi.colour.fx import reset
#Use this later for handling the tile if statements?
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

def tileStatements(tile, tileFlavorText, hasItem):
  global tile
  tile = 1
  print(reset + tileFlavorText)
  userInput = checkIn(tilesetLegals, "str", "What will you do? " + gold)
  match userInput:
    case search or look:

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
    elif tileItems == 0 or stats["Level"] >= 3:
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