import re
import json

print("Hello World!")


def createMeleeWeapon(unitName):
    createOffensiveProfile(unitName+"_melee.csv")


def createRangedWeapon(unitName):
    createOffensiveProfile(unitName+"_ranged.csv")


def createOffensiveProfile(fileName):
    numAttacks = testForPositiveIntegerString(input(" please enter the total number attacks with this profile: "))
    hitRoll = testForPositiveIntegerString(input("Please enter the hit roll: "))
    strength = testForPositiveIntegerString(input("Please enter weapon strength: "))
    baseAp = testForPositiveIntegerString(input("Please enter weapon base AP: "))
    baseDamage = input("Please enter weapon base damage: ")
    hitModifier = testForIntegerString(input("Please enter the hit modifier: "))
    hitReroll = input("Please enter the hit reroll, acceptable answers are 'ones', 'all', 'failed', anything else will "
                      "be considered as no reroll: ")
    woundModifier = testForIntegerString(input("Please enter the wound modifier: "))
    woundReroll = input("Please enter the wound reroll, acceptable answers are 'ones', 'all', 'failed', anything else"
                        " will be considered as no reroll ")
    autoSuccess = testForBooleanString(input("Does the attack always hit? "))

    autoWoundRoll = 7
    autoWoundIsModified = False
    if testForBooleanString(input("Does the unit auto wound? ")):
        autoWoundRoll = testForPositiveIntegerString(input("Dice roll for auto wounding: "))
        autoWoundIsModified = testForBooleanString(input("Is the dice roll modifiable? "))

    rendRoll = 7
    rendBonus = 0
    rendIsModified = False
    if testForBooleanString(input("Does the unit rend? ")):
        rendRoll = testForPositiveIntegerString(input("Dice roll for rending: "))
        rendIsModified = testForBooleanString(input("is the dice roll modifiable? "))
        rendBonus = testForPositiveIntegerString(input("Enter the bonus to AP for rending: "))

    extraHitsRoll = 7
    extraHitsBonus = 0
    extraHitsIsModified = False
    if testForBooleanString(input("Does the unit generate extra hits? ")):
        extraHitsRoll = testForPositiveIntegerString(input("Dice roll for extra hits: "))
        extraHitsBonus = testForPositiveIntegerString(input("Number of extra hits: "))
        extraHitsIsModified = testForBooleanString(input("is the dice roll modifiable? "))

    mortalWoundToHitRoll = 7
    mortalWoundToHitBonus = 0
    mortalWoundToHitRollIsModified = False
    if testForBooleanString(input("Does the unit generate additonal mortal wound on hit rolls? ")):
        mortalWoundToHitRoll = testForPositiveIntegerString(input("Dice roll for mortal wounds: "))
        mortalWoundToHitBonus = testForDiceString(input("Bonus mortal wounds: "))
        mortalWoundToHitRollIsModified = testForBooleanString(input("is the dice roll modifiable? "))

    mortalWoundToWoundRoll = 7
    mortalWoundToWoundRollIsModified = 0
    mortalWoundsToWoundBonus = False
    if testForBooleanString(input("Does the unit generate mortal wounds on wound rolls? ")):
        mortalWoundToWoundRoll = testForPositiveIntegerString(input("Dice roll for mortal wounds: "))
        mortalWoundToWoundRollIsModified = testForBooleanString(input("is the dice roll modifiable? "))
        mortalWoundsToWoundBonus = input("Enter the bonus mortal wounds: ")

    explodingDamageRoll = 7
    explodingDamageBonus = 0
    explodingDamageIsModified = False
    if testForBooleanString(input("Does the wound roll generate extra damage? ")):
        explodingDamageRoll = testForPositiveIntegerString(input("Dice roll for bonus damage: "))
        explodingDamageBonus = testForPositiveIntegerString(input("is the dice roll modifiable? "))
        explodingDamageIsModified = testForBooleanString(input("Enter the bonus to damage for rending: "))

    toWrite_dict = {}
    toWrite_dict["numAttacks"] = numAttacks
    toWrite_dict["strength"] = strength
    toWrite_dict["baseAp"] = baseAp
    toWrite_dict["baseDamage"] = baseDamage
    toWrite_dict["hitModifier"] = hitModifier
    toWrite_dict["hitReroll"] = hitReroll
    toWrite_dict["woundModifier"] = woundModifier
    toWrite_dict["woundReroll"] = woundReroll
    toWrite_dict["autoSuccess"] = autoSuccess
    toWrite_dict["autoWoundRoll"] = autoWoundRoll
    toWrite_dict["autoWoundIsModified"] = autoWoundIsModified
    toWrite_dict["extraHitsRoll"] = extraHitsRoll
    toWrite_dict["extraHitsBonus"] = extraHitsBonus
    toWrite_dict["extraHitsIsModified"] = extraHitsIsModified
    toWrite_dict["mortalWoundToHitRoll"] = mortalWoundToHitRoll
    toWrite_dict["mortalWoundToHitBonus"] = mortalWoundToHitBonus
    toWrite_dict["mortalWoundToHitRollIsModified"] = mortalWoundToHitRollIsModified
    toWrite_dict["mortalWoundToWoundRoll"] = mortalWoundToWoundRoll
    toWrite_dict["mortalWoundsToWoundBonus"] = mortalWoundsToWoundBonus
    toWrite_dict["mortalWoundToWoundRollIsModified"] = mortalWoundToWoundRollIsModified
    toWrite_dict["rendRoll"] = rendRoll
    toWrite_dict["rendBonus"] = rendBonus
    toWrite_dict["rendIsModified"] = rendIsModified
    toWrite_dict["explodingDamageRoll"] = explodingDamageRoll
    toWrite_dict["explodingDamageIsModified"] = explodingDamageIsModified
    toWrite_dict["explodingDamageBonus"] = explodingDamageBonus

    toWrite_json = json.dumps(toWrite_dict)

    file = open(fileName, 'a')
    file.write(toWrite_json +"\n")
    file.close()

