print("Hello World!")

from DiceRollModule import Hitter, Wounder, Saver, SystemObject
import numpy as np
import sys
import os.path
import re
import json

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
    aWounder = createWounder(4, 4, 1, 1, mortalRoll=[6, 1], mortalIsModified=False)
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


def createHitter(bs, rerolls='none', hitModifier=0, autoWoundRoll=100, autoWoundIsModified=False, autoHit=False,
                 mortalWound=None, mortalWoundIsModified=False, explodingHits=None, explodingHitsModified=False):
    if mortalWound is None:
        mortalWound = []
    if explodingHits is None:
        explodingHits = []
    output = Hitter(bs)
    output.myDiceModifier = hitModifier
    output.myRerollType = rerolls
    output.myAutoWound = autoWoundRoll
    output.myAutoWoundIsModified = autoWoundIsModified
    output.myAutoSuccess = autoHit
    output.myMortalWound = mortalWound
    output.myMortalWoundIsModified = mortalWoundIsModified
    output.myExplodingHits = explodingHits
    output.myExplodingHitsIsModified = explodingHitsModified
    return output


def createWounder(strength, toughness, baseAp, baseDamage, rerolls='none', woundModifier=0, rendRoll=[],
                  rendIsModified=False, mortalRoll=[], mortalIsModified=False):
    output = Wounder(strength, toughness, baseDamage, baseAp)
    output.myRerollType = rerolls
    output.myDiceModifier = woundModifier
    output.myRending = rendRoll
    output.myRendingIsModified = rendIsModified
    output.myMortalWounds = mortalRoll
    output.myMortalWoundsIsModified = mortalIsModified
    return output


def createTarget(armourSave, invunerableSave, fnp, wounds, halveDamage=False, reduceDamageBy1=False):
    output = Saver(armourSave, invunerableSave, fnp, wounds)
    output.myHalveDamage = halveDamage
    output.myReduceDamageBy1 = reduceDamageBy1
    return output


def processOffense(offensiveDict):
    stats = [0, 0, 0, 0]
    # number of wounds to guardsman
    [lemanRussTarget, lemanRussToughness] = createLemanRussDefence()
    [custodesTarget, custodesToughness] = createCustodes()
    [primarisTarget, primarisToughness] = createPrimarisMarine()
    [guardTarget, guardToughness] = createGuardsman()
    mortalWoundForHitter = [offensiveDict["mortalWoundToHitRoll"], offensiveDict["mortalWoundToHitBonus"]]
    explodingHitsForHitter = [offensiveDict["extraHitsRoll"], offensiveDict["extraHitsBonus"]]
    hitter = createHitter(offensiveDict["numAttacks"], rerolls=offensiveDict["hitReroll"],
                          hitModifier=offensiveDict["hitModifier"], autoWoundRoll=offensiveDict["hitModifier"],
                          autoWoundIsModified=offensiveDict["hitModifier"], autoHit=offensiveDict["autoSuccess"],
                          mortalWound=mortalWoundForHitter, mortalWoundIsModified=offensiveDict["mortalWoundToHitRollIsModified"],
                          explodingHits=explodingHitsForHitter, explodingHitsModified=offensiveDict["extraHitsIsModified"])
    strength = offensiveDict["strength"]
    mortalWoundsForWounder = [offensiveDict["mortalWoundToWoundRoll"], offensiveDict["mortalWoundsToWoundBonus"]]
    explodingDamage = [offensiveDict["explodingDamageRoll"], offensiveDict["explodingDamageBonus"]]
    rending = [offensiveDict["rendRoll"], offensiveDict["rendBonus"]]
    wounder = createWounder(strength, lemanRussToughness, offensiveDict["baseAp"], offensiveDict["baseDamage"],
                            rerolls=offensiveDict["woundReroll"], woundModifier=offensiveDict["woundModifier"],
                            rendRoll=rending, rendIsModified=offensiveDict["rendIsModified"],
                            mortalRoll=mortalWoundsForWounder, mortalIsModified=offensiveDict["rendIsModified"])
    systemObject = SystemObject(hitter, wounder, lemanRussTarget, offensiveDict["numAttacks"])
    print("Processing Leman Russ")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[0] = np.mean(systemObject.myLostModels)

    wounder.mySuccessRoll = wounder.calculateSuccessRoll(strength, custodesToughness)
    systemObject = SystemObject(hitter, wounder, custodesTarget, offensiveDict["numAttacks"])
    print("Processing Custodes")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[1] = np.mean(systemObject.myLostModels)

    wounder.mySuccessRoll = wounder.calculateSuccessRoll(strength, primarisToughness)
    systemObject = SystemObject(hitter, wounder, primarisTarget, offensiveDict["numAttacks"])
    print("Processing Primaris Marine")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[2] = np.mean(systemObject.myLostModels)

    wounder.mySuccessRoll = wounder.calculateSuccessRoll(strength, guardToughness)
    systemObject = SystemObject(hitter, wounder, guardTarget, offensiveDict["numAttacks"])
    print("Processing Guardsman")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[3] = np.mean(systemObject.myLostModels)

    return stats


