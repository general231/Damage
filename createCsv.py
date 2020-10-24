import re
import json

print("Hello World!")


def createMeleeWeapon(name):
    createOffensiveProfile(name + "_melee.csv")


def createRangedWeapon(name):
    createOffensiveProfile(name + "_ranged.csv")


def createOffensiveProfile(fileName):
    numAttacks = input(" please enter the total number attacks with this profile: ")
    hitRoll = testForPositiveIntegerString(input("Please enter the hit roll: "))
    strength = testForPositiveIntegerString(input("Please enter weapon strength: "))
    baseAp = testForPositiveIntegerString(input("Please enter weapon base AP: "))
    baseDamage = input("Please enter weapon base damage: ")
    hitModifier = 0
    hitReroll = "None"
    woundModifier = 0
    woundReroll = "None"
    autoSuccess = False
    autoWoundRoll = 7
    autoWoundIsModified = False
    rendRoll = 7
    rendBonus = 0
    rendIsModified = False
    extraHitsRoll = 7
    extraHitsBonus = 0
    extraHitsIsModified = False
    mortalWoundToHitRoll = 7
    mortalWoundToHitBonus = 0
    mortalWoundToHitRollIsModified = False
    mortalWoundToWoundRoll = 7
    mortalWoundToWoundRollIsModified = 0
    mortalWoundsToWoundBonus = False
    explodingDamageRoll = 7
    explodingDamageBonus = 0
    explodingDamageIsModified = False
    if not testForBooleanString(input("Is this a vanilla profile? ")):
        hitModifier = testForIntegerString(input("Please enter the hit modifier: "))
        hitReroll = input(
            "Please enter the hit reroll, acceptable answers are 'ones', 'all', 'failed', anything else will "
            "be considered as no reroll: ")
        woundModifier = testForIntegerString(input("Please enter the wound modifier: "))
        woundReroll = input(
            "Please enter the wound reroll, acceptable answers are 'ones', 'all', 'failed', anything else"
            " will be considered as no reroll ")
        autoSuccess = testForBooleanString(input("Does the attack always hit? "))

        if testForBooleanString(input("Does the unit auto wound? ")):
            autoWoundRoll = testForPositiveIntegerString(input("Dice roll for auto wounding: "))
            autoWoundIsModified = testForBooleanString(input("Is the dice roll modifiable? "))

        if testForBooleanString(input("Does the unit rend? ")):
            rendRoll = testForPositiveIntegerString(input("Dice roll for rending: "))
            rendIsModified = testForBooleanString(input("is the dice roll modifiable? "))
            rendBonus = testForPositiveIntegerString(input("Enter the bonus to AP for rending: "))

        if testForBooleanString(input("Does the unit generate extra hits? ")):
            extraHitsRoll = testForPositiveIntegerString(input("Dice roll for extra hits: "))
            extraHitsBonus = testForPositiveIntegerString(input("Number of extra hits: "))
            extraHitsIsModified = testForBooleanString(input("is the dice roll modifiable? "))

        if testForBooleanString(input("Does the unit generate additonal mortal wound on hit rolls? ")):
            mortalWoundToHitRoll = testForPositiveIntegerString(input("Dice roll for mortal wounds: "))
            mortalWoundToHitBonus = testForDiceString(input("Bonus mortal wounds: "))
            mortalWoundToHitRollIsModified = testForBooleanString(input("is the dice roll modifiable? "))

        if testForBooleanString(input("Does the unit generate mortal wounds on wound rolls? ")):
            mortalWoundToWoundRoll = testForPositiveIntegerString(input("Dice roll for mortal wounds: "))
            mortalWoundToWoundRollIsModified = testForBooleanString(input("is the dice roll modifiable? "))
            mortalWoundsToWoundBonus = input("Enter the bonus mortal wounds: ")

        if testForBooleanString(input("Does the wound roll generate extra damage? ")):
            explodingDamageRoll = testForPositiveIntegerString(input("Dice roll for bonus damage: "))
            explodingDamageBonus = testForPositiveIntegerString(input("is the dice roll modifiable? "))
            explodingDamageIsModified = testForBooleanString(input("Enter the bonus to damage for rending: "))

    toWrite_dict = {"hitRoll": hitRoll, "numAttacks": numAttacks, "strength": strength, "baseAp": baseAp,
                    "baseDamage": baseDamage, "hitModifier": hitModifier, "hitReroll": hitReroll,
                    "woundModifier": woundModifier, "woundReroll": woundReroll, "autoSuccess": autoSuccess,
                    "autoWoundRoll": autoWoundRoll, "autoWoundIsModified": autoWoundIsModified,
                    "extraHitsRoll": extraHitsRoll, "extraHitsBonus": extraHitsBonus,
                    "extraHitsIsModified": extraHitsIsModified, "mortalWoundToHitRoll": mortalWoundToHitRoll,
                    "mortalWoundToHitBonus": mortalWoundToHitBonus,
                    "mortalWoundToHitRollIsModified": mortalWoundToHitRollIsModified,
                    "mortalWoundToWoundRoll": mortalWoundToWoundRoll,
                    "mortalWoundsToWoundBonus": mortalWoundsToWoundBonus,
                    "mortalWoundToWoundRollIsModified": mortalWoundToWoundRollIsModified, "rendRoll": rendRoll,
                    "rendBonus": rendBonus, "rendIsModified": rendIsModified,
                    "explodingDamageRoll": explodingDamageRoll, "explodingDamageIsModified": explodingDamageIsModified,
                    "explodingDamageBonus": explodingDamageBonus}

    toWrite_json = json.dumps(toWrite_dict)

    file = open(fileName, 'a')
    file.write(toWrite_json + "\n")
    file.close()


def createDefensiveProfile(name):
    toughness = testForPositiveIntegerString(input("Please enter toughness "))
    armourSave = testForPositiveIntegerString(input("Please enter armour save "))
    invulnerableSave = testForPositiveIntegerString(input("Please enter invulnerable save "))
    fnp = testForPositiveIntegerString(input("Please enter feel no pain "))
    woundCharacteristic = testForPositiveIntegerString(input("Please enter wounds characteristic "))

    hitModifier = 0
    woundModifier = 0
    reduceDamageByOne = False
    halveDamage = False
    if not testForBooleanString(input("Is this a vanilla profile? ")):
        hitModifier = testForIntegerString(input("Please enter the hit modifier "))
        woundModifier = testForIntegerString(input("Please enter the wound modifier "))
        reduceDamageByOne = testForBooleanString(input("Does the unit reduce damage by 1 "))
        halveDamage = testForBooleanString(input("Does the unit halve damage "))

    toWrite_dict = {"toughness": toughness, "armourSave": armourSave, "invulnerableSave": invulnerableSave, "fnp": fnp,
                    "woundCharacteristic": woundCharacteristic, "hitModifier": hitModifier,
                    "woundModifier": woundModifier, "reduceDamageByOne": reduceDamageByOne, "halveDamage": halveDamage}

    toWrite_json = json.dumps(toWrite_dict)

    file = open(name + "_defense.csv", 'a')
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
