print("Hello World!")

from Dice_rolling.DiceRollModule import Hitter, Wounder, Saver, SystemObject

numIterations = 100000

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