from DiceRollModule import *

def hitterTester(aHitter, input, expectedOutput, testName):
    print(testName)
    for i in range(0, 6):
        output = aHitter(input[i])
        if output != expectedOutput[i]:
            why = output
            fail = expectedOutput[i]
            raise Exception("failed " + testName)

def WounderDamageTypeTest(aWounder, input, numTests, inputType, expectedOutput, testName):
    print(testName)
    for i in range(0, numTests):
        output = aWounder(input[i], inputType)[0].myType
        if output != expectedOutput[i]:
            why = output
            fail = expectedOutput[i]
            raise Exception("failed " + testName)

def WounderDamageAmountTest(aWounder, input, numTests, inputType, expectedOutput, testName):
    print(testName)
    for i in range(0, numTests):
        output = aWounder(input[i], inputType)[0].myDamage
        if output != expectedOutput[i]:
            why = output
            fail = expectedOutput[i]
            raise Exception("failed " + testName)

def WounderApTest(aWounder, input, numTests, inputType, expectedOutput, testName):
    print(testName)
    for i in range(0, numTests):
        output = aWounder(input[i], inputType)[0].myAp
        if output != expectedOutput[i]:
            why = output
            fail = expectedOutput[i]
            raise Exception("failed " + testName)

class DummyDiceRoller():
    def __init__(self,value):
        self.myReturnValue = value

    def __call__(self):
        return self.myReturnValue

def saverTest(aSaver, aDamageObject, diceInput, expectedOutput, testName):
    print(testName)
    for i in range(0, 6):
        aSaver.myDiceRoller = DummyDiceRoller(diceInput[i])
        output = aSaver(aDamageObject)
        if output != expectedOutput[i]:
            raise Exception(testName)


#test hitter
testHitter = Hitter(3)
diceRolls = [1,2,3,4,5,6]
expectedOutput = [['fail'], ['fail'], ['success'], ['success'], ['success'], ['success']]
hitterTester(testHitter, diceRolls, expectedOutput, 'basic hitter test')

#test auto hit
testHitter = Hitter(3)
diceRolls = [1,2,3,4,5,6]
expectedOutput = [['success'], ['success'], ['success'], ['success'], ['success'], ['success']]
testHitter.myAutoSuccess = True
hitterTester(testHitter, diceRolls, expectedOutput, 'auto success test')

#test exploding 6s
testHitter = Hitter(3)
diceRolls = [1,2,3,4,5,6]
testHitter.myExplodingHits = [6,1]
expectedOutput = [['fail'], ['fail'], ['success'], ['success'], ['success'], ['success','success']]
hitterTester(testHitter, diceRolls, expectedOutput, 'exploding 6 hitter test')

#test exploding mortal wounds
testHitter = Hitter(3)
diceRolls = [1,2,3,4,5,6]
testHitter.myMortalWound = [6,1]
expectedOutput = [['fail'], ['fail'], ['success'], ['success'], ['success'], ['mortal','success']]
hitterTester(testHitter, diceRolls, expectedOutput, 'mortal wounds on 6 hitter test')

#test auto wounding
testHitter = Hitter(3)
diceRolls = [1,2,3,4,5,6]
testHitter.myAutoWound = 6
expectedOutput = [['fail'], ['fail'], ['success'], ['success'], ['success'], ['wound']]
hitterTester(testHitter, diceRolls, expectedOutput, 'auto wound on 6 hitter test')

#test positive hit modifiers
testHitter = Hitter(3)
diceRolls = [1,2,3,4,5,6]
testHitter.myDiceModifier = 1
expectedOutput = [['fail'], ['success'], ['success'], ['success'], ['success'], ['success']]
hitterTester(testHitter, diceRolls, expectedOutput, 'bonus to hit test')

#test negative hit modifiers
testHitter = Hitter(3)
testHitter.myDiceModifier = -1
diceRolls = [1,2,3,4,5,6]
expectedOutput = [['fail'], ['fail'], ['fail'], ['success'], ['success'], ['success']]
hitterTester(testHitter, diceRolls, expectedOutput, 'negative to hit test')


########################################################################################################################
#test wounder, test correct success roll from strength and toughness
testWounder = Wounder(4,4,1,1)
if testWounder.mySuccessRoll != 4:
    raise Exception("failed wound success roll test")
testWounder = Wounder(4,3,1,1)
if testWounder.mySuccessRoll != 3:
    raise Exception("failed wound success roll test")
testWounder = Wounder(4,2,1,1)
if testWounder.mySuccessRoll != 2:
    raise Exception("failed wound success roll test")
testWounder = Wounder(4,5,1,1)
if testWounder.mySuccessRoll != 5:
    raise Exception("failed wound success roll test")
testWounder = Wounder(4,8,1,1)
if testWounder.mySuccessRoll != 6:
    raise Exception("failed wound success roll test")

