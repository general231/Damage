import re

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
    autoWoundIsModified = 0
    if testForBooleanString(input("Does the unit auto wound? ")):
        autoWoundRoll = testForPositiveIntegerString(input("Dice roll for auto wounding: "))
        autoWoundIsModified = testForBooleanString(input("Is the dice roll modifiable? "))

    rendRoll = 7
    rendBonus = 0
    rendIsModified = 0
    if testForBooleanString(input("Does the unit rend? ")):
        rendRoll = testForPositiveIntegerString(input("Dice roll for rending: "))
        rendIsModified = testForBooleanString(input("is the dice roll modifiable? "))
        rendBonus = testForPositiveIntegerString(input("Enter the bonus to AP for rending: "))

    extraHitsRoll = 7
    extraHitsIsModified = 0
    if testForBooleanString(input("Does the unit generate extra hits? ")):
        extraHitsRoll = testForPositiveIntegerString(input("Dice roll for extra hits: "))
        extraHitsIsModified = testForBooleanString(input("is the dice roll modifiable? "))

    mortalWoundToHitRoll = 7
    mortalWoundToHitRollIsModified = 0
    if testForBooleanString(input("Does the unit generate additonal mortal wound on hit rolls? ")):
        mortalWoundToHitRoll = testForPositiveIntegerString(input("Dice roll for mortal wounds: "))
        mortalWoundToHitRollIsModified = testForBooleanString(input("is the dice roll modifiable? "))

    mortalWoundToWoundRoll = 7
    mortalWoundToWoundRollIsModified = 0
    mortalWoundsToWoundBonus = 0
    if testForBooleanString(input("Does the unit generate mortal wounds on wound rolls? ")):
        mortalWoundToWoundRoll = testForPositiveIntegerString(input("Dice roll for mortal wounds: "))
        mortalWoundToWoundRollIsModified = testForBooleanString(input("is the dice roll modifiable? "))
        mortalWoundsToWoundBonus = input("Enter the bonus mortal wounds: ")

    explodingDamageRoll = 7
    explodingDamageBonus = 0
    explodingDamageIsModified = 0
    if testForBooleanString(input("Does the wound roll generate extra damage? ")):
        explodingDamageRoll = testForPositiveIntegerString(input("Dice roll for bonus damage: "))
        explodingDamageBonus = testForPositiveIntegerString(input("is the dice roll modifiable? "))
        explodingDamageIsModified = testForBooleanString(input("Enter the bonus to damage for rending: "))

    toWrite = [numAttacks, hitRoll, strength, baseAp, baseDamage, hitModifier, hitReroll, woundModifier, woundReroll,
               autoSuccess, autoWoundRoll, autoWoundIsModified, extraHitsRoll, extraHitsIsModified, mortalWoundToHitRoll,
               mortalWoundToHitRollIsModified, mortalWoundToWoundRoll, mortalWoundToWoundRollIsModified,
               mortalWoundsToWoundBonus, rendRoll, rendIsModified, rendBonus, explodingDamageRoll,
               explodingDamageIsModified, explodingDamageBonus]
    file = open(fileName, 'a')
    file.write(','.join(map(str, toWrite))+"\n")
    file.close()

def createDefensiveProfile(unitName):
    toughness = testForPositiveIntegerString(input("Please enter toughness "))
    armourSave = testForPositiveIntegerString(input("Please enter armour save "))
    invulnerableSave = testForPositiveIntegerString(input("Please enter invulnerable save "))
    fnp = testForPositiveIntegerString(input("Please enter feel no pain "))
    wounds = testForPositiveIntegerString(input("Please enter wounds characteristic "))
    hitModifier = testForIntegerString(input("Please enter the hit modifier "))
    woundModifier = testForIntegerString(input("Please enter the wound modifier "))
    reduceDamageByOne = testForBooleanString(input("Does the unit reduce damage by 1 "))
    halveDamage = testForBooleanString(input("Does the unit halve damage "))

    toWrite = [toughness, armourSave, invulnerableSave, fnp, wounds, hitModifier, woundModifier, reduceDamageByOne, halveDamage]
    file = open(unitName+"_defense.csv", 'a')
    file.write(','.join(map(str, toWrite)))
    file.close()


def testForBooleanString(testString):
    isValid = re.search(r"y|yes|n|no", testString.lower()) is not None
    while not isValid:
        testString = input("Please try again, valid responses are \"y, yes, n, no\" ")
        isValid = re.search(r"y|yes|n|no", testString.lower()) is not None
    if re.search(r"y|yes", testString.lower()) is not None:
        return 1
    return 0


def testForPositiveIntegerString(testString):
    while not testString.isdecimal():
        testString = input("Please try again, valid responses are positive integers ")
    return int(testString)


def testForIntegerString(testString):
    multiplier = 1
    if testString[0] == "-":
        testString = testString[1:]
        multiplier = -1
    while not testString.isdecimal():
        testString = input("Please try again, valid responses are positive integers ")
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