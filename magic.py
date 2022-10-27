from random import randint, choices
from ansi.colour.rgb import rgb256
from ansi.colour.fx import reset
black = "\u001b[30m"
red = "\u001b[31m"
bloodred = rgb256(0x87, 0x0f, 0x01)
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
colorsForTypes = {"Damage":red, "Effect":orange, "Heal":green, "Vampire":bloodred, "DoT":purple, "Buff":cyan}

def int_to_Roman(num):
  val = [
      1000, 900, 500, 400,
      100, 90, 50, 40,
      10, 9, 5, 4,
      1]
  syb = [
      "M", "CM", "D", "CD",
      "C", "XC", "L", "XL",
      "X", "IX", "V", "IV",
      "I"]
  roman_num = ''
  i = 0
  while num > 0:
    for _ in range(num // val[i]):
      roman_num += syb[i]
      num -= val[i]
    i += 1
  return roman_num

class StatusEffect:
  def __init__(self, name, level, duration, target, startTime, effect={}, scaling=0, durationScaling=0):
    self.name = name
    self.level = level
    self.duration = duration
    self.target = target
    self.startTime = startTime
    self.effect = effect
    self.baseEffect = effect
    self.scaling = scaling
    self.durationScaling = durationScaling
    self.defaultDuration = duration
    for key, _ in effect.items():
      effect[key] += (scaling * level)
    duration += (durationScaling * level)

  def __str__(self):
    string = ""
    string += self.name + " " + int_to_Roman(self.level) + ": "
    for key, value in self.effect.items():
      if value > 0:
        string += green + key + " +" + str(value) + " "
      elif value < 0:
        string += red + key + " " + str(value) + " "
    return string
  
  def getLevel(self):
    return self.level
  def setLevel(self, value):
    self.level = int(value)
    for key in self.effect.keys():
      if self.baseEffect[key] > 0:
        self.effect[key] = self.baseEffect[key] + (self.scaling * (self.level-1))
      else:
        self.effect[key] = self.baseEffect[key] - (self.scaling * (self.level-1))
    self.duration = self.defaultDuration + (self.durationScaling * (self.level-1))
  def getDuration(self):
    return self.duration
  def getTarget(self):
    return self.target
  def setTarget(self, value):
    self.target = value
  def getStartTime(self):
    return self.startTime
  def getScaling(self):
    return self.scaling
  def getEffect(self):
    return self.effect
  

class Magic:
  def __init__(self, name, kind, cost, level, cooldown, target, scaling=0, effects=[], damage=0, damageScaling=0, cooldownScaling=0, healAmount=0, healScaling=0, costScaling=0):
    self.name = name
    self.kind = kind
    self.cost = cost
    self.target = target
    self.defaultCost = cost
    self.level = level
    self.cooldown = cooldown
    self.defaultCooldown = cooldown
    self.color = colorsForTypes[kind]
    self.scaling = scaling
    self.effects = effects
    self.damage = damage
    self.defaultDamage = damage
    self.damageScaling = damageScaling
    self.cooldownScaling = cooldownScaling
    self.healAmount = healAmount
    self.defaultHealAmount = healAmount
    self.healScaling = healScaling
    self.costScaling = costScaling

  def __str__(self):
    string = ""
    string += self.color + self.name + " " + int_to_Roman(self.level) + " "
    string += purple + "MP Cost: " + str(self.cost) + " "
    if self.damage > 0:
      string += "Damage: " + str(self.damage)
    if self.healAmount > 0: 
      string += "Heal Amount: " + str(self.healAmount)
    if len(self.effects) != 0:
      for i in self.effects:
        string += " " + str(i)
    return string

  def getCastRepresentation(self):
    string = ""
    string += self.color + self.name
    return string

  def getType(self):
    return self.kind
  def getName(self):
    return self.name
  def getCost(self):
    return self.cost
  def getLevel(self):
    return self.level
  def setLevel(self, amount):
    self.level = amount
    self.damage = self.defaultDamage + (self.level * self.damageScaling)
    self.cooldown = self.defaultCooldown + (self.level * self.cooldownScaling)
    self.cost = self.defaultCost + (self.level * self.costScaling)
    if len(self.effects) != 0:
      for i in self.effects:
        effectDict[i].setLevel(amount)
  def getDamage(self):
    return self.damage
  def getHealAmount(self):
    return self.healAmount
  def getCooldown(self):
    return self.cooldown
  def getTarget(self):
    return self.target
  def setTarget(self, value):
    self.target = value
  def getEffects(self):
    return self.effects
  def receiveStringified(self, value):
    value = value.split("|")
    self.setLevel(value[1])
  
    
bleed = StatusEffect("Bleed", 1, 8, "player", 0, effect={"HP":-1}, scaling=1, durationScaling=1)    
deafen = StatusEffect("Deafen", 1, 6, "player", 0, effect={"Damage":-4, "Dexterity":-5}, scaling=2)
blinded = StatusEffect("Blinded", 1, 3, "player", 0, effect={"Dexterity":-20}, scaling=5)
foodPoisoning = StatusEffect("Food Poisoning", 1, 28, "player", 0, effect={"Dexterity":-2, "Constitution":-4, "Current HP":-20, "Max HP":-20}, scaling=2, durationScaling=1)
heartyMeal = StatusEffect("Hearty Meal", 1, 30, "player", 0, effect={"Damage":4, "Dexterity":3}, scaling=2, durationScaling=4)
improvedSight = StatusEffect("Improved Sight", 1, 40, "player", 0, effect={"Perception":4}, scaling=3, durationScaling=8)

discordantShriek = Magic("Discordant Shriek", "Effect", 16, 2, 2, "player", effects=["Deafen"])
bleedingStrike = Magic("Bleeding Strike", "Effect", 20, 1, 2, "player", effects=["Bleed"], scaling=1, damage=6, damageScaling=2, cooldownScaling=1)
blindingFlash = Magic("Blinding Flash", "Effect", 10, 1, 5, "player", scaling=1, effects=["Blinded"])
heavyStrike = Magic("Heavy Strike", "Damage", 25, 1, 3, "player", damage=48, damageScaling=6, cooldownScaling=1, costScaling=5)

effectDict = {"Deafen":deafen, "Bleed":bleed, "Blinded":blinded, "Food Poisoning":foodPoisoning, "Hearty Meal":heartyMeal, "Improved Sight":improvedSight}
spellDict= {"Discordant Shriek":discordantShriek, "Bleeding Strike":bleedingStrike, "Blinding Flash":blindingFlash, "Heavy Strike":heavyStrike}