print("Hello World!")

from DiceRollModule import Hitter, Wounder, Saver, SystemObject
import numpy as np
import sys
import os.path

NUM_ITERATIONS = 10000


def createBolters():
    return 1


def createLascannons():
    return 1


def createAvengerGatlingCannon():
    return 1


def createLemanRussDefence():
    return createTarget(3, 7, 7, 12), 8


def createPrimarisMarine():
    return createTarget(3, 7, 7, 2), 4


def createCustodes():
    return createTarget(2, 4, 7, 3), 5


def createGuardsman():
    return createTarget(4, 7, 7, 1), 3


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
    stats = [0, 0, 0, 0]
    # number of wounds to guardsman
    [lemanRussTarget, lemanRussToughness] = createLemanRussDefence()
    [custodesTarget, custodesToughness] = createCustodes()
    [primarisTarget, primarisToughness] = createPrimarisMarine()
    [guardTarget, guardToughness] = createGuardsman()
    hitter = createHitter(offensiveList[1], rerolls=offensiveList[2], hitModifier=offensiveList[3],
                          autoWoundModified=offensiveList[4], autoWoundUnmodified=offensiveList[5],
                          autoHit=offensiveList[6], mortalWound=offensiveList[7], mortalWoundIsModified=offensiveList[8],
                          explodingHits=offensiveList[9], explodingHitsModified=offensiveList[10])
    strength = offensiveList[11]
    wounder = createWounder(strength, lemanRussToughness, offensiveList[12], offensiveList[13],
                            rerolls=offensiveList[14], woundModifier=offensiveList[15], rendDiceRoll=offensiveList[16],
                            rendIsModified=offensiveList[17], rendBonus=offensiveList[18], mortalDiceRoll=offensiveList[19],
                            mortalIsModified=offensiveList[20], mortalBonus=offensiveList[21])
    systemObject = SystemObject(hitter, wounder, lemanRussTarget, offensiveList[0])
    while i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[0] = np.mean(systemObject.myLostModels)

    wounder.mySuccessRoll = wounder.calculateSuccessRoll(strength, custodesToughness)
    systemObject = SystemObject(hitter, wounder, custodesTarget, offensiveList[0])
    while i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[1] = np.mean(systemObject.myLostModels)

    wounder.mySuccessRoll = wounder.calculateSuccessRoll(strength, primarisToughness)
    systemObject = SystemObject(hitter, wounder, primarisTarget, offensiveList[0])
    while i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[2] = np.mean(systemObject.myLostModels)

    wounder.mySuccessRoll = wounder.calculateSuccessRoll(strength, guardToughness)
    systemObject = SystemObject(hitter, wounder, guardTarget, offensiveList[0])
    while i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[3] = np.mean(systemObject.myLostModels)

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
