print("Hello World!")

from DiceRollModule import Hitter, Wounder, Saver, SystemObject
import numpy as np
import sys
import os.path
import re

NUM_ITERATIONS = 10000

# 10 tactical marines with bolters in rapidfire range
def createBolters():
    aHitter = createHitter(3)
    aWounder = createWounder(4, 4, 0, 1)
    return aHitter, aWounder, 20

# 10 tactical marines with lascannons
def createLascannons():
    aHitter = createHitter(3)
    aWounder = createWounder(9, 4, 4, "D6")
    return aHitter, aWounder, 10

# 3 broadsides with high yield  missile pods
def createBroadsideHighYieldMissilePods():
    aHitter = createHitter(4, 'ones')
    aWounder = createWounder(7, 4, 1, "D3")
    return aHitter, aWounder, 24

# 10 snipers
def createScoutSniper():
    aHitter = createHitter(3)
    aWounder = createWounder(4, 4, 1, 1, mortalDiceRoll=6, mortalIsModified=False, mortalBonus=1)
    return aHitter, aWounder, 10

def createLemanRussDefence():
    return createTarget(3, 7, 7, 12), 8


def createPrimarisMarine():
    return createTarget(3, 7, 7, 2), 4


def createCustodes():
    return createTarget(2, 4, 7, 3), 5


def createGuardsman():
    return createTarget(4, 7, 7, 1), 3

def inputToBool(input):
    test = re.findall(r'[y|yes|1|True|true]', str(input))
    return len(test) != 0


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
    output = Wounder(strength, toughness, baseDamage, baseAp)
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
    hitter = createHitter(offensiveList[1], rerolls=offensiveList[6], hitModifier=offensiveList[5],
                          autoWoundModified=offensiveList[10], autoWoundUnmodified=offensiveList[11],
                          autoHit=inputToBool(offensiveList[9]), mortalWound=offensiveList[13],
                          mortalWoundIsModified=inputToBool(offensiveList[14]),
                          explodingHits=offensiveList[12], explodingHitsModified=inputToBool(offensiveList[13]))
    strength = offensiveList[2]
    wounder = createWounder(strength, lemanRussToughness, offensiveList[3], offensiveList[4],
                            rerolls=offensiveList[8], woundModifier=offensiveList[7], rendDiceRoll=offensiveList[19],
                            rendIsModified=inputToBool(offensiveList[20]), rendBonus=offensiveList[21],
                            mortalDiceRoll=offensiveList[19],
                            mortalIsModified=inputToBool(offensiveList[20]), mortalBonus=offensiveList[21])
    systemObject = SystemObject(hitter, wounder, lemanRussTarget, offensiveList[0])
    print("Processing Leman Russ")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[0] = np.mean(systemObject.myLostModels)

    wounder.mySuccessRoll = wounder.calculateSuccessRoll(strength, custodesToughness)
    systemObject = SystemObject(hitter, wounder, custodesTarget, offensiveList[0])
    print("Processing Custodes")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[1] = np.mean(systemObject.myLostModels)

    wounder.mySuccessRoll = wounder.calculateSuccessRoll(strength, primarisToughness)
    systemObject = SystemObject(hitter, wounder, primarisTarget, offensiveList[0])
    print("Processing Primaris Marine")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[2] = np.mean(systemObject.myLostModels)

    wounder.mySuccessRoll = wounder.calculateSuccessRoll(strength, guardToughness)
    systemObject = SystemObject(hitter, wounder, guardTarget, offensiveList[0])
    print("Processing Guardsman")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[3] = np.mean(systemObject.myLostModels)

    return stats


