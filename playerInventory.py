from ansi.colour.rgb import rgb256
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
colorsForTypes = {"Consumable":green, "Magic":purple, "Weapon":red, "Armor":cyan, "Misc":orange}

class InvItem(object):
  def __init__(self, itemType, itemName, amount):
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
    if type(other) != InvItem or type(other) != EquipmentItem or type(other) != ConsumableItem:
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
  def getItemType(self):
    return self.itemType
  def getItemAmount(self):
    return self.amount
  def getColor(self):
    return self.typeColor

class ConsumableItem(InvItem):
  def __init__(self, itemName, amount, bonuses):
    self.typeColor = green
    self.itemType = "Consumable"
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
        appendedString += appendedString + color + key + " " + str(value) + ", "
      else:
        appendedString += appendedString + color + key + " " + str(value)
    return self.typeColor + self.itemName + cyan + ": " + str(self.amount) + appendedString
  def __str__(self):
    appendedString = " "
    counter = len(self.bonuses.items())
    for key, value in self.bonuses.items():
      counter -= 1
      color = green
      if value < 0:
        color = red
      if counter != 0:
        appendedString += appendedString + color + key + " " + str(value) + ", "
      else:
        appendedString += appendedString + color + key + " " + str(value)
    return self.typeColor + self.itemName + cyan + ": " + str(self.amount) + appendedString
  
  def getBonusDict(self):
    return self.bonuses

  
  

class EquipmentItem(InvItem):
  #Input bonuses parameter as a dictionary with keys as the bonus name, and values as buffs or debuffs.
  def __init__(self, itemType, itemName, amount, bonuses):
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
        appendedString += appendedString + color + key + " " + str(value) + ", "
      else:
        appendedString += appendedString + color + key + " " + str(value)
    return self.typeColor + self.itemName + cyan + ": " + str(self.amount) + appendedString
    
  def __str__(self):
    appendedString = " "
    counter = len(self.bonuses.items())
    for key, value in self.bonuses.items():
      counter -= 1
      color = green
      if value < 0:
        color = red
      if counter != 0:
        appendedString += appendedString + color + key + " " + str(value) + ", "
      else:
        appendedString += appendedString + color + key + " " + str(value)
    return self.typeColor + self.itemName + cyan + ": " + str(self.amount) + appendedString
  def getBonusDict(self):
    return self.bonuses
  def equippedRepresentation(self):
    appendedString = " "
    counter = len(self.bonuses.items())
    for key, value in self.bonuses.items():
      counter -= 1
      color = green
      if value < 0:
        color = red
      if counter != 0:
        appendedString += appendedString + color + key + " " + str(value) + ", "
      else:
        appendedString += appendedString + color + key + " " + str(value)
      
    return self.typeColor + self.itemName + appendedString
  
  