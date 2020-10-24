print("Hello World!")

from DiceRollModule import Hitter, Wounder, Saver, SystemObject
import numpy as np
import sys
import os.path
import re
import json
import time

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


# create a lemanRuss
def createLemanRussDefence():
    return createTarget(3, 7, 7, 12), 8


# create a bog standard primaris marine
def createPrimarisMarine():
    return createTarget(3, 7, 7, 2), 4


# create a custodes, the emperors shiniest
def createCustodes():
    return createTarget(2, 4, 7, 3), 5


# create a guardsman
def createGuardsman():
    return createTarget(4, 7, 7, 1), 3


# this converts any of the various ways of saying true or false to a python bool
def inputToBool(input):
    test = re.findall(r'[y|yes|1|True|true]', str(input))
    return len(test) != 0


# sums values in the dictionary, this assumes every key in dict1 is also in dict2
def addNumericalDictionaries(dict1, dict2):
    for key, value in dict1.items():
        dict2[key] = dict2[key] + dict1[key]
    return dict2


# a simpe factory for building a hitter object
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


# a simple factory for creating a wounder, rendRoll and mortalWound needs to be in the format the wounder wants because
# I didnt want to add 2 extra arguments and a check for both
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


# a simple factory for creating a target object
def createTarget(armourSave, invunerableSave, fnp, wounds, halveDamage=False, reduceDamageBy1=False, transHuman=False):
    output = Saver(armourSave, invunerableSave, fnp, wounds)
    output.myHalveDamage = halveDamage
    output.myReduceDamageBy1 = reduceDamageBy1
    output.myTransHuman = transHuman
    return output


def updateOffense(oldDict):
    newDict = {"hitRoll": 7, "numAttacks": 0, "strength": 0, "baseAp": 0, "baseDamage": 0, "hitModifier": 0,
               "hitReroll": 0, "woundModifier": 0, "woundReroll": 0, "autoSuccess": False, "autoWoundRoll": 7,
               "autoWoundIsModified": False, "extraHitsRoll": 7, "extraHitsBonus": 0, "extraHitsIsModified": False,
               "mortalWoundToHitRoll": 7, "mortalWoundToHitBonus": 0, "mortalWoundToHitRollIsModified": False,
               "mortalWoundToWoundRoll": 7, "mortalWoundsToWoundBonus": 0, "mortalWoundToWoundRollIsModified": False,
               "rendRoll": 7, "rendBonus": 0, "rendIsModified": False, "explodingDamageRoll": 7,
               "explodingDamageIsModified": False, "explodingDamageBonus": 0}

    for key, value in oldDict.items():
        newDict[key] = value

    return newDict


def updateDefense(oldDict):
    newDict = {"toughness": 0, "armourSave": 7, "invulnerableSave": 7, "fnp": 7, "woundCharacteristic": 0,
               "hitModifier": 0, "woundModifier": 0, "reduceDamageByOne": False, "halveDamage": False,
               "transHuman": False}

    for key, value in oldDict.items():
        newDict[key] = value

    return newDict


# this
def processOffense(offensiveDict):
    offensiveDict = updateOffense(offensiveDict)
    stats = {"lemanRuss": 0, "custodes": 0, "primarisMarine": 0, "imperialGuard": 0}
    # number of wounds to guardsman
    [lemanRussTarget, lemanRussToughness] = createLemanRussDefence()
    [custodesTarget, custodesToughness] = createCustodes()
    [primarisTarget, primarisToughness] = createPrimarisMarine()
    [guardTarget, guardToughness] = createGuardsman()
    mortalWoundForHitter = [offensiveDict["mortalWoundToHitRoll"], offensiveDict["mortalWoundToHitBonus"]]
    explodingHitsForHitter = [offensiveDict["extraHitsRoll"], offensiveDict["extraHitsBonus"]]
    hitter = createHitter(offensiveDict["hitRoll"], rerolls=offensiveDict["hitReroll"],
                          hitModifier=offensiveDict["hitModifier"], autoWoundRoll=offensiveDict["autoWoundRoll"],
                          autoWoundIsModified=offensiveDict["autoWoundIsModified"],
                          autoHit=offensiveDict["autoSuccess"],
                          mortalWound=mortalWoundForHitter,
                          mortalWoundIsModified=offensiveDict["mortalWoundToHitRollIsModified"],
                          explodingHits=explodingHitsForHitter,
                          explodingHitsModified=offensiveDict["extraHitsIsModified"])
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
    stats["lemanRuss"] = np.mean(systemObject.myLostModels)

    wounder.mySuccessRoll = wounder.calculateSuccessRoll(strength, custodesToughness)
    systemObject = SystemObject(hitter, wounder, custodesTarget, offensiveDict["numAttacks"])
    print("Processing Custodes")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats["custodes"] = np.mean(systemObject.myLostModels)

    wounder.mySuccessRoll = wounder.calculateSuccessRoll(strength, primarisToughness)
    systemObject = SystemObject(hitter, wounder, primarisTarget, offensiveDict["numAttacks"])
    print("Processing Primaris Marine")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats["primarisMarine"] = np.mean(systemObject.myLostModels)

    wounder.mySuccessRoll = wounder.calculateSuccessRoll(strength, guardToughness)
    systemObject = SystemObject(hitter, wounder, guardTarget, offensiveDict["numAttacks"])
    print("Processing Guardsman")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats["imperialGuard"] = np.mean(systemObject.myLostModels)

    return stats