def processDefense(defensiveList):
    stats = [1, 2, 3, 4]

    hitter, wounder, numShots = createBolters()
    wounder.calculateSuccessRoll(wounder.myStrength, defensiveList[0])
    wounder.myDiceModifier = defensiveList[6]
    hitter.myDiceModifier = defensiveList[5]
    target = createTarget(defensiveList[1], defensiveList[2], defensiveList[3], defensiveList[4],
                          halveDamage=inputToBool(defensiveList[8]), reduceDamageBy1=inputToBool(defensiveList[7]))
    systemObject = SystemObject(hitter, wounder, target, numShots)
    print("Processing Bolters")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[0] = np.mean(systemObject.myLostModels)

    hitter, wounder, numShots = createLascannons()
    wounder.calculateSuccessRoll(wounder.myStrength, defensiveList[0])
    wounder.myDiceModifier = defensiveList[6]
    hitter.myDiceModifier = defensiveList[5]
    target = createTarget(defensiveList[1], defensiveList[2], defensiveList[3], defensiveList[4],
                          halveDamage=defensiveList[8], reduceDamageBy1=defensiveList[7])
    systemObject = SystemObject(hitter, wounder, target, numShots)
    print("Processing Lascannons")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[1] = np.mean(systemObject.myLostModels)

    hitter, wounder, numShots = createBroadsideHighYieldMissilePods()
    wounder.calculateSuccessRoll(wounder.myStrength, defensiveList[0])
    wounder.myDiceModifier = defensiveList[6]
    hitter.myDiceModifier = defensiveList[5]
    target = createTarget(defensiveList[1], defensiveList[2], defensiveList[3], defensiveList[4],
                          halveDamage=defensiveList[8], reduceDamageBy1=defensiveList[7])
    systemObject = SystemObject(hitter, wounder, target, numShots)
    print("Processing High Yield Missile Pods")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[2] = np.mean(systemObject.myLostModels)

    hitter, wounder, numShots = createScoutSniper()
    wounder.calculateSuccessRoll(wounder.myStrength, defensiveList[0])
    wounder.myDiceModifier = defensiveList[6]
    hitter.myDiceModifier = defensiveList[5]
    target = createTarget(defensiveList[1], defensiveList[2], defensiveList[3], defensiveList[4],
                          halveDamage=defensiveList[8], reduceDamageBy1=defensiveList[7])
    systemObject = SystemObject(hitter, wounder, target, numShots)
    print("Processing Snipers")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[3] = np.mean(systemObject.myLostModels)

    return stats


def processProfile(rangeFileName, meleeFileName, defensiveFileName, outputFileName):
    output_file = open(outputFileName, "w+")
    range_file = open(rangeFileName, "r")
    melee_file = open(meleeFileName, "r")
    defense_file = open(defensiveFileName, "r")
    rangeOutput = [0, 0, 0, 0]
    meleeOutput = [0, 0, 0, 0]
    defenseOutput = [0, 0, 0, 0]
    print("Processing Ranged Profile")
    line = range_file.readline()
    while line:
        line_list = re.split(r'[,]', line)
        for i in range(len(line_list)):
            if line_list[i].isdigit():
                line_list[i] = int(line_list[i])
        rangeOutput = np.add(processOffense(line_list), rangeOutput)
        line = range_file.readline()

    print("Processing Melee Profile")
    line = melee_file.readline()
    while line:
        line_list = line.split(',')
        for i in range(len(line_list)):
            if line_list[i].isdigit():
                line_list[i] = int(line_list[i])
        meleeOutput = np.add(processOffense(line_list), meleeOutput)
        line = melee_file.readline()

    print("Processing Defensive Profile")
    line = defense_file.readline()
    while line:
        line_list = line.split(',')
        for i in range(len(line_list)):
            if line_list[i].isdigit():
                line_list[i] = int(line_list[i])
        defenseOutput = np.add(processDefense(line_list), defenseOutput)
        line = melee_file.readline()

    output_file.write(np.array2string(rangeOutput, separator=',') + "\n")
    output_file.write(np.array2string(meleeOutput, separator=',') + "\n")
    output_file.write(np.array2string(defenseOutput, separator=',') + "\n")
    output_file.close()
    range_file.close()
    melee_file.close()
    defense_file.close()


if len(sys.argv) != 2:
    print("Not enough arguments, expected 2, received ", len(sys.argv))
    quit()

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
    rangeFileNames.append(line + "_ranged.csv")
    meleeFileNames.append(line + "_melee.csv")
    defensiveFileNames.append(line + "_defense.csv")
    outputFileNames.append(line + "_output.csv")
    fileCounter += 1
    line = file.readline()

for i in range(0, fileCounter):
    processProfile(rangeFileNames[i], meleeFileNames[i], defensiveFileNames[i], outputFileNames[i])
    print("Processed data-set ", outputFileNames[i].split("_")[0])
