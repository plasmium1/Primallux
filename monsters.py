import playerInventory
from random import randint, choices
from ansi.colour.rgb import rgb256
from ansi.colour.fx import reset
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
  def __init__(self, name, hp, damage_lower, damage_upper, speed, defense, giveXP, enterBattleText, duringBattleText, exitBattleText, pacifyText, ifPacifyBonus, convinceThreshold=5, lootTable={"Rolls":1}, spells=(), faction="", factionRepDecrease=0, dialogue=()):
    self.name = name
    self.faction = faction
    self.mobHP = hp
    self.damageLower = damage_lower
    self.damageUpper = damage_upper
    self.speed = speed
    self.lootTable = lootTable
    self.convinceThreshold = convinceThreshold
    self.defense = defense
    self.giveXP = giveXP
    self.spells = spells
    self.factionRepDecrease = factionRepDecrease
    self.enterBattleText = enterBattleText
    self.duringBattleText = duringBattleText
    self.exitBattleText = exitBattleText
    self.pacifyText = pacifyText
    self.ifPacifyBonus = ifPacifyBonus
    self.dialogue = dialogue

  def takeDamage(self, amount):
    self.mobHP -= (amount - self.defense)

  def dealDamage(self):
    return randint(self.damageLower, self.damageUpper)

  def lootGenerate(self):
    keys = []
    values = []
    for key, value in self.lootTable.items()[1:]:
      keys.add(key)
      values.add(values)
    return choices(keys, values, k=self.lootTable["Rolls"])

  def getMobName(self):
    return self.name
  def getSpeed(self):
    return self.speed
  def getDefense(self):
    return self.defense
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
  def pacifyText(self):
    return self.pacifyText
  def getPacifyBonus(self):
    return self.ifPacifyBonus
  def getDialogue(self):
    return self.dialogue[randint(0, len(self.dialogue))]
    
  def disarm(self, playerRep):
    if self.faction == "":
      if randint(1, self.convinceThreshold) == 0:
        return True
      else:
        return False
    else:
      if playerRep[self.faction]<-100:
        return False
      elif playerRep[self.faction]>100:
        return True
      else:
        if randint(1, self.convinceThreshold) == 0:
          return True
        else:
          return False
