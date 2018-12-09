import unittest

from Logic import Logic
from matchingCard import listOfCard

class testLogic(unittest.TestCase):
    def setUp(self):
        self.t1 = Logic()

    def testDrawCard(self):
        newCard = self.t1.drawCard()
        try:
            self.assertIn(newCard, listOfCard)
        except:
            self.assertEqual(newCard[-1], 'D')


    def testCardSum(self):
        self.assertEqual(self.t1.cardSum(['spadesA', 'heart10', 'club5', 'diamond8']), 24)

    def testDie(self):
        self.t1.pool = 50
        self.t1.playerMoney = 100
        self.t1.die()
        self.assertEqual(self.t1.pool, 0)
        self.assertEqual(self.t1.playerMoney, 50)

    def testSetPool(self):
        self.t1.setPool(100)
        self.assertEqual(self.t1.pool, 100)

    def testEndGame(self):
        self.t1.dealerCard = ['club7', 'heart10']
        for i in [(16, -1), (17, 0), (18, 1)]:
            self.t1.playerNum = i[0]
            self.t1.endGame()
            self.assertEqual(self.t1.endGame()[0], i[1])
        self.t1.playerNum = 21
        self.t1.endGame()
        self.assertEqual(self.t1.endGame()[0], 2)


if __name__ == "__main__":
    unittest.main()
