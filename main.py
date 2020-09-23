print("Hello World!")

from DiceRollModule import Hitter, Wounder, Saver, SystemObject

def createHitter(bs, rerolls='none', hitModifier=0, autoWoundModified=100, autoWoundUnmodified=100, autoHit=False,
                 mortalWound=[], mortalWoundIsModified=False, explodingHits=[], explodingHitsModified=False):
    output = Hitter(bs)
    output.myRerollType = rerolls
    output.myAutoWound = autoWoundUnmodified
    output.myAutoWoundModified = autoWoundModified
    output.myAutoSuccess = autoHit
    output.myMortalWound = mortalWound
    output.myMortalWoundIsModified = mortalWoundIsModified
    output.myExplodingHits = explodingHits
    output.myExplodingHitsIsModified = explodingHitsModified
    return output

def createWounder(strength, toughness, baseAp, baseDamage, rerolls='none', woundModifier=0,rendDiceRoll=100,
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

for i in range(0,numIterations):
    aSystemObject()

aSystemObject.finalise()