def processDefense(defensiveDict):
    stats = [1, 2, 3, 4]

    hitter, wounder, numShots = createBolters()
    target = createTarget(defensiveDict["armourSave"], defensiveDict["invulnerableSave"], defensiveDict["fnp"], defensiveDict["woundCharacteristic"],
                          halveDamage=defensiveDict["halveDamage"], reduceDamageBy1=defensiveDict["reduceDamageByOne"])
    wounder.calculateSuccessRoll(wounder.myStrength, defensiveDict["toughness"])
    wounder.myDiceModifier -= defensiveDict["woundModifier"]
    hitter.myDiceModifier -= defensiveDict["hitModifier"]

    systemObject = SystemObject(hitter, wounder, target, numShots)
    print("Processing Bolters")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[0] = np.mean(systemObject.myLostModels)

    hitter, wounder, numShots = createLascannons()
    wounder.calculateSuccessRoll(wounder.myStrength, defensiveDict["toughness"])
    wounder.myDiceModifier -= defensiveDict["woundModifier"]
    hitter.myDiceModifier -= defensiveDict["hitModifier"]
    target.myModelObject.reset()
    systemObject = SystemObject(hitter, wounder, target, numShots)
    print("Processing Lascannons")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[1] = np.mean(systemObject.myLostModels)

    hitter, wounder, numShots = createBroadsideHighYieldMissilePods()
    wounder.calculateSuccessRoll(wounder.myStrength, defensiveDict["toughness"])
    wounder.myDiceModifier -= defensiveDict["woundModifier"]
    hitter.myDiceModifier -= defensiveDict["hitModifier"]
    target.myModelObject.reset()
    systemObject = SystemObject(hitter, wounder, target, numShots)
    print("Processing High Yield Missile Pods")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[2] = np.mean(systemObject.myLostModels)

    hitter, wounder, numShots = createScoutSniper()
    wounder.calculateSuccessRoll(wounder.myStrength, defensiveDict["toughness"])
    wounder.myDiceModifier -= defensiveDict["woundModifier"]
    hitter.myDiceModifier -= defensiveDict["hitModifier"]
    target.myModelObject.reset()
    systemObject = SystemObject(hitter, wounder, target, numShots)
    print("Processing Snipers")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats[3] = np.mean(systemObject.myLostModels)

    return stats


def processProfile(rangeFileName, meleeFileName, defensiveFileName, outputFileName):
    range_file = open(rangeFileName, "r")
    melee_file = open(meleeFileName, "r")
    defense_file = open(defensiveFileName, "r")
    output_file = open(outputFileName, "w+")
    rangeOutput = [0, 0, 0, 0]
    meleeOutput = [0, 0, 0, 0]
    defenseOutput = [0, 0, 0, 0]
    print("Processing Ranged Profile")
    line = range_file.readline()
    while line:
        line_dict = json.loads(line)
        rangeOutput = np.add(processOffense(line_dict), rangeOutput)
        line = range_file.readline()

    print("Processing Melee Profile")
    line = melee_file.readline()
    while line:
        line_dict = json.loads(line)
        meleeOutput = np.add(processOffense(line_dict), meleeOutput)
        line = melee_file.readline()

    print("Processing Defensive Profile")
    line = defense_file.readline()
    while line:
        line_dict = json.loads(line)
        defenseOutput = np.add(processDefense(line_dict), defenseOutput)
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
line = line[:-1]
rangeFileNames = []
meleeFileNames = []
defensiveFileNames = []
outputFileNames = []
fileCounter = 0
while line:
    line = line[:-1]
    rangeFileNames.append(line + "_ranged.csv")
    meleeFileNames.append(line + "_melee.csv")
    defensiveFileNames.append(line + "_defense.csv")
    outputFileNames.append(line + "_output.csv")
    fileCounter += 1
    line = file.readline()

for i in range(0, fileCounter):
    processProfile(rangeFileNames[i], meleeFileNames[i], defensiveFileNames[i], outputFileNames[i])
    print("Processed data-set ", outputFileNames[i].split("_")[0])