def processDefense(defensiveDict):
    defensiveDict = updateDefense(defensiveDict)
    stats = {"bolters": 0, "lascannons": 0, "highYieldMissilePod": 0, "sniper": 0}

    hitter, wounder, numShots = createBolters()
    target = createTarget(defensiveDict["armourSave"], defensiveDict["invulnerableSave"], defensiveDict["fnp"],
                          defensiveDict["woundCharacteristic"], halveDamage=defensiveDict["halveDamage"],
                          reduceDamageBy1=defensiveDict["reduceDamageByOne"], transHuman=defensiveDict["transHuman"])
    wounder.calculateSuccessRoll(wounder.myStrength, defensiveDict["toughness"])
    wounder.myDiceModifier -= defensiveDict["woundModifier"]
    hitter.myDiceModifier -= defensiveDict["hitModifier"]

    systemObject = SystemObject(hitter, wounder, target, numShots)
    print("Processing Bolters")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats["bolters"] = np.mean(systemObject.myLostModels)

    hitter, wounder, numShots = createLascannons()
    wounder.calculateSuccessRoll(wounder.myStrength, defensiveDict["toughness"])
    wounder.myDiceModifier -= defensiveDict["woundModifier"]
    hitter.myDiceModifier -= defensiveDict["hitModifier"]
    target.myModelObject.reset()
    systemObject = SystemObject(hitter, wounder, target, numShots)
    print("Processing Lascannons")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats["lascannons"] = np.mean(systemObject.myLostModels)

    hitter, wounder, numShots = createBroadsideHighYieldMissilePods()
    wounder.calculateSuccessRoll(wounder.myStrength, defensiveDict["toughness"])
    wounder.myDiceModifier -= defensiveDict["woundModifier"]
    hitter.myDiceModifier -= defensiveDict["hitModifier"]
    target.myModelObject.reset()
    systemObject = SystemObject(hitter, wounder, target, numShots)
    print("Processing High Yield Missile Pods")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats["highYieldMissilePod"] = np.mean(systemObject.myLostModels)

    hitter, wounder, numShots = createScoutSniper()
    wounder.calculateSuccessRoll(wounder.myStrength, defensiveDict["toughness"])
    wounder.myDiceModifier -= defensiveDict["woundModifier"]
    hitter.myDiceModifier -= defensiveDict["hitModifier"]
    target.myModelObject.reset()
    systemObject = SystemObject(hitter, wounder, target, numShots)
    print("Processing Snipers")
    for i in range(0, NUM_ITERATIONS):
        systemObject()
    stats["sniper"] = np.mean(systemObject.myLostModels)

    return stats


class DummyFile:
    def readline(self):
        return []

    def close(self):
        pass


def processProfile(rangeFileName, meleeFileName, defensiveFileName, outputFileName):
    range_file = DummyFile()
    try:
        range_file = open(rangeFileName, "r")
    except IOError:
        print("Unable to open ranged weapon file, assuming no ranged weapon")
    try:
        melee_file = open(meleeFileName, "r")
    except Exception as e:
        print("Unable to open melee file")
        raise
    try:
        defense_file = open(defensiveFileName, "r")
    except exception as e:
        print("Unable to open defense file")
        raise
    output_file = open(outputFileName, "w+")
    rangeOutput = {"lemanRuss": 0, "custodes": 0, "primarisMarine": 0, "imperialGuard": 0}
    meleeOutput = {"lemanRuss": 0, "custodes": 0, "primarisMarine": 0, "imperialGuard": 0}
    defenseOutput = {"bolters": 0, "lascannons": 0, "highYieldMissilePod": 0, "sniper": 0}
    print("Processing Ranged Profile")
    line = range_file.readline()
    while line:
        line_dict = json.loads(line)
        rangeOutput = addNumericalDictionaries(processOffense(line_dict), rangeOutput)
        line = range_file.readline()

    print("Processing Melee Profile")
    line = melee_file.readline()
    while line:
        line_dict = json.loads(line)
        meleeOutput = addNumericalDictionaries(processOffense(line_dict), meleeOutput)
        line = melee_file.readline()

    print("Processing Defensive Profile")
    line = defense_file.readline()
    while line:
        line_dict = json.loads(line)
        defenseOutput = addNumericalDictionaries(processDefense(line_dict), defenseOutput)
        line = melee_file.readline()

    output_file.write(json.dumps(rangeOutput) + "\n")
    output_file.write(json.dumps(meleeOutput) + "\n")
    output_file.write(json.dumps(defenseOutput) + "\n")
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
    line = line.replace("\n", "")
    rangeFileNames.append(line + "_ranged.csv")
    meleeFileNames.append(line + "_melee.csv")
    defensiveFileNames.append(line + "_defense.csv")
    outputFileNames.append(line + "_output.csv")
    fileCounter += 1
    line = file.readline()

startTime = time.perf_counter()
for i in range(0, fileCounter):
    try:
        startTime2 = time.perf_counter()
        processProfile(rangeFileNames[i], meleeFileNames[i], defensiveFileNames[i], outputFileNames[i])
        stopTime2 = time.perf_counter()
        print("Processed data-set ", outputFileNames[i].split("_")[0], ", it took ", stopTime2 - startTime2)

    except IOError:
        print("Unable to process ", outputFileNames[i].split("_")[0], ", skipping this datasheet")
stopTime = time.perf_counter()

print("total time to process: ", stopTime - startTime)
