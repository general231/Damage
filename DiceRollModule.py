import random as rand
from math import ceil
from math import floor
import re


# not working:
# attacks causing additional wounds

# This converts a string representing a random or fixed value and converts it to an integer
def diceToNum(value):
    # This converts dice rolls D6, 3D6 etc and gives a integer number out
    value = str(value)
    diceSize = re.findall(r"D(\d+)", value)
    numDice = re.findall(r"(\d+)D", value)
    bonus = re.findall(r"\+(\d+)", value)
    # TODO option for best of 2D6, reroll dice, etc
    if diceSize == []:
        diceSize = 6
    else:
        diceSize = int(diceSize[0])
    if numDice == []:
        numDice = 1
    else:
        numDice = int(numDice[0])
    if bonus == []:
        bonus = 0
    else:
        bonus = int(bonus[0])

    # test for integer input value
    if (value.isdigit()):
        return int(value)

    tempDiceRoller = DiceRoller(int(diceSize))
    totalValue = 0
    for i in range(0, numDice):
        totalValue += tempDiceRoller()

    totalValue += bonus
    return bonus


# This object represents a dice roll, it will return a random integer in the range 1-self.maxValue
class DiceRoller:
    def __init__(self, maxValue):
        self.myMaxValue = maxValue

    def __call__(self, diceToRoll=1):
        if diceToRoll == 1:
            return ceil(self.myMaxValue * rand.random())
        dice_results = []
        for i in range(0, diceToRoll):
            dice_results.append(ceil(self.myMaxValue * rand.random()))
        return dice_results


class DamageObject:
    def __init__(self, type, damage=1, ap=0):
        self.myType = type
        self.myDamage = damage
        self.myAp = ap

    def reduceDamage(self, value):
        tempDamage = self.myDamage - value
        if tempDamage < 1:
            tempDamage = 1
        self.myDamage = tempDamage

    def halveDamage(self):
        self.myDamage = ceil(self.myDamage / 2)


# This object stores the statistics about the model being attacked and makes the FNP rolls
class ModelObject():
    def __init__(self, wounds, fnp):
        self.myWoundCharacteristic = wounds
        self.myFnp = fnp
        self.myLostModelsCounter = 0
        self.myTotalDamageRecieved = 0
        self.myRemainingWounds = self.myWoundCharacteristic
        self.myDiceRoller = DiceRoller(6)

    def applyDamage(self, damage):
        for i in range(0, damage):
            diceValue = self.myDiceRoller()
            if diceValue >= self.myFnp:
                damage -= 1
        self.myRemainingWounds -= damage
        self.myTotalDamageRecieved += damage
        if self.myRemainingWounds <= 0:
            self.myRemainingWounds = self.myWoundCharacteristic
            self.myLostModelsCounter += 1

    def reset(self):
        self.myTotalDamageRecieved = 0
        self.myLostModelsCounter = 0
        self.myRemainingWounds = self.myWoundCharacteristic


# This is the parent class for the Hitter and the Wounder class, it contains the common code for exploding dice,
# rerolls and dice rolls
class SuccessObject:
    def __init__(self, successRoll):
        self.mySuccessRoll = successRoll
        self.myDiceModifier = 0
        self.myRerollType = 'none'

    def _doesItExplode(self, diceValue, diceRequirment, isModified, bonusValue):
        # This function is a generic function to be called when a bonus occurs on a specific value, e.g. exploding  6s
        if isModified:
            diceValue = diceValue - self.myDiceModifier
        if diceValue >= diceRequirment:
            return bonusValue
        return 0

    def _applyReRoll(self, value):
        if self.myRerollType != 'none':
            # This is done so that you cant keep re rolling failed hits when the function calls itself
            tempDiceRoller = DiceRoller(6)
            newDiceRoll = tempDiceRoller()
            if self.myRerollType == 'all':
                if newDiceRoll + self.myDiceModifier >= self.mySuccessRoll:
                    return newDiceRoll
            if self.myRerollType == 'failed' and value < self.mySuccessRoll:
                if newDiceRoll >= self.mySuccessRoll:
                    return newDiceRoll
            if self.myRerollType == 'ones' and value == 1:
                if newDiceRoll + self.myDiceModifier >= self.mySuccessRoll:
                    return newDiceRoll
            return None

    def _doISucceed(self, value):
        if value + self.myDiceModifier >= self.mySuccessRoll and not value <= 1:
            return True
        else:
            return False


