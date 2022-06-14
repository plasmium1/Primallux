from ansi.colour.rgb import rgb256
from ansi.colour.fx import reset
from random import choices

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

#Class for storing data for quests! Quest progress is synced in the main file dictionary but this saves the individual parts of npc text, various other flavor text, the workflow for it, needed rep, and more. This should be tied into a Quest-type interaction in order to launch it. Maybe various other quest type interactions to handle intermediary quest parts?
class Quest:
  def __init__(self, questName, questDescription, difficulty, introText, introInteraction, questChainDict, questChainTextDict, neededReputation):
    self.questName = questName
    self.questDescription = questDescription
    self.difficulty = difficulty
    self.introText = introText
    self.introInteraction = introInteraction
    self.questChainDict = questChainDict
    self.questChainTextDict = questChainTextDict
    self.neededReputation = neededReputation

  def getQuestName(self):
    return self.questName
  def getDifficulty(self):
    return self.difficulty
  def getIntroText(self):
    return self.introText
  def getIntroInteraction(self):
    return self.introInteraction
  def getQuestChainDict(self):
    return self.questChainDict
  def getQuestChainTextDict(self):
    return self.questChainTextDict
  def getNeededReputation(self):
    return self.neededReputation

class Objective:
  def __init__(self, type, number, location=""):
    self.type = type
    self.number = number
    self.location = location

  def __str__(self):
    if type == "Kill":
      return red + self.type + 