# #test if wounder works correctly
testWounder = Wounder(4,4,3,2)
diceRolls = [4,5,6]
expectedOutput = ['normal','normal','normal']
numTests = 3
WounderDamageTypeTest(testWounder, diceRolls, numTests, 'normal', expectedOutput, 'wounder type test')
expectedOutput = [2,2,2]
numTests = 3
WounderApTest(testWounder, diceRolls, numTests, 'normal', expectedOutput, 'wounder AP test')
expectedOutput = [3,3,3]
numTests = 3
WounderDamageAmountTest(testWounder, diceRolls, numTests, 'normal', expectedOutput, 'wounder Damage test')

#test if auto wound in generates basic wound out
testWounder = Wounder(4,4,3,2)
diceRolls = [1,2,3,4,5,6]
expectedOutput = ['normal','normal','normal','normal','normal','normal']
numTests = 6
WounderDamageTypeTest(testWounder, diceRolls, numTests, 'wound', expectedOutput, 'auto wound in wounder type test')

#test if mortal wound in generates basic wound out
testWounder = Wounder(4,4,3,2)
diceRolls = [1,2,3,4,5,6]
expectedOutput = ['mortal','mortal','mortal','mortal','mortal','mortal']
numTests = 6
WounderDamageTypeTest(testWounder, diceRolls, numTests, 'mortal', expectedOutput, 'mortal wound in wounder type test')

#test extra damage on 6s
testWounder = Wounder(4,4,3,2)
testWounder.myExplodingDamage = [6,'2']
diceRolls = [4,5,6]
expectedOutput = [3,3,5]
numTests = 3
WounderDamageAmountTest(testWounder, diceRolls, numTests, 'normal', expectedOutput, 'wounder extra Damage test')

#test rending on 6s
testWounder = Wounder(4,4,3,2)
testWounder.myRending = [6,3]
diceRolls = [4,5,6]
expectedOutput = [2,2,5]
numTests = 3
WounderApTest(testWounder, diceRolls, numTests, 'normal', expectedOutput, 'wounder extra AP test')

#test mortal wounds on 6s
testWounder = Wounder(4,4,3,2)
testWounder.myMortalWounds = [6,'1']
diceRolls = [4,5,6]
expectedOutput = ['normal','normal','mortal']
numTests = 3
WounderDamageTypeTest(testWounder, diceRolls, numTests, 'normal', expectedOutput, 'mortal wounds on 6s type test')

#test exploding wounds
testName = "failed exploding wounds on 6s test"
testWounder = Wounder(4,4,3,2)
testWounder.myExplodingWounds = [6,1]
dice5Output = testWounder(5, 'normal')
dice6Output = testWounder(6, 'normal')
if not ((len(dice5Output) == 1) and (len(dice6Output) == 2)):
    raise Exception(testName)


#######################################################################################################################

#test saver works
testSaver = Saver(3,5,100,2)
testDamageObject = DamageObject('normal', 1, 0)
testSaver.myDiceRoller = DummyDiceRoller(3)
diceRolls = [1,2,3,4,5,6]
expectedOutput = [False, False, True, True, True, True]
saverTest(testSaver, testDamageObject, diceRolls, expectedOutput, "basic saver test")

#test armour penetration works
testSaver = Saver(3,5,100,2)
testDamageObject = DamageObject('normal', 1, 1)
testSaver.myDiceRoller = DummyDiceRoller(3)
diceRolls = [1,2,3,4,5,6]
expectedOutput = [False, False, False, True, True, True]
saverTest(testSaver, testDamageObject, diceRolls, expectedOutput, "armour penetration saver test")

#test invunerable save works
testSaver = Saver(3,5,100,2)
testDamageObject = DamageObject('normal', 1, 100)
testSaver.myDiceRoller = DummyDiceRoller(3)
diceRolls = [1,2,3,4,5,6]
expectedOutput = [False, False, False, False, True, True]
saverTest(testSaver, testDamageObject, diceRolls, expectedOutput, "invunerable save test")

#test mortal wounds ignore everything
testSaver = Saver(3, 5, 100, 2)
testDamageObject = DamageObject('mortal', 1, 0)
testSaver.myDiceRoller = DummyDiceRoller(3)
diceRolls = [1, 2, 3, 4, 5, 6]
expectedOutput = [False, False, False, False, False, False]
saverTest(testSaver, testDamageObject, diceRolls, expectedOutput, "mortal wound saver test")

#test models die
testName = "model death count test"
print(testName)
testSaver = Saver(3, 5, 100, 2)
testDamageObject = DamageObject('normal', 1, 0)
testSaver.myDiceRoller = DummyDiceRoller(2)
testSaver(testDamageObject)
if testSaver.myModelObject.myRemainingWounds != 1:
    raise Exception(testName)
testSaver(testDamageObject)
if testSaver.myModelObject.myRemainingWounds != 2 or testSaver.myModelObject.myLostModelsCounter != 1:
    raise Exception(testName)

#test damage spill over
testName = "damage spillover test"
print(testName)
testSaver = Saver(3,5,100,2)
testDamageObject = DamageObject('normal', 100, 0)
testSaver.myDiceRoller = DummyDiceRoller(2)
testSaver(testDamageObject)

if testSaver.myModelObject.myRemainingWounds != 2 or testSaver.myModelObject.myLostModelsCounter != 1:
    raise Exception(testName)

# Do I explode test, modified v unmodified, unmodified works even when impossible to hit