# This object rolls the hit roll, it takes in a dice value and will return the number of hits out, the output is a
# list, the possible values are 'fail', 'success', 'mortal' or 'wound'
class Hitter(SuccessObject):
    def __init__(self, successRoll):
        super().__init__(successRoll)
        self.myAutoWoundModified = 100
        self.myAutoWoundUnmodified = 100
        self.myDestroyerMissile = False
        self.myAutoSuccess = False
        self.myAutoWound = 100
        self.myAutoWoundIsModified = False
        self.myMortalWound = []
        self.myMortalWoundIsModified = False
        self.myExplodingHits = []
        self.myExplodingHitsIsModified = False

    def __call__(self, value):
        # this function returns an array of strings, possible results are 'fail', 'success', 'mortal or 'wound' depending
        # on the dice roll, an array is returned because you can generate more hits then dice in
        modifiedValue = value + self.myDiceModifier
        output = []
        if self.myAutoSuccess:
            output.append('success')
            return output
        if modifiedValue >= self.myAutoWound:
            output.append('wound')
            return output
        if len(self.myExplodingHits) != 0:
            output += ['success'] * self._doesItExplode(value, self.myExplodingHits[0],
                                                        self.myExplodingHitsIsModified, self.myExplodingHits[1])
        if len(self.myMortalWound) != 0:
            output += ['mortal'] * self._doesItExplode(value, self.myMortalWound[0],
                                                       self.myExplodingHitsIsModified, self.myMortalWound[1])
        if self._doISucceed(value):
            output.append('success')
        else:
            newDice = self._applyReRoll(value)
            if newDice is not None:
                output += self.__call__(newDice)
            else:
                output.append('fail')
        return output


# This represnts the wound roll for the attack, it takes in the dice value and hit type and returns an array of
# DamageObjects
class Wounder(SuccessObject):
    def __init__(self, strength, toughness, baseDamage, baseAp):
        super().__init__(self.calculateSuccessRoll(strength, toughness))
        self.myStrength = strength
        self.myToughness = toughness
        self.myBaseDamage = baseDamage
        self.myBaseAp = baseAp
        self.myExplodingWounds = []
        self.myExplodingWoundsIsModified = False
        self.myRending = []  # idx 0 is the dice roll, idx 1 is the bonus
        self.myRendingIsModified = False
        self.myExplodingDamage = []  # idx 0 is the dice roll, idx 1 is the bonus
        self.myExplodingDamageIsModified = False
        self.myMortalWounds = []  # idx 0 is the dice roll, idx 1 is the bonus
        self.myMortalWoundsIsModified = False

    def calculateSuccessRoll(self, strength, toughness):
        if strength == toughness:
            successRoll = 4
        elif floor(strength / 2) >= toughness:
            successRoll = 2
        elif strength > toughness:
            successRoll = 3
        elif floor(toughness / 2) >= strength:
            successRoll = 6
        else:
            successRoll = 5
        return successRoll

    def __generateDamageObject(self, type, bonusDamage=0, bonusAp=0):
        output = []
        if type == 'mortal':
            output += [DamageObject('mortal')] * bonusDamage
        else:
            damage = diceToNum(self.myBaseDamage)
            damageObject = DamageObject(type, damage + bonusDamage, self.myBaseAp + bonusAp)
            output.append(damageObject)
        return output

    def __call__(self, diceValue, hitType):
        output = []
        if hitType == 'mortal':
            output += self.__generateDamageObject('mortal', 1)
            return output
        if hitType == 'wound':
            output += self.__generateDamageObject('normal')
            return output
        if hitType == 'fail':
            return output
        if len(self.myRending) != 0:
            rend = self._doesItExplode(diceValue, self.myRending[0], self.myRendingIsModified, self.myRending[1])
            if rend != 0:
                output += self.__generateDamageObject('normal', 0, rend)
                return output
        if len(self.myExplodingDamage) != 0:
            bonusDamage = diceToNum(self._doesItExplode(diceValue, self.myExplodingDamage[0],
                                                        self.myExplodingDamageIsModified, self.myExplodingDamage[1]))
            if bonusDamage != 0:
                output += self.__generateDamageObject('normal', bonusDamage)
                return output
        if len(self.myMortalWounds) != 0:
            numMortalWounds = diceToNum(self._doesItExplode(diceValue, self.myMortalWounds[0],
                                                            self.myMortalWoundsIsModified, self.myMortalWounds[1]))
            output += self.__generateDamageObject('mortal', numMortalWounds)
        if len(self.myExplodingWounds) != 0:
            output += self.__generateDamageObject('normal') * self._doesItExplode(diceValue, self.myExplodingWounds[0],
                                                                                  self.myExplodingWoundsIsModified,
                                                                                  self.myExplodingWounds[1])
        if self._doISucceed(diceValue):
            output += self.__generateDamageObject('normal')
        else:
            newDice = self._applyReRoll(diceValue)
            if newDice is not None:
                output += self.__call__(newDice)
        return output


