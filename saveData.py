#Unused because Repl doesn't let pickle access the save files. Shifted to using Repl DB. Works perfectly when you get this in a personal version though, which is hilarious.
import pickle
from ansi.colour.rgb import rgb256
from ansi.colour.fx import reset

black = "\u001b[30m"
red = "\u001b[31m"
green = rgb256(0x00, 0xff, 0x09)
orange = rgb256(0xd4, 0x71, 0x00)
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

global username, password, accountBool
accountBool = False

def login():
  global username, password, accountBool
  print("Login to your account.")
  print("Just press enter if you don't have an account.")
  username = input("Type in your username. ")
  if username == "":
    return False
  password = input("Type in your password to log in. ")
  try:
    accountBool = True
    file = open(str(hash(str(hash(username)) + str(hash(password)))), "rb")
    character = pickle.load(file)
    file.close()
    return character
  except (OSError, IOError):
    print(red + "One or more of the entered information is incorrect. Please try again.", reset)
    accountBool = False
    login()


def save(playerStats, playerEquipped, playerInventory, playerSubStats, playerQuestProgress, currentTileItems, currentTileMobs, playerName, playerGender, playerRace, tileVar):
  saveData = {"Stats":playerStats, "Equipped":playerEquipped, "Inventory":playerInventory, "Sub Stats":playerSubStats, "Quest Progress":playerQuestProgress, "Tile Items":currentTileItems, "Tile Mobs":currentTileMobs, "Name":playerName, "Gender":playerGender, "Race":playerRace, "Tile ID":tileVar}
  global username, password, accountBool
    
  if accountBool:
    file = open(str(hash(str(hash(username)) + str(hash(password)))), "wb")
    pickle.dump(saveData, file)
    print(green + "Data saved!")
    file.close()
  else:
    print(orange + "Make an account.", reset)
    username = input("Create a username: ")
    password = input("Create a password: ")
    file = open(str(hash(str(hash(username)) + str(hash(password)))), "wb")
    pickle.dump(saveData, file)
    print(green + "Data saved!")
    file.close()
    accountBool = True