print("Hello World!")

from DiceRollModule import Hitter, Wounder, Saver, SystemObject
import numpy as np
import sys
import os.path

def createHitter(bs, rerolls='none', hitModifier=0, autoWoundModified=100, autoWoundUnmodified=100, autoHit=False,
                 mortalWound=None, mortalWoundIsModified=False, explodingHits=None, explodingHitsModified=False):
    if mortalWound is None:
        mortalWound = []
    if explodingHits is None:
        explodingHits = []
    output = Hitter(bs)
    output.myDiceModifier = hitModifier
    output.myRerollType = rerolls
    output.myAutoWound = autoWoundUnmodified
    output.myAutoWoundModified = autoWoundModified
    output.myAutoSuccess = autoHit
    output.myMortalWound = mortalWound
    output.myMortalWoundIsModified = mortalWoundIsModified
    output.myExplodingHits = explodingHits
    output.myExplodingHitsIsModified = explodingHitsModified
    return output


def createWounder(strength, toughness, baseAp, baseDamage, rerolls='none', woundModifier=0, rendDiceRoll=100,
                  rendIsModified=False, rendBonus=0, mortalDiceRoll=100, mortalIsModified=False, mortalBonus='0'):
    output = Wounder(strength, toughness, baseAp, baseDamage)
    output.myRerollType = rerolls
    output.myDiceModifier = woundModifier
    output.myRending = [rendDiceRoll, rendBonus]
    output.myRendingIsModified = rendIsModified
    output.myMortalWounds = [mortalDiceRoll, mortalBonus]
    output.myMortalWoundsIsModified = mortalIsModified
    return output


def createTarget(armourSave, invunerableSave, fnp, wounds, halveDamage=False, reduceDamageBy1=False):
    output = Saver(armourSave, invunerableSave, fnp, wounds)
    output.myHalveDamage = halveDamage
    output.myReduceDamageBy1 = reduceDamageBy1
    return output

def processOffense(offensiveList):
    stats = [4, 5, 6]
    return stats


def processDefense(defensiveList):
    stats = [1, 2, 3]
    return stats

def processProfile(rangeFileName, meleeFileName, defensiveFileName, outputFileName):
    output_file = open(outputFileName, "w+")
    range_file = open(rangeFileName, "r")
    melee_file = open(meleeFileName, "r")
    defense_file = open(defensiveFileName, "r")
    rangeOutput = [0, 0, 0]
    meleeOutput = [0, 0, 0]
    defenseOutput = [0, 0, 0]
    line = range_file.readline()
    while line:
        rangeOutput = np.add(processOffense(line), rangeOutput)
        line = rangeFileName.readline()
    line = melee_file.readline()
    while line:
        meleeOutput = np.add(processOffense(line), meleeOutput)
        line = melee_file.readline()
    line = defense_file.readline()
    while line:
        defenseOutput = np.add(processOffense(line), defenseOutput)
        line = melee_file.readline()
    output_file.write(str(rangeOutput.join(",") + "\n"))
    output_file.write(str(meleeOutput.join(",") + "\n"))
    output_file.write(str(defenseOutput.join(",") + "\n"))
    output_file.close()
    range_file.close()
    melee_file.close()
    defense_file.close()








if len(sys.argv) != 2:
    print("Not enought arguments, expected 2, recieved ", len(sys.argv))

fileNamesCsv = sys.argv[1]
file = None
try:
    file = open(fileNamesCsv, 'r')
except IOError:
    print("Unable to open file ", fileNamesCsv, ", program is exiting")
    quit()

line = file.readline()
rangeFileNames = []
meleeFileNames = []
defensiveFileNames = []
outputFileNames = []
fileCounter = 0
while line:
    rangeFileNames.append(line + "_range.csv")
    meleeFileNames.append(line + "_melee.csv")
    defensiveFileNames.append(line + "_defense.csv")
    outputFileNames.append(line + "_output.csv")
    fileCounter += 1
    line = file.readline()

for i in range(0, fileCounter):
    processProfile(rangeFileNames[i], meleeFileNames[i], defensiveFileNames[i])
    print("Processed data-set ", outputFileNames[i].split("_")[0])


numIterations = 10000

numShots = 12
balisticSkill = 3
reRolls = 'none'
hitModifier = 0
explodingSix = []

strength = 10
toughness = 5
armourSave = 2
invunSave = 8
fnp = 7
damage = 'D6'
ap = 3
woundCharacteristic = 4
woundReRoll = 'none'
# 553753
# 209517

aHitter = Hitter(balisticSkill)
aHitter.myDiceModifier = hitModifier
aHitter.myRerollType = reRolls
aHitter.myExplodingHits = explodingSix
aHitter.myExplodingHitsIsModified = False

aWounder = Wounder(strength, toughness, damage, ap)

aSaver = Saver(armourSave, invunSave, fnp, woundCharacteristic)

aSystemObject = SystemObject(aHitter, aWounder, aSaver, numShots)

for i in range(0, numIterations):
    aSystemObject()

aSystemObject.finalise()