def createDefensiveProfile(unitName):
    toughness = testForPositiveIntegerString(input("Please enter toughness "))
    armourSave = testForPositiveIntegerString(input("Please enter armour save "))
    invulnerableSave = testForPositiveIntegerString(input("Please enter invulnerable save "))
    fnp = testForPositiveIntegerString(input("Please enter feel no pain "))
    woundCharacteristic = testForPositiveIntegerString(input("Please enter wounds characteristic "))
    hitModifier = testForIntegerString(input("Please enter the hit modifier "))
    woundModifier = testForIntegerString(input("Please enter the wound modifier "))
    reduceDamageByOne = testForBooleanString(input("Does the unit reduce damage by 1 "))
    halveDamage = testForBooleanString(input("Does the unit halve damage "))

    toWrite_dict = {}
    toWrite_dict["toughness"] = toughness
    toWrite_dict["armourSave"] = armourSave
    toWrite_dict["invulnerableSave"] = invulnerableSave
    toWrite_dict["fnp"] = fnp
    toWrite_dict["woundCharacteristic"] = woundCharacteristic
    toWrite_dict["hitModifier"] = hitModifier
    toWrite_dict["woundModifier"] = woundModifier
    toWrite_dict["reduceDamageByOne"] = reduceDamageByOne
    toWrite_dict["halveDamage"] = halveDamage

    toWrite_json = json.dumps(toWrite_dict)

    file = open(unitName+"_defense.csv", 'a')
    file.write(toWrite_json)
    file.close()


def testForBooleanString(testString):
    isValid = re.search(r"y|yes|n|no", testString.lower()) is not None
    while not isValid:
        testString = input("Please try again, valid responses are \"y, yes, n, no\" ")
        isValid = re.search(r"y|yes|n|no", testString.lower()) is not None
    if re.search(r"y|yes", testString.lower()) is not None:
        return True
    return False


def testForPositiveIntegerString(testString):
    while not testString.isdecimal():
        testString = input("Please try again, valid responses are positive integers ")
    return int(testString)


def testForDiceString(testString):
    return testString


def testForIntegerString(testString):
    multiplier = 1
    while not testString.isdecimal():
        testString = input("Please try again, valid responses are positive integers ")
    if testString[0] == "-":
        testString = testString[1:]
        multiplier = -1
    return multiplier * int(testString)


unitName = input("What is the unit name? ").replace(" ", "-")
print("Creating ranged weapons")
booleanAnswer = input("Does this unit have a ranged weapon? ")
while testForBooleanString(booleanAnswer) == 1:
    createRangedWeapon(unitName)
    booleanAnswer = input("Does this unit have more then one profile? ")

print("Creating melee weapons")
booleanAnswer = input("Does this unit have a melee weapon? ")
while testForBooleanString(booleanAnswer) == 1:
    createMeleeWeapon(unitName)
    booleanAnswer = input("Does this unit have more then one profile? ")

print("Creating defensive profile")
createDefensiveProfile(unitName)