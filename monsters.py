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
  def __init__(self, name, hp, damage_lower, damage_upper, speed, defense, giveXP, enterBattleText, duringBattleText, exitBattleText, taunt, pacifyText, ifPacifyBonus, convinceThreshold=5, lootTable={"Rolls":1}, spells=(), faction="", factionRepDecrease=0, dialogue=()):
    self.name = name
    self.faction = faction
    self.mobHP = hp
    self.mobMaxHP = hp
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
    self.taunt = taunt
    self.pacifyText = pacifyText
    self.ifPacifyBonus = ifPacifyBonus
    self.dialogue = dialogue
  def __str__(self):
    return self.name + " " + red + "HP: " + str(self.mobHP) + "/" + str(self.mobMaxHP)
  
  def takeDamage(self, amount):
    self.mobHP -= (amount - self.defense)

  def dealDamage(self):
    return randint(self.damageLower, self.damageUpper)

  def resetHP(self):
    self.mobHP = self.mobMaxHP
  
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
  def getTaunt(self):
    return self.taunt
  def pacifyText(self):
    return self.pacifyText
  def getPacifyBonus(self):
    return self.ifPacifyBonus
  def getFaction(self):
    return self.faction
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
    
  def disarm(self, playerStats, playerRep):
    if self.faction == "":
      if choices(("succeed", "fail"), weights=(playerStats["Charisma"], self.convinceThreshold)) == "succeed":
        return True
      else:
        return False
    else:
      if playerRep[self.faction]<-100:
        return False
      elif playerRep[self.faction]>100:
        return True
      else:
        if choices(("succeed", "fail"), weights=(playerStats["Charisma"], self.convinceThreshold)) == "succeed":
          return True
        else:
          return False