# This object makes the saving roll, it takes in a damage object, and it returns true if successful
class Saver():
    def __init__(self, armourSave, invulnerableSave, fnp, wounds):
        self.myModelObject = ModelObject(wounds, fnp)
        self.myArmourSave = armourSave
        self.myInvulnerableSave = invulnerableSave
        self.myDiceRoller = DiceRoller(6)
        self.myHalveDamage = False
        self.myReduceDamageBy1 = False

    def __call__(self, aDamageObject):
        diceRoll = self.myDiceRoller()
        if (diceRoll >= (
                self.myArmourSave + aDamageObject.myAp) or diceRoll >= self.myInvulnerableSave) and diceRoll != 1 \
                and aDamageObject.myType != 'mortal':
            return True
        else:
            if self.myHalveDamage:
                aDamageObject.halveDamage()
            if self.myReduceDamageBy1:
                aDamageObject.reduceDamage(1)
            self.myModelObject.applyDamage(aDamageObject.myDamage)
            return False


class SystemObject:
    def __init__(self, aHitter, aWounder, aSaver, numShots):
        self.myHitter = aHitter
        self.myWounder = aWounder
        self.mySaver = aSaver
        self.myNumShots = numShots
        self.myDiceRoller = DiceRoller(6)
        # variables storing statistics
        self.myRunningHitSuccess = []
        self.myTotalNumberShots = 0
        self.myRunningWounds = []
        self.mySaves = 0
        self.myReceivedDamage = []
        self.myLostModels = []

    def __call__(self):
        numShots = diceToNum(self.myNumShots)
        self.myTotalNumberShots += numShots
        diceValue = self.myDiceRoller(numShots)
        hits = []
        wounds = []
        for j in diceValue:
            hits += self.myHitter(j)
        self.myRunningHitSuccess.append(hits.count('success'))
        for j in hits:
            wounds += self.myWounder(self.myDiceRoller(), j)
        self.myRunningWounds.append(len(wounds))
        for j in wounds:
            if self.mySaver(j):
                self.mySaves += 1
        self.myLostModels.append(self.mySaver.myModelObject.myLostModelsCounter)
        self.myReceivedDamage.append(self.mySaver.myModelObject.myTotalDamageRecieved)
        self.mySaver.myModelObject.reset()

    def finalise(self):
        hitSuccessRate = 100 * sum(self.myRunningHitSuccess) / self.myTotalNumberShots
        print(
            "hits: " + str(sum(self.myRunningHitSuccess)) + " success rate:" + str(hitSuccessRate))
        woundSuccessRate = 100 * sum(self.myRunningWounds) / (sum(self.myRunningHitSuccess))
        print("wounds: " + str(sum(self.myRunningWounds)) + " success rate:" + str(woundSuccessRate))
        saveSuccessRate = 100 * self.mySaves / sum(self.myRunningWounds)
        print("saves: " + str(self.mySaves) + " success rate:" + str(saveSuccessRate))
        print("Damage received: " + str(sum(self.myReceivedDamage) / len(self.myReceivedDamage)) + " lost models: "
              + str(sum(self.myLostModels) / len(self.myLostModels